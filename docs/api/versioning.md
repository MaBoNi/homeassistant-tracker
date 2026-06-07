# API Versioning Policy

_Closes #78._

## Overview

The Home Assistant Tracker HTTP API is versioned via a URL prefix:

- **Canonical:** `/api/v1/...`
- **Deprecated alias (legacy):** `/api/...` — kept for one release cycle, slated for removal.

Clients SHOULD call `/api/v1/...` directly. Calls to the bare `/api/...`
prefix continue to work but receive `Deprecation: true`, a `Sunset` date,
and a `Link: <successor>; rel="successor-version"` header on every response.

## Discovery

```
GET /api/v1/version
→ { "api_version": "v1", "current": true,
    "deprecated_alias": false, "canonical_prefix": "/api/v1" }
```

The same endpoint exists at `/api/version` and will respond with
`"deprecated_alias": true` along with the deprecation headers.

## Lifecycle

Each major API version moves through three phases:

| Phase       | Meaning                                                         |
|-------------|-----------------------------------------------------------------|
| **Active**  | Fully supported. New features land here.                        |
| **Deprecated** | Still served, but emits `Deprecation` + `Sunset` headers. New features will NOT be added. Clients should migrate. |
| **Retired** | Removed. Requests return `410 Gone`.                            |

A version stays Deprecated for **at least 12 months** before retirement,
giving downstream integrations time to migrate.

## Current status

| Prefix     | Status     | Sunset                  |
|------------|------------|-------------------------|
| `/api/v1`  | Active     | —                       |
| `/api`     | Deprecated | 2027-06-06 (12 months)  |

## Versioning rules

- **Backwards-compatible additions** (new endpoints, new optional fields) do
  NOT bump the version.
- **Breaking changes** (removed/renamed fields, changed response shape,
  changed status code semantics) require a new major version (`/api/v2`).
- When `/api/v2` ships, `/api/v1` moves to Deprecated and starts its own
  ≥12-month sunset clock.

## Client guidance

- Always send requests to `/api/v1/...`.
- Watch for the `Deprecation` and `Sunset` response headers in CI/logs.
- Pin to a major version in client config so a server-side rollout of
  `/api/v2` doesn't break you implicitly.
