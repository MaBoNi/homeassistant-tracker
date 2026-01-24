# Security Documentation

## Known Security Limitations

### Frontend Authentication Token Exposure

**Status**: Known limitation
**Severity**: High
**CWE**: CWE-312 (Cleartext Storage of Sensitive Information)

#### Issue Description

The current authentication implementation embeds the `TRACKER_APP_TOKEN` directly into the frontend JavaScript file (`script.js`) at container startup via the `entrypoint.sh` script. This makes the token accessible to anyone who:
- Views the page source
- Uses browser developer tools
- Intercepts the JavaScript file

This effectively makes the API publicly accessible to anyone who can access the frontend.

#### Current Mitigation

- Rate limiting has been implemented to prevent abuse (30 req/min for GPS data)
- CORS is restricted to specific origins
- All access is logged for monitoring
- Authentication still prevents casual API browsing

#### Recommended Solutions (Future Work)

**Option 1: Backend-for-Frontend Pattern (Recommended)**
- Implement session-based authentication in the frontend
- Backend maintains the API token and makes requests on behalf of authenticated users
- Frontend never sees the actual API token
- Add user login system (OAuth, local accounts, etc.)

**Option 2: OAuth2/JWT with Short-Lived Tokens**
- Implement proper OAuth2 flow with short-lived access tokens
- Frontend requests tokens from auth server
- Tokens are scoped and time-limited (e.g., 1 hour)
- Refresh token mechanism for seamless UX

**Option 3: API Gateway**
- Place an API gateway between frontend and backend
- Gateway handles authentication and authorization
- Different credentials for frontend vs direct API access
- Additional security policies at gateway level

#### Temporary Workarounds

Until a proper solution is implemented:

1. **Accept the Risk**: Understand that frontend access = API access
2. **Monitor Usage**:
   - Review logs regularly for unusual access patterns
   - Set up alerts for excessive API calls
   - Track IP addresses accessing the API
3. **Rate Limiting**: Already implemented (see commit 515211b)
4. **Network Restrictions**: Deploy behind VPN or restrict access by IP if possible
5. **Token Rotation**: Regularly rotate the `TRACKER_APP_TOKEN` (every 30-90 days)

#### Detection

Monitor for:
- API calls from unexpected IP addresses
- Requests without corresponding frontend page loads
- Unusual access patterns or times
- Sudden spike in API usage

## Other Security Considerations

### Credential Management

- Never commit `.env` file to version control (already in `.gitignore`)
- Rotate credentials regularly:
  - `HA_TOKEN`: Every 90 days or if compromised
  - `TRACKER_APP_TOKEN`: Every 30-90 days
  - `POSTGRES_PASSWORD`: Every 90 days
- Use strong, randomly generated passwords (minimum 32 characters)

### HTTPS/TLS

The current deployment runs over HTTP. For production:
- Deploy behind a reverse proxy (Nginx, Traefik, Caddy)
- Use Let's Encrypt for free SSL certificates
- Enable HSTS headers
- Redirect all HTTP to HTTPS

### Database Security

- PostgreSQL container runs with restricted user (postgres)
- Database is not exposed externally (only accessible within Docker network)
- Consider enabling PostgreSQL SSL connections for added security
- Implement regular backups and test restore procedures

### Container Security

- Both backend and frontend run as non-root users (appuser, nginx)
- Images built with supply chain attestations (SBOM, provenance)
- Regular dependency updates via Dependabot
- Consider adding container scanning (Trivy, Snyk) to CI/CD

## Security Update Process

When security vulnerabilities are discovered:

1. Assess severity and impact
2. Review Dependabot PRs within 7 days
3. Test security updates in development environment
4. Deploy critical updates within 24 hours
5. Document changes in commit messages and release notes

## Contact

For security concerns, please create a private security advisory in GitHub or contact the maintainers directly.

## Last Updated

2026-01-24
