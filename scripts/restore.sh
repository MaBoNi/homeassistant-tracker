#!/usr/bin/env bash
# scripts/restore.sh
#
# Restore a Home Assistant Tracker Postgres backup written by backup.sh.
#
# Usage:
#   DATABASE_URL=postgres://... ./scripts/restore.sh /path/to/20260607-020000.sql.gz
#
# DESTRUCTIVE: the target database will receive every CREATE / COPY /
# INSERT in the dump. Restore into an EMPTY database, not a live one.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: restore.sh <backup.sql.gz>" >&2
  exit 1
fi

BACKUP_PATH="$1"

if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "restore.sh: DATABASE_URL is required" >&2
  exit 1
fi

if [[ ! -f "$BACKUP_PATH" ]]; then
  echo "restore.sh: $BACKUP_PATH not found" >&2
  exit 1
fi

echo "restore.sh: restoring $BACKUP_PATH into \$DATABASE_URL"
gunzip -c "$BACKUP_PATH" | psql --set ON_ERROR_STOP=on "$DATABASE_URL"
echo "restore.sh: done"
