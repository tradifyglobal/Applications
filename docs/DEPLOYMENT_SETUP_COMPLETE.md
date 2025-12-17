# GitHub Actions Deployment Setup - Complete Guide

## 📋 Overview

You now have a fully automated GitHub Actions workflow that will:

1. **Validate Configuration** - Check all prerequisites
2. **Deploy to Dev Server** - Install all system and Python dependencies
3. **Configure Environment** - Set up .env and repository
4. **Generate Documentation** - Create deployment checklists and summaries

## 🎯 Quick Summary

| Component | Details |
|-----------|---------|
| **Dev Server** | 192.168.6.128 |
| **Username** | zubair |
| **SSH Method** | Public Key Authentication (already configured) |
| **Workflow Name** | Deploy Prerequisites to Dev Server |
| **Trigger** | Manual or automatic on file changes |
| **Deployment Path** | ~/erp-deployment |

## 📚 Documentation Files Created

- **`.github/workflows/deploy-prerequisites.yml`** - The GitHub Actions workflow
- **`docs/GITHUB_ACTIONS_DEPLOYMENT.md`** - Complete detailed guide
- **`docs/QUICK_DEPLOYMENT_START.md`** - 5-minute quick start
- **`ENVIRONMENTS.md`** - Multi-environment configuration guide

## ✅ Step-by-Step Setup Instructions

### Step 1: Configure GitHub Secrets (CRITICAL)

**Location**: https://github.com/tradifyglobal/Applications/settings/secrets/actions

1. Click **New repository secret** for each:

#### Secret 1: `DEV_APP_SERVER_IP`
- **Value**: `192.168.6.128`
- Click **Add secret**

#### Secret 2: `DEV_APP_SERVER_USER`
- **Value**: `zubair`
- Click **Add secret**

#### Secret 3: `DEV_APP_SERVER_PORT`
- **Value**: `22`
- Click **Add secret**

#### Secret 4: `DEV_SSH_PRIVATE_KEY` (IMPORTANT!)
- Get your SSH private key:
  ```powershell
  # Windows PowerShell
  cat ~/.ssh/id_rsa
  ```
- Copy the **entire** content including:
  ```
  -----BEGIN RSA PRIVATE KEY-----
  MIIEpAIBAAKCAQEA...
  ...
  -----END RSA PRIVATE KEY-----
  ```
- Paste into the secret field
- Click **Add secret**

### Verification
After adding all secrets, visit: https://github.com/tradifyglobal/Applications/settings/secrets/actions

You should see all 4 secrets listed (values hidden):
- ✅ DEV_APP_SERVER_IP
- ✅ DEV_APP_SERVER_USER  
- ✅ DEV_APP_SERVER_PORT
- ✅ DEV_SSH_PRIVATE_KEY

## 🚀 Triggering the Deployment

### Method 1: Manual Trigger (Recommended for First Deployment)

1. Go to: **https://github.com/tradifyglobal/Applications**
2. Click **Actions** tab
3. Click **Deploy Prerequisites to Dev Server** (left sidebar)
4. Click **Run workflow** button (blue button)
5. Select environment dropdown: `development`
6. Click **Run workflow** button
7. Watch the workflow execute!

### Method 2: Automatic Trigger

The workflow automatically runs when:
- You modify `requirements.txt`
- You update deployment scripts in `scripts/`
- You modify `.github/workflows/deploy-prerequisites.yml`
- Changes are pushed to `main` branch

### Method 3: Command Line (if you have GitHub CLI)

```bash
gh workflow run deploy-prerequisites.yml -f environment=development
```

## 📊 Monitoring Deployment Progress

### Real-Time Monitoring

1. After clicking "Run workflow", GitHub shows the workflow starting
2. Click on the workflow run to see detailed progress
3. Click on **Deploy Prerequisites** job to expand
4. Scroll down to see real-time command output

### Key Milestones to Watch For

```
✅ Validate Configuration
   - "All secrets configured"

✅ Deploy Prerequisites
   ├─ "SSH connection successful"
   ├─ "System dependencies installed"
   ├─ "Virtual environment created"
   ├─ "Python dependencies installed"
   ├─ "Django version: (4, 2, 7)"
   ├─ "Environment configuration created"
   ├─ "Repository cloned/updated"
   └─ "Prerequisites deployment completed successfully"
```

### Typical Execution Time

- First run: **8-12 minutes** (includes dependency downloads)
- Subsequent runs: **3-5 minutes** (uses cache where possible)

## 🔍 What Gets Installed

After successful workflow execution on your dev server:

### System Packages
```
✓ python3-pip
✓ python3-venv
✓ python3-dev
✓ build-essential
✓ libpq-dev (PostgreSQL development)
✓ postgresql-client
✓ git
✓ curl, wget, nano, htop
```

### Python Virtual Environment
```
Location: ~/erp-deployment/venv
Size: ~500MB
Contains: Django, DRF, Celery, and 50+ packages
```

### Django Application
```
Repository: Cloned from GitHub
Path: ~/erp-deployment
Apps: 24 ERP modules (Accounting, HR, Inventory, etc.)
```

## 📁 Directory Structure on Dev Server

After deployment, your dev server will have:

```
/home/zubair/
└── erp-deployment/
    ├── venv/                    # Python virtual environment
    │   ├── bin/
    │   │   ├── python
    │   │   ├── pip
    │   │   ├── django-admin
    │   │   └── gunicorn
    │   └── lib/
    ├── apps/                    # 24 Django applications
    ├── core/                    # Django core settings
    ├── scripts/                 # Deployment scripts
    ├── docs/                    # Documentation
    ├── manage.py               # Django management command
    ├── requirements.txt        # Python dependencies
    ├── .env                    # Environment configuration
    ├── DEPLOYMENT_CHECKLIST.md # Next steps
    └── DEPLOYMENT_SUMMARY.txt  # Deployment report
```

## 🔧 What to Do After Deployment

### 1. SSH into Dev Server

```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.128
```

### 2. Activate Virtual Environment

```bash
cd ~/erp-deployment
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### 3. Verify Installation

```bash
# Check Python
python --version          # Should show 3.x.x

# Check Django
django-admin --version   # Should show 4.2.7

# Check packages
pip list | head           # Show installed packages
```

### 4. Configure Database

Edit the `.env` file with your database credentials:

```bash
nano .env
```

Example configuration:
```
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-dev-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_dev_db
DB_USER=erp_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Initialize Database

```bash
# Check Django setup
python manage.py check

# Run migrations
export ENVIRONMENT=development
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Test Application

```bash
# Development server
python manage.py runserver 0.0.0.0:8000
```

Visit: `http://192.168.6.128:8000/admin/`

## 🆘 Troubleshooting

### Problem: "Permission denied (publickey)" Error

**Cause**: SSH key not properly configured

**Solution**:
```bash
# Verify SSH key exists on your machine
cat ~/.ssh/id_rsa

# If not, generate new key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""

# Re-add to GitHub secret:
# Copy entire key content and update DEV_SSH_PRIVATE_KEY secret
```

### Problem: Workflow Status Shows "Secret Not Found"

**Cause**: One or more secrets not configured

**Solution**:
1. Go to: https://github.com/tradifyglobal/Applications/settings/secrets/actions
2. Verify all 4 secrets exist:
   - DEV_APP_SERVER_IP
   - DEV_APP_SERVER_USER
   - DEV_APP_SERVER_PORT
   - DEV_SSH_PRIVATE_KEY
3. Re-add any missing secrets

### Problem: "pip: command not found"

**Cause**: Virtual environment not activated

**Solution**:
```bash
cd ~/erp-deployment
source venv/bin/activate
# Now try: pip list
```

### Problem: "psql: could not connect to server"

**Cause**: PostgreSQL not running or not installed

**Solution**:
```bash
# Check if PostgreSQL is installed
sudo apt list --installed | grep postgres

# If not installed, install it
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql  # Auto-start on boot

# Verify connection
psql -U postgres -c "SELECT version();"
```

### Problem: "django-admin command not found"

**Cause**: Virtual environment not activated or Django not installed

**Solution**:
```bash
cd ~/erp-deployment
source venv/bin/activate
python -m django --version   # Should show 4.2.7
```

## 📈 Advanced: Running in Production Mode

Once database is configured, you can start with production-like setup:

```bash
cd ~/erp-deployment
source venv/bin/activate
export ENVIRONMENT=development

# Start with Gunicorn (production WSGI server)
gunicorn core.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class sync \
  --log-level info
```

## 🔄 Re-running the Workflow

You can safely re-run the workflow multiple times:

1. All steps are **idempotent** (safe to repeat)
2. Existing files are **preserved**
3. New dependencies are **installed**
4. Configuration is **updated**

### Re-run Steps:
1. Go to Actions tab
2. Click on the previous workflow run
3. Click **Re-run all jobs** button
4. Wait for completion

## 📝 Useful Commands on Dev Server

```bash
# SSH in
ssh -i ~/.ssh/id_rsa zubair@192.168.6.128

# Navigate to app
cd ~/erp-deployment
source venv/bin/activate

# Run Django management commands
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000

# Check logs
tail -f ~/erp-deployment/logs/erp.log

# View environment variables
cat .env

# Check PostgreSQL
psql -U erp_user -d erp_dev_db -c "\dt"

# Stop app
pkill -f "python manage.py runserver"
```

## ✨ Next Steps

After successful deployment:

1. ✅ Configure secrets in GitHub (Step 1)
2. ✅ Trigger workflow manually (Step 2)
3. ✅ Monitor execution (Step 3)
4. ✅ SSH into dev server (Step 4)
5. ✅ Configure database credentials (Step 5)
6. ✅ Run migrations (Step 6)
7. ✅ Create superuser (Step 7)
8. ✅ Access application at http://192.168.6.128:8000

## 📚 Documentation Links

- **Full GitHub Actions Guide**: `docs/GITHUB_ACTIONS_DEPLOYMENT.md`
- **Quick Start**: `docs/QUICK_DEPLOYMENT_START.md`
- **Environment Setup**: `ENVIRONMENTS.md`
- **Deployment Guide**: `docs/DEPLOYMENT_GUIDE.md`

## 🎓 Learning Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets Guide](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## 💡 Pro Tips

1. **Keep SSH key secure** - Never commit it to repository
2. **Test locally first** - Run `python manage.py check` before deploying
3. **Review logs carefully** - Each step provides useful debugging info
4. **Use development environment** - Less strict security for easier debugging
5. **Backup database regularly** - Before major changes

## 🆘 Getting Help

If deployment fails:

1. **Check GitHub Actions logs** - Scroll to the error message
2. **Verify SSH connection** - `ssh -i ~/.ssh/id_rsa zubair@192.168.6.128`
3. **Check server resources** - `free -h` and `df -h` on dev server
4. **Review error messages** - They usually indicate the exact issue

---

**Status**: ✅ Ready for deployment

**Last Updated**: December 17, 2025

**Workflow Repository**: https://github.com/tradifyglobal/Applications
