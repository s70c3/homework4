# Base image
FROM nginx:alpine

# Copy static files
COPY ./static /usr/share/nginx/html/static

# Copy templates
COPY ./pages /usr/share/nginx/html/pages

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf