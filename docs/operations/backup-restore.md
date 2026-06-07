# Backup & Restore

_Closes #76._

This project ships a small, dependency-light backup/restore pair plus a
scheduled GitHub Actions workflow that runs daily.

## Components

| Path                                          | Purpose                                |
|-----------------------------------------------|----------------------------------------|
| `scripts/backup.sh`                           | `pg_dump` → gzip → local dir, optional S3 upload. |
| `scripts/restore.sh`                          | `gunzip` → `psql` round-trip restore.  |
| `.github/workflows/database-backup.yml`       | Daily 02:00 UTC run; smoke-tests on PRs / forks with no prod secret set. |

## Running manually

```
export DATABASE_URL=postgres://user:pw@host:5432/ha_tracker
./scripts/backup.sh
```

Default output directory is `/var/backups/ha-tracker`; override with
`BACKUP_DIR`. To also push to S3:

```
export S3_BUCKET=my-ha-tracker-backups
./scripts/backup.sh
```

AWS credentials are picked up from the usual `AWS_ACCESS_KEY_ID` /
`AWS_SECRET_ACCESS_KEY` / `AWS_DEFAULT_REGION` environment variables (or
an IAM instance role).

## Restoring

> ⚠️ Restoring overwrites the target database. Always restore into an
> empty database (e.g. `ha_tracker_restore`), validate, then cut over.

```
export DATABASE_URL=postgres://user:pw@host:5432/ha_tracker_restore
./scripts/restore.sh /var/backups/ha-tracker/20260607-020000.sql.gz
```

## Scheduled workflow

`.github/workflows/database-backup.yml` runs daily at 02:00 UTC. Two modes:

- **Prod mode**: when the `DATABASE_URL_PROD` secret is set, it runs
  `backup.sh` against that DB. If `BACKUP_S3_BUCKET` (+ AWS secrets) is
  also set, the dump is uploaded.
- **Smoke mode**: when no prod secret is configured (e.g. forks, PR
  builds), the workflow spins up a throwaway `postgres:16` container,
  seeds a tiny table, backs it up, drops the table, restores from the
  backup, and asserts the row count round-trips. This means the script
  itself is tested on every run, even without prod access.

### Required repository secrets (prod mode)

| Secret                          | Purpose                              |
|---------------------------------|---------------------------------------|
| `DATABASE_URL_PROD`             | Postgres connection string.          |
| `BACKUP_S3_BUCKET` (optional)   | Target S3 bucket name.               |
| `BACKUP_AWS_ACCESS_KEY_ID`      | AWS credentials for `aws s3 cp`.     |
| `BACKUP_AWS_SECRET_ACCESS_KEY`  |                                       |
| `BACKUP_AWS_REGION`             |                                       |

## Retention policy

- **Local on-disk**: `RETENTION_DAYS` (default **30**) — older
  `*.sql.gz` files in `BACKUP_DIR` are pruned by `backup.sh` after a
  successful write/upload.
- **S3**: enforced at the bucket level via an S3 lifecycle rule (operator
  responsibility — recommended 30 days hot + 90 days Glacier transition
  before deletion).
- **Smoke artifacts**: uploaded as a GitHub Actions artifact with a
  7-day retention so operators can grab a recent dump for local restore
  drills.

## Tested restore procedure

A real restore drill should be performed at least once a quarter:

1. Provision a scratch Postgres instance.
2. Set `DATABASE_URL` to point at it (empty DB).
3. `./scripts/restore.sh <most-recent-backup>.sql.gz`.
4. Run `SELECT COUNT(*) FROM gps_logs;` and spot-check a few rows.
5. Connect a local copy of the frontend at the scratch backend and verify
   the UI renders.
6. Tear down the scratch instance.

Record the date/version of the last successful drill in the repository
release notes.

## Failure modes

- `pg_dump` not on PATH → install `postgresql-client`.
- S3 upload failure does NOT block the local write — `backup.sh` exits
  non-zero, but the local `.sql.gz` is still on disk and you can retry
  the upload manually with `aws s3 cp`.
- The script intentionally uses `--no-owner --no-privileges` so dumps
  restore cleanly into databases with different role names.
