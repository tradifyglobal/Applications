#!/bin/bash
# Web Server (Nginx + Gunicorn) Setup Script
# Run as: sudo bash webserver_setup.sh

set -e

echo "=================================="
echo "Web Server Setup (Nginx + Gunicorn)"
echo "=================================="
echo ""

APP_DIR="/var/www/erp"
APP_USER="erpadmin"

echo "[1/4] Creating Gunicorn socket..."
cat > /etc/systemd/system/gunicorn.socket << 'EOF'
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=127.0.0.1:8000
Accept=false

[Install]
WantedBy=sockets.target
EOF

echo "[2/4] Creating Gunicorn service..."
cat > /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
User=$APP_USER
Group=www-data
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/gunicorn \\
    --workers 4 \\
    --worker-class sync \\
    --bind unix:/run/gunicorn.sock \\
    --timeout 120 \\
    core.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
KillSignal=SIGQUIT
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

echo "✓ Gunicorn configured"
echo ""

echo "[3/4] Creating Nginx configuration..."
read -p "Enter your domain (e.g., example.com): " DOMAIN

cat > /etc/nginx/sites-available/erp << EOF
upstream erp {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN www.$DOMAIN;
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;
    
    client_max_body_size 20M;
    
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    add_header Strict-Transport-Security "max-age=31536000" always;

    location /static/ {
        alias $APP_DIR/static/;
        expires 30d;
    }

    location /media/ {
        alias $APP_DIR/media/;
    }

    location / {
        proxy_pass http://erp;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/erp /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx config
nginx -t
echo "✓ Nginx configured"
echo ""

echo "[4/4] Enabling services..."
systemctl daemon-reload
systemctl enable gunicorn.socket gunicorn.service
systemctl enable nginx
systemctl enable redis-server

# Start services
systemctl start gunicorn.socket gunicorn.service
systemctl restart nginx

echo "✓ Services enabled and started"
echo ""

echo "=================================="
echo "✓ Web Server Setup Complete!"
echo "=================================="
echo ""
echo "To setup SSL certificate, run:"
echo "sudo certbot certonly --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "Then update Nginx with:"
echo "sudo systemctl reload nginx"
echo ""
