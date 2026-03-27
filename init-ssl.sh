#!/bin/bash
set -e

# Step 1: Start nginx with init config (HTTP only, for certbot challenge)
echo "Starting nginx with temporary config..."
cp nginx/nginx-init.conf nginx/nginx-active.conf
docker compose up -d nginx

# Step 2: Request certificate
echo "Requesting SSL certificate..."
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email admin@nickorp.com \
    --agree-tos \
    --no-eff-email \
    -d nickorp.com \
    -d www.nickorp.com

# Step 3: Switch to full config with SSL
echo "Switching to SSL config..."
cp nginx/nginx.conf nginx/nginx-active.conf
docker compose restart nginx

echo "SSL setup complete!"
