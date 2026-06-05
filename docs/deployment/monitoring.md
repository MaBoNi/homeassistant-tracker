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

## docker-compose stack

Add the following to `docker-compose.yml` (or a `docker-compose.obs.yml`
overlay):

```yaml
  loki:
    image: grafana/loki:3.2.0
    container_name: tracker-loki
    restart: unless-stopped
    command: -config.file=/etc/loki/local-config.yaml
    volumes:
      - loki_data:/loki
    networks: [default]

  promtail:
    image: grafana/promtail:3.2.0
    container_name: tracker-promtail
    restart: unless-stopped
    command: -config.file=/etc/promtail/config.yaml
    volumes:
      - ./observability/promtail-config.yaml:/etc/promtail/config.yaml:ro
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on: [loki]

  grafana:
    image: grafana/grafana:11.3.0
    container_name: tracker-grafana
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./observability/grafana/provisioning:/etc/grafana/provisioning:ro
    ports:
      - "127.0.0.1:3000:3000"   # Front with Caddy / Tailscale, not public
    depends_on: [loki]

volumes:
  loki_data:
  grafana_data:
```

`promtail-config.yaml` should use the `docker_sd_config` discovery so
every container picks up labels automatically:

```yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ["__meta_docker_container_name"]
        target_label: container
      - source_labels: ["__meta_docker_container_label_com_docker_compose_service"]
        target_label: service
```

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
