#!/bin/sh

# Replace the placeholder in script.js with the actual environment variable
#sed -i 's|__TRACKER_APP_TOKEN__|'${TRACKER_APP_TOKEN}'|g' /usr/share/nginx/html/script.js

# Replace placeholders in the script.js with the actual environment variables
sed -i "s|__TRACKER_APP_TOKEN__|$TRACKER_APP_TOKEN|g" /usr/share/nginx/html/script.js
sed -i "s|__BACKEND_API_URL__|$BACKEND_API_URL|g" /usr/share/nginx/html/script.js



# Start Nginx
nginx -g 'daemon off;'




