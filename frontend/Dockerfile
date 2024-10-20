# Use a lightweight Nginx image to serve the static HTML page
FROM nginx:alpine

# Copy the static HTML, CSS, and JS files to the Nginx public directory
COPY . /usr/share/nginx/html

# Expose the default Nginx port
EXPOSE 80

# Start Nginx when the container is run
CMD ["nginx", "-g", "daemon off;"]
