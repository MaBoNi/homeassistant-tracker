#!/bin/sh
set -e

# Backend that nginx proxies /api/ and /auth/ to (issue #115). The browser
# never sees this address, and nothing secret is written into the page.
BACKEND_UPSTREAM="${BACKEND_UPSTREAM:-http://backend:5000}"

# /etc/nginx is root-owned and we run as nginx, so render the config to /tmp.
sed "s|__BACKEND_UPSTREAM__|${BACKEND_UPSTREAM}|g" /etc/nginx/nginx.conf > /tmp/nginx.conf

# Start Nginx
exec nginx -c /tmp/nginx.conf -g 'daemon off;'
