# HTTPS / TLS in Production

The bundled `docker-compose.yml` exposes the backend on `:5171` and the
frontend on `:5172` over plain HTTP. That is fine for local development, but
**do not** point a public DNS record at those ports. Production deployments
must terminate TLS in front of both services.

This guide describes the simplest robust setup: a [Caddy](https://caddyserver.com/)
reverse proxy that obtains and renews Let's Encrypt certificates
automatically, fronts both the frontend and the backend API on a single
hostname, and adds standard hardening headers.

If you already run Traefik / nginx-proxy / a cloud load balancer, the same
routing rules apply — only the syntax changes.

---

## 1. DNS

Point an A/AAAA record at the host running Docker, e.g.:

```
tracker.example.com.   A   203.0.113.42
```

Caddy needs ports `80` and `443` reachable from the public internet so the
HTTP-01 / TLS-ALPN-01 challenges can complete.

---

## 2. Add a `caddy` service to docker-compose

Append the following service to `docker-compose.yml` (or, preferably, keep
production overrides in a separate `docker-compose.prod.yml`):

```yaml
  caddy:
    image: caddy:2-alpine
    container_name: homeassistant-tracker-caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "443:443/udp"   # HTTP/3
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      backend:
        condition: service_healthy
      frontend:
        condition: service_healthy

volumes:
  postgres_data:
  caddy_data:
  caddy_config:
```

Remove the public `ports:` mapping from the `backend` and `frontend`
services so they are only reachable via the Caddy network — Compose's
default bridge network already lets containers reach each other by service
name.

---

## 3. The `Caddyfile`

Create `Caddyfile` next to `docker-compose.yml`:

```caddy
{
    # Production email for Let's Encrypt account / expiry notices.
    email ops@example.com
}

tracker.example.com {
    encode zstd gzip

    # Strict-Transport-Security: opt all clients into HTTPS for a year and
    # allow preloading once you are confident the setup is permanent.
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options    "nosniff"
        X-Frame-Options           "SAMEORIGIN"
        Referrer-Policy           "strict-origin-when-cross-origin"
        # Caddy sets Server: Caddy by default — hide it.
        -Server
    }

    # API traffic → backend container, port 5000 (internal).
    handle_path /api/* {
        reverse_proxy backend:5000
    }

    # Everything else → frontend nginx container, port 8080 (internal).
    handle {
        reverse_proxy frontend:8080
    }
}
```

`handle_path` strips the `/api` prefix before forwarding; if your backend
already expects the `/api` prefix on its routes (it does — see
`backend/api/routes.py`), use `handle` instead and forward the full path:

```caddy
    handle /api/* {
        reverse_proxy backend:5000
    }
```

Pick whichever matches your backend's expectations and stay consistent.

---

## 4. Update `CORS_ORIGINS` and `BACKEND_API_URL`

In `.env` for production:

```
CORS_ORIGINS=https://tracker.example.com
BACKEND_API_URL=https://tracker.example.com/api
```

The frontend now talks to the API over the same origin, which sidesteps
most CORS issues entirely.

---

## 5. Bring it up

```bash
docker compose pull
docker compose up -d
docker compose logs -f caddy
```

On first run, Caddy will:

1. Solve an ACME challenge against `tracker.example.com`.
2. Provision a cert and store it under the `caddy_data` volume.
3. Begin serving HTTPS and HTTP/2 (and HTTP/3 if UDP/443 is open).

Renewals happen automatically ~30 days before expiry. Nothing to cron.

---

## 6. Production deployment checklist

Before flipping DNS:

- [ ] Backend and frontend `ports:` removed from public mapping (or bound
      to `127.0.0.1` only).
- [ ] `.env` contains strong `POSTGRES_PASSWORD`, `TRACKER_APP_TOKEN`,
      and `HA_TOKEN` values — none of them committed.
- [ ] `CORS_ORIGINS` set to the exact production origin (no `*`).
- [ ] `DROP_DB_ON_START` unset or `false`.
- [ ] Postgres volume on persistent storage with a backup strategy
      (see `docs/deployment/postgres-upgrade.md` for dump/restore).
- [ ] Caddy can reach the internet on 80/443 outbound and accept inbound
      on the same.
- [ ] HSTS verified with [hstspreload.org](https://hstspreload.org/) once
      satisfied with the cert chain.
- [ ] A monitoring story in place — see
      `docs/deployment/monitoring.md`.

---

## Alternative: Traefik

If you already run Traefik, attach labels to the `backend` and `frontend`
services instead of adding Caddy. The rules are equivalent:

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.tracker-api.rule=Host(`tracker.example.com`) && PathPrefix(`/api`)"
      - "traefik.http.routers.tracker-api.tls.certresolver=le"
      - "traefik.http.services.tracker-api.loadbalancer.server.port=5000"
```

Same idea, more verbose YAML.
