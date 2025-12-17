# GitHub Actions Deployment Guide

## Overview

This guide explains how to set up GitHub Actions to automatically deploy prerequisites to your development app server using SSH public key authentication.

## Prerequisites

✅ Dev app server (192.168.6.128) with SSH public key authentication configured  
✅ GitHub repository with the ERP code pushed  
✅ SSH private key for authentication

## Step 1: Configure GitHub Secrets

GitHub Actions requires secrets to be configured in your repository to authenticate with the dev server.

### Setting up GitHub Secrets

1. Go to your GitHub repository: `https://github.com/tradifyglobal/Applications`
2. Click on **Settings** tab
3. Click on **Secrets and variables** → **Actions** in the left sidebar
4. Click **New repository secret**

### Required Secrets to Add

Create the following secrets:

#### 1. `DEV_APP_SERVER_IP`
- **Value**: `192.168.6.128`
- Click "Add secret"

#### 2. `DEV_APP_SERVER_USER`
- **Value**: `zubair`
- Click "Add secret"

#### 3. `DEV_APP_SERVER_PORT`
- **Value**: `22`
- Click "Add secret"

#### 4. `DEV_SSH_PRIVATE_KEY`
- **Value**: Your SSH private key (entire content)
- **How to get your private key**:
  ```powershell
  # Windows PowerShell
  cat ~/.ssh/id_rsa
  
  # Copy the entire content including:
  # -----BEGIN RSA PRIVATE KEY-----
  # ... key content ...
  # -----END RSA PRIVATE KEY-----
  ```
- Paste the entire key content into this secret
- Click "Add secret"

### Verify Secrets are Added

After adding all 4 secrets, you should see:
- ✅ DEV_APP_SERVER_IP
- ✅ DEV_APP_SERVER_USER
- ✅ DEV_APP_SERVER_PORT
- ✅ DEV_SSH_PRIVATE_KEY

## Step 2: Understand the Deployment Workflow

The `deploy-prerequisites.yml` workflow performs these steps:

### 1. **Validate Configuration**
   - Checks that all required secrets are configured
   - Validates requirements.txt exists

### 2. **Setup SSH Connection**
   - Configures SSH with the private key
   - Adds server to known_hosts

### 3. **Test Connection**
   - Verifies SSH connection is working

### 4. **Check System Requirements**
   - Checks OS, CPU, Memory
   - Verifies Python, pip, Git, Docker availability

### 5. **Deploy Files**
   - Copies requirements.txt
   - Copies deployment scripts
   - Copies .env.example

### 6. **Install System Dependencies**
   - Updates package manager
   - Installs Python development packages
   - Installs database clients
   - Installs utilities (Git, curl, etc.)

### 7. **Setup Python Environment**
   - Creates virtual environment
   - Upgrades pip and setuptools

### 8. **Install Python Dependencies**
   - Installs all packages from requirements.txt

### 9. **Configure Environment**
   - Creates .env file from .env.example
   - Sets development defaults

### 10. **Clone/Update Repository**
   - Clones or updates the application code

### 11. **Verify Installation**
   - Tests Django, DRF, Daphne, Celery imports

### 12. **Generate Deployment Documentation**
   - Creates DEPLOYMENT_CHECKLIST.md
   - Creates DEPLOYMENT_SUMMARY.txt

## Step 3: Trigger the Workflow

### Option A: Manual Trigger (Recommended for first deployment)

1. Go to **Actions** tab in your GitHub repository
2. Click **Deploy Prerequisites to Dev Server** workflow
3. Click **Run workflow** button
4. Select environment: `development`
5. Click **Run workflow**

### Option B: Automatic Trigger

The workflow runs automatically when:
- `requirements.txt` is updated
- Deployment scripts are modified
- The workflow file itself is updated
- Pushed to `main` branch

### Option C: Using GitHub CLI

```bash
gh workflow run deploy-prerequisites.yml -f environment=development
```

## Step 4: Monitor Workflow Execution

### Watch Deployment Progress

1. Go to **Actions** tab
2. Click the running workflow
3. Click the **Deploy Prerequisites** job
4. Watch the real-time output

### Key Checkpoints to Monitor

- ✅ "SSH configured"
- ✅ "SSH connection successful"
- ✅ "System dependencies installed"
- ✅ "Virtual environment created"
- ✅ "Python dependencies installed"
- ✅ "Django version: (4, 2, 7)"
- ✅ "Prerequisites deployment completed successfully"

## Step 5: What's Installed on Dev Server

After successful deployment, the dev server will have:

```
~/erp-deployment/
├── venv/                          # Python virtual environment
│   ├── bin/
│   │   ├── python                 # Python interpreter
│   │   ├── pip                    # Package manager
│   │   ├── django-admin           # Django admin command
│   │   └── gunicorn              # WSGI server
│   ├── lib/python3.x/site-packages/  # All packages
│   └── include/
├── scripts/                       # Deployment scripts
├── requirements.txt               # Python dependencies
├── .env                          # Environment configuration
├── DEPLOYMENT_CHECKLIST.md       # Next steps checklist
└── DEPLOYMENT_SUMMARY.txt        # Deployment summary
```

## Step 6: Manual Setup on Dev Server

After GitHub Actions completes, complete these manual steps:

### SSH into Dev Server

```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.128
```

### Navigate to Deployment Directory

```bash
cd ~/erp-deployment
source venv/bin/activate
```

### Update Database Configuration

```bash
nano .env
```

Configure these variables:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_dev_db
DB_USER=erp_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Initialize Database

```bash
export ENVIRONMENT=development
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts to create admin user
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Test Django Installation

```bash
python manage.py check
```

## Step 7: Running the Application

### Development Server (for testing)

```bash
cd ~/erp-deployment
source venv/bin/activate
export ENVIRONMENT=development
python manage.py runserver 0.0.0.0:8000
```

Visit: `http://192.168.6.128:8000`

### Production Server (with Gunicorn)

```bash
cd ~/erp-deployment
source venv/bin/activate
export ENVIRONMENT=development
gunicorn core.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --log-level info
```

## Troubleshooting

### Workflow Fails - SSH Connection Error

**Problem**: "Permission denied (publickey)"

**Solution**:
```bash
# Verify SSH key is correct
cat ~/.ssh/id_rsa

# Copy entire key (including BEGIN and END lines)
# Re-add DEV_SSH_PRIVATE_KEY secret with full key content
```

### Secret Not Found Error

**Problem**: "env.SSH_PRIVATE_KEY is not defined"

**Solution**:
- Go to Settings → Secrets and variables → Actions
- Verify all 4 secrets exist:
  - DEV_APP_SERVER_IP
  - DEV_APP_SERVER_USER
  - DEV_APP_SERVER_PORT
  - DEV_SSH_PRIVATE_KEY

### Virtual Environment Not Activating

**Problem**: Command not found after activation

**Solution**:
```bash
# Ensure you're in the right directory
cd ~/erp-deployment

# Try full path to python
./venv/bin/python --version

# Try activating with full path
source ./venv/bin/activate
```

### Database Connection Failed

**Problem**: "could not connect to server"

**Solution**:
```bash
# Ensure database is running
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql

# Test connection
psql -U erp_user -d erp_dev_db -h localhost -p 5432
```

## Advanced: Modifying Workflow

### Add Custom Post-Deployment Scripts

Edit `.github/workflows/deploy-prerequisites.yml` and add a new step:

```yaml
- name: Run Custom Setup
  run: |
    ssh -p ${{ env.APP_SERVER_PORT }} ${{ env.APP_SERVER_USER }}@${{ env.APP_SERVER_IP }} << 'EOF'
    cd ~/erp-deployment
    source venv/bin/activate
    # Your custom commands here
    EOF
```

### Create Different Workflows for Staging/Production

Copy the workflow and modify:
1. Change `name` to "Deploy Prerequisites to Staging"
2. Change secrets prefix: `DEV_` → `STAGING_`
3. Update conditions and inputs

## Next Steps

1. ✅ Configure GitHub secrets (Step 1)
2. ✅ Trigger workflow manually (Step 3)
3. ✅ Monitor execution (Step 4)
4. ✅ Complete manual setup (Step 6)
5. ✅ Run the application (Step 7)

## Useful Commands

### View Workflow Status
```bash
gh workflow view deploy-prerequisites.yml
```

### List All Workflow Runs
```bash
gh run list --workflow deploy-prerequisites.yml
```

### View Specific Run Details
```bash
gh run view <run-id>
```

### Cancel Running Workflow
```bash
gh run cancel <run-id>
```

## Support & Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Django Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
