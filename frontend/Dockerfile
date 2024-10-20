FROM nginx:alpine

# Copy the static HTML, CSS, and JS files to the Nginx public directory
COPY . /usr/share/nginx/html

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the default Nginx port
EXPOSE 80

# Replace environment variables in the configuration file and start Nginx
CMD ["/entrypoint.sh"]
