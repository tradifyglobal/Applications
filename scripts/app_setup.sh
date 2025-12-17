#!/bin/bash
# Application Server Setup Script
# Run as: bash app_setup.sh

set -e

echo "=================================="
echo "ERP Application Setup"
echo "=================================="
echo ""

APP_DIR="/var/www/erp"
VENV_DIR="$APP_DIR/venv"

# Navigate to app directory
cd $APP_DIR

echo "[1/6] Creating Python virtual environment..."
python3.10 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

echo "[2/6] Upgrading pip and tools..."
pip install --upgrade pip setuptools wheel

echo "[3/6] Installing Python dependencies..."
pip install Django==4.2.0 \
    djangorestframework==3.14.0 \
    django-cors-headers==4.0.0 \
    django-filter==23.1 \
    drf-yasg==1.21.6 \
    djangorestframework-simplejwt==5.2.2 \
    psycopg2-binary==2.9.6 \
    gunicorn==20.1.0 \
    whitenoise==6.4.0 \
    python-dotenv==1.0.0 \
    celery==5.2.7 \
    redis==4.5.5 \
    pillow==9.5.0

echo "[4/6] Creating logs directory..."
mkdir -p $APP_DIR/logs
chmod 755 $APP_DIR/logs

echo "[5/6] Creating .env file template..."
cat > $APP_DIR/.env.template << 'EOF'
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# Database
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=erp_db
DATABASE_USER=erp_user
DATABASE_PASSWORD=your_secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Django Settings
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
USE_I18N=True
USE_L10N=True

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_SECURITY_POLICY=True
EOF

echo "✓ .env template created"
echo ""

echo "[6/6] Creating deployment script..."
cat > $APP_DIR/deploy.sh << 'EOF'
#!/bin/bash
set -e

cd /var/www/erp
source venv/bin/activate

echo "Pulling latest code..."
git pull origin main || echo "Git pull skipped"

echo "Installing dependencies..."
pip install -r requirements.txt 2>/dev/null || echo "Requirements already installed"

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting services..."
sudo systemctl restart gunicorn
sudo systemctl restart celery 2>/dev/null || echo "Celery not yet configured"

echo "✓ Deployment completed!"
EOF

chmod +x $APP_DIR/deploy.sh

echo "=================================="
echo "✓ Application Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Copy .env file: cp $APP_DIR/.env.template $APP_DIR/.env"
echo "2. Update .env with your credentials"
echo "3. Run migrations: cd $APP_DIR && source venv/bin/activate && python manage.py migrate"
echo "4. Create superuser: python manage.py createsuperuser"
echo "5. Run web server setup"
echo ""
