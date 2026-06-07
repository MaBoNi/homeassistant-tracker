#!/usr/bin/env bash
# scripts/backup.sh
#
# Automated Postgres backup for Home Assistant Tracker (issue #76).
#
# Usage:
#   DATABASE_URL=postgres://... ./scripts/backup.sh
#
# Environment:
#   DATABASE_URL   (required) postgres connection string consumed by pg_dump.
#   BACKUP_DIR     (optional, default /var/backups/ha-tracker) local output dir.
#   S3_BUCKET      (optional) if set, the gzipped dump is also uploaded with
#                  `aws s3 cp` to s3://$S3_BUCKET/<basename>.
#   RETENTION_DAYS (optional, default 30) local files older than this many days
#                  are pruned after a successful upload.

set -euo pipefail

if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "backup.sh: DATABASE_URL is required" >&2
  exit 1
fi

BACKUP_DIR="${BACKUP_DIR:-/var/backups/ha-tracker}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TS="$(date -u +%Y%m%d-%H%M%S)"
OUT="${BACKUP_DIR}/${TS}.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "backup.sh: writing $OUT"
# pg_dump streams plain SQL; gzip in-line to avoid an intermediate file.
# `--no-owner --no-privileges` keeps restores portable across roles.
pg_dump --no-owner --no-privileges "$DATABASE_URL" | gzip -9 > "$OUT"

SIZE="$(stat -c%s "$OUT" 2>/dev/null || stat -f%z "$OUT")"
echo "backup.sh: wrote $OUT (${SIZE} bytes)"

if [[ -n "${S3_BUCKET:-}" ]]; then
  echo "backup.sh: uploading to s3://${S3_BUCKET}/$(basename "$OUT")"
  aws s3 cp "$OUT" "s3://${S3_BUCKET}/$(basename "$OUT")"
fi

# Prune local copies older than RETENTION_DAYS to keep disk bounded.
find "$BACKUP_DIR" -maxdepth 1 -type f -name '*.sql.gz' -mtime "+${RETENTION_DAYS}" -print -delete || true

echo "backup.sh: done"
