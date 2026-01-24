FROM nginx:alpine

# Copy custom nginx configuration for non-root operation
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static HTML, CSS, and JS files to the Nginx public directory
COPY . /usr/share/nginx/html

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Create necessary directories and set permissions for non-root user
RUN chmod +x /entrypoint.sh && \
    mkdir -p /tmp/client_temp /tmp/proxy_temp_path /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp && \
    chown -R nginx:nginx /usr/share/nginx/html /tmp/client_temp /tmp/proxy_temp_path /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp /var/log/nginx && \
    chmod -R 755 /usr/share/nginx/html && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx

# Switch to non-root user
USER nginx

# Expose non-privileged port
EXPOSE 8080

# Replace environment variables in the configuration file and start Nginx
CMD ["/entrypoint.sh"]
