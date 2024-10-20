#!/bin/sh

# Replace the placeholder in script.js with the actual environment variable
sed -i 's|__TRACKER_APP_TOKEN__|'${TRACKER_APP_TOKEN}'|g' /usr/share/nginx/html/script.js

# Start Nginx
nginx -g 'daemon off;'
