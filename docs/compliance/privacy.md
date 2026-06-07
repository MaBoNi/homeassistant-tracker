# Privacy & GDPR Compliance

_Closes #75._

## Data we collect

Home Assistant Tracker stores **GPS location history** fetched from a
configured Home Assistant instance:

| Field      | Purpose                                                        |
|------------|----------------------------------------------------------------|
| `user`     | The Home Assistant person entity (e.g. `alice`).               |
| `device`   | The device tracker entity (e.g. `alice_phone`).                |
| `latitude` / `longitude` | Reported coordinates.                            |
| `accuracy` | Reported accuracy radius in metres.                            |
| `timestamp`| When the point was sampled.                                    |

We do **not** collect: contact details, browsing data, contents of messages,
or any data outside Home Assistant's device-tracker entities.

## Lawful basis

This is a self-hosted operator-deployed application. The operator (the
person running the Docker stack) is the **data controller**. The lawful
basis is usually **legitimate interest** (household / family location
awareness) or **explicit consent** (where applicable). Operators are
responsible for collecting consent from tracked users before deployment.

## User rights (GDPR Arts. 15-21)

The following endpoints implement the practical mechanics:

| Right                          | Endpoint                                              |
|--------------------------------|--------------------------------------------------------|
| Right to access / portability  | `GET /api/v1/users/<username>/export?format=json\|csv`  |
| Right to erasure ("forgotten") | `DELETE /api/v1/users/<username>/data`                |
| Consent read                   | `GET /api/v1/users/<username>/consent`                |
| Consent grant / withdraw       | `POST /api/v1/users/<username>/consent`               |

All four endpoints require the standard `Authorization: Bearer ...` header.

### Example: export as CSV

```
curl -H "Authorization: Bearer $TOKEN" \
  "$BACKEND/api/v1/users/alice/export?format=csv" \
  -o alice-export.csv
```

### Example: record consent

```
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"consent": true, "policy_version": "1.0"}' \
  $BACKEND/api/v1/users/alice/consent
```

### Example: erase all data for a user

```
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  $BACKEND/api/v1/users/alice/data
```

Erasure removes all `gps_logs` rows for that user. The `user_consent`
row is intentionally preserved so a "withdrew consent at <timestamp>"
audit record survives the erasure.

## Retention policy (proposed)

| Tier              | Retention                |
|-------------------|--------------------------|
| Raw GPS points    | **180 days** by default. |
| Aggregated stats  | Indefinite (no PII).     |
| Consent records   | Lifetime of installation.|
| Database backups  | **30 days** (see `docs/operations/backup-restore.md`). |

Retention is enforced by the operator. A scheduled cleanup job is tracked
separately and is out of scope for #75.

## Storage location

All data lives in the Postgres database configured via `DATABASE_URL`. No
data is sent to third parties unless the operator has explicitly configured
S3 backup uploads (`S3_BUCKET`); in that case the operator is responsible
for ensuring the bucket region and encryption satisfy their jurisdiction.

## Contact

Issues / data-subject requests against a specific deployment should be
directed at the operator running that deployment, not the upstream
maintainers.
