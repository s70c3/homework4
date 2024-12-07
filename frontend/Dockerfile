# Base image
FROM nginx:alpine

# Copy static files
COPY pages/static /usr/share/nginx/html/static

# Copy templates
COPY ./templates /usr/share/nginx/html/templates

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf