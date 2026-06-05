# Security Monitoring & Alerting

This document covers an opinionated, lightweight observability stack for
homeassistant-tracker in production. The goals are modest:

1. Centralised, searchable logs from `backend`, `frontend`, `db`, and the
   TLS proxy.
2. Local retention long enough to investigate incidents (default: 14 days,
   rotated by size).
3. Push-style alerts to a Discord webhook for the handful of events that
   actually warrant a human looking at them — failed auth bursts, 5xx
   spikes, container restarts, certificate near-expiry.

The stack is **Loki + Promtail + Grafana**, all containerised. No
metrics server, no full Prometheus deployment — see the "Graduating to
Prometheus" section at the end for when that changes.

---

## Stack overview

```
 backend, frontend, caddy, db  ──►  Promtail  ──►  Loki  ──►  Grafana
                                                              │
                                                              ▼
                                                       Discord webhook
                                                       (Alertmanager-
                                                        compatible
                                                        webhook receiver)
```

- **Loki** stores logs. Single-binary, filesystem-backed for small
  deployments.
- **Promtail** tails Docker container logs via the Docker socket and ships
  them to Loki with service labels.
- **Grafana** is the query / dashboard / alert UI. Alert rules are
  defined declaratively under `grafana/provisioning/alerting/`.

---

## Quick start

Everything below is wired into the repo. To bring up the observability
stack:

1. Copy the contact-points template and paste your Discord webhook:

   ```bash
   cp observability/grafana/provisioning/alerting/contactpoints.yaml.example \
      observability/grafana/provisioning/alerting/contactpoints.yaml
   # edit the new file, replace REPLACE_WITH_YOUR_DISCORD_WEBHOOK_URL
   ```

2. Set `GRAFANA_ADMIN_PASSWORD` in your `.env` (see `.env.template`).

3. Bring up the stack:

   ```bash
   docker compose --profile observability up -d
   ```

4. Grafana: http://127.0.0.1:3000 (admin / your password). Front with
   Caddy / Tailscale for any non-local access — the port is bound to
   `127.0.0.1` on purpose.

Without the `--profile observability` flag, `docker compose up`
continues to start only `backend`, `frontend`, `db` — exactly as before.

## File layout

- `docker-compose.yml` — `loki`, `promtail`, `grafana` services, gated
  by the `observability` profile.
- `observability/loki-config.yaml` — Loki config, 14-day retention.
- `observability/promtail-config.yaml` — Docker socket discovery, ships
  every container's logs to Loki with `service` / `container` labels.
- `observability/grafana/provisioning/datasources/loki.yaml` —
  auto-wires Loki as the default datasource.
- `observability/grafana/provisioning/alerting/rules.yaml` — the 5 alert
  rules below, provisioned at boot.
- `observability/grafana/provisioning/alerting/contactpoints.yaml.example`
  — Discord webhook template. The real file is gitignored; copy it,
  fill it in, and Grafana picks it up on next restart.

---

## Log rotation

Docker's default `json-file` driver grows forever. Cap it in
`/etc/docker/daemon.json` on the host:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "5"
  }
}
```

`sudo systemctl restart docker` to apply. Existing containers keep the old
config until recreated.

Loki retention is set in its config (`retention_period: 336h` = 14 days).
Adjust for disk budget.

---

## Alert rules

Provision the following alerts under
`observability/grafana/provisioning/alerting/rules.yaml` (Grafana picks
them up at boot). The thresholds are starting points — tune after a week
of baseline data.

| Alert                      | Query (LogQL)                                                      | Threshold              | Severity |
|----------------------------|--------------------------------------------------------------------|------------------------|----------|
| Auth failure burst         | `sum(rate({service="backend"} \|= "401" [5m]))`                    | > 5 / min for 5 min    | warning  |
| Backend 5xx spike          | `sum(rate({service="backend"} \|~ " 5\\d\\d " [5m]))`              | > 1 / min for 5 min    | warning  |
| Container restart loop     | `count_over_time({service="backend"} \|= "Starting" [15m])`        | > 3 in 15 min          | critical |
| DB connection errors       | `sum(rate({service="backend"} \|~ "OperationalError\|psycopg2" [5m]))` | > 0 for 5 min       | critical |
| Caddy cert near expiry     | `{container="homeassistant-tracker-caddy"} \|~ "certificate.*expir"` | any in 24h           | warning  |

### Discord webhook receiver

Grafana supports Discord webhooks natively as a contact point:

1. In Discord: server settings → Integrations → Webhooks → New Webhook,
   copy the URL.
2. In Grafana: Alerting → Contact points → Add → Discord, paste URL.
3. Set the default notification policy to that contact point, or scope it
   to `severity=critical` and route warnings to email.

For everything-as-code, set it via provisioning under
`observability/grafana/provisioning/alerting/contactpoints.yaml`.

---

## What's covered, what isn't

Covered:

- Centralised logs from every service container.
- Discord pings for auth bursts, 5xx spikes, restart loops, DB errors,
  cert expiry.
- 14 days of searchable history.
- Disk-bounded log growth.

Not covered (intentionally, for v1):

- System-level metrics (CPU / memory / disk) — `cAdvisor` + Prometheus is
  the next step, see below.
- Distributed tracing.
- Synthetic uptime checks — handle externally (UptimeRobot, BetterStack)
  to catch the case where the host itself is down and can't send alerts.

---

## Graduating to Prometheus

Move from "logs + ad-hoc dashboards" to a full metrics stack when **any
of** the following becomes true:

- You need SLO-style alerting (e.g. "99.5% of requests under 300 ms over
  30 days") — that's a histogram-quantile query, which needs metrics, not
  logs.
- You're running more than ~3 application instances and need cross-cutting
  aggregation.
- You want long-horizon (>90 days) trend data without paying for log
  storage.

At that point, add `prometheus` + `node-exporter` + `cadvisor` to the
stack, point Grafana at Prometheus as a second data source, and migrate
the rate-based alerts from LogQL to PromQL. Loki stays — it remains the
best place to search the actual log lines a metric points you at.
