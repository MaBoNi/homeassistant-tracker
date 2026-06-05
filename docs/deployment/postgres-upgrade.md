# PostgreSQL 13 → 16 Upgrade

`docker-compose.yml` now pins `postgres:16-alpine`. PostgreSQL 13 is
end-of-life as of November 2025; 16 is the current stable major and has
~3 more years of upstream support.

There are **no application-level breaking changes** for
homeassistant-tracker:

- SQLAlchemy 2.0.50 (pinned) supports PostgreSQL 16 fully.
- `psycopg2-binary==2.9.12` (pinned) supports 16 since 2.9.x — no client
  bump required.
- Our schema uses no features touched by 13→16 deprecations.

The only thing that needs care is **the data directory format**. A
PostgreSQL data directory written by major version N cannot be opened by
major version N+1; you must either dump-and-restore or run `pg_upgrade`.
A fresh install with no existing data: just pull and go.

---

## Option A — fresh install (no data)

```bash
docker compose pull db
docker compose up -d db
```

Done. `init_db` on first backend boot creates the schema in PG16.

---

## Option B — dump and restore (recommended for existing prod data)

This is the safest path. ~15 min downtime for a small dataset, no
in-place format risk.

```bash
# 0. Stop the backend so no new writes land mid-dump.
docker compose stop backend

# 1. Dump from the running PG13 container.
docker compose exec -T db \
    pg_dump -U "$POSTGRES_USER" -Fc "$POSTGRES_DB" \
    > backup-pg13-$(date +%Y%m%d-%H%M).dump

# 2. Stop and remove the PG13 container (volume stays).
docker compose stop db
docker compose rm -f db

# 3. Rename or remove the old volume so PG16 starts fresh.
#    (Compose volume names are prefixed with the project name — adjust.)
docker volume rm homeassistant-tracker_postgres_data
# …or, safer: rename it so you can roll back.
#   docker volume create homeassistant-tracker_postgres_data_pg13_backup
#   (then copy the data directory across)

# 4. Pull and start PG16. It initialises a fresh cluster.
docker compose pull db
docker compose up -d db

# 5. Restore the dump into PG16.
docker compose exec -T db \
    pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
    --clean --if-exists --no-owner \
    < backup-pg13-YYYYMMDD-HHMM.dump

# 6. Bring the backend back.
docker compose start backend
docker compose logs -f backend
```

Verify a few row counts against the pre-dump numbers before declaring
victory.

---

## Option C — `pg_upgrade` in-place

Faster on large datasets (no full dump/restore round-trip) but trickier
to set up under Docker because `pg_upgrade` needs **both** the old and
new binaries pointing at **both** the old and new data directories
simultaneously. Use the official
[`tianon/postgres-upgrade`](https://hub.docker.com/r/tianon/postgres-upgrade)
helper image:

```bash
docker compose stop backend db

docker run --rm \
    -v homeassistant-tracker_postgres_data:/var/lib/postgresql/13/data \
    -v homeassistant-tracker_postgres_data_v16:/var/lib/postgresql/16/data \
    tianon/postgres-upgrade:13-to-16
```

Then point the `db` service at the new volume in `docker-compose.yml` and
`docker compose up -d`. Keep the old volume around until you've verified
the app works against PG16 — `docker volume rm` is irreversible.

For our dataset size (Home Assistant device-tracker history is small
relative to typical OLTP workloads), **Option B is recommended**. The
extra minutes vs. `pg_upgrade` aren't worth the operational complexity.

---

## Pre-flight checklist

- [ ] You have a current `pg_dump` you've verified is restorable (test it
      against a throwaway PG16 container first if paranoid).
- [ ] Disk has room for: existing data + dump + new cluster. Roughly
      2.5× the current PGDATA size during the cutover window.
- [ ] You're not mid-migration on the backend side — `init_db` should not
      run mid-upgrade.
- [ ] You've stopped writers (backend, scheduled jobs) before dumping.
- [ ] You know how to roll back: keep the PG13 volume until satisfied.

---

## Rollback

If anything goes sideways:

```bash
docker compose stop db
# Restore the old volume / dump.
# Re-pin docker-compose.yml back to postgres:13 (or 13-alpine).
docker compose up -d db backend
```

Then file an issue with what broke and we'll fix forward.
