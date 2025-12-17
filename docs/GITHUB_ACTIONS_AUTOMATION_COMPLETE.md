# GitHub Actions Deployment - Complete Automation Guide

> **Version 2.0 - Fully Automated GitHub Actions Deployment**  
> Last Updated: January 2024  
> Status: ✅ COMPLETE - All deployment via GitHub Actions (NO MANUAL SSH)

## 📌 Overview

This guide covers **100% automated deployment** using GitHub Actions workflows. All deployment tasks run through GitHub Actions - no direct SSH access required for deployment.

### Available Workflows

| Workflow | Purpose | Trigger | Manual |
|----------|---------|---------|--------|
| **setup-database-server** | Install PostgreSQL & configure database | Manual | ✅ Yes |
| **run-database-migrations** | Apply Django migrations to database | On push to migrations | ✅ Yes |
| **create-superuser** | Create Django admin superuser | Manual | ✅ Yes |
| **deploy-prerequisites** | Install prerequisites on app server | Manual | ✅ Yes |
| **full-deployment** | Orchestrate all deployment steps | Manual | ✅ Yes |

---

## 🔑 GitHub Secrets Configuration

Before running any workflows, configure these secrets in GitHub repository settings:

### App Server Secrets
```
DEV_APP_SERVER_IP: 192.168.6.128
DEV_APP_SERVER_USER: zubair
DEV_APP_SERVER_PORT: 22
DEV_SSH_PRIVATE_KEY: [Your SSH Private Key]
```

### Database Server Secrets
```
DB_SERVER_IP: 192.168.6.129
DB_SERVER_USER: zubair
DB_SERVER_PORT: 22
DB_SSH_PRIVATE_KEY: [Your SSH Private Key]
```

### How to add secrets:
1. Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Enter name and value
4. Click **Add secret**

---

## 🚀 Quick Start - Full Deployment

For complete automated deployment:

1. **Go to GitHub Actions**
   - Navigate to your repository on GitHub
   - Click **Actions** tab
   - Find **Full Application Deployment** workflow

2. **Run the workflow**
   - Click **Run workflow**
   - Select environment (development/staging/production)
   - Choose deployment options:
     - ☑ Setup Database Server (if first time)
     - ☑ Run Migrations (usually yes)
     - ☑ Create Superuser (if needed)
     - ☑ Deploy App Server (usually yes)
   - Click **Run workflow**

3. **Monitor deployment**
   - Watch the workflow progress in real-time
   - Check each job for logs
   - Fix any issues shown in logs

---

## 📋 Individual Workflow Usage

### 1️⃣ Setup Database Server

**When to use:** First deployment or database reset

**Steps:**
1. Go to **Actions** → **Setup Database Server**
2. Click **Run workflow**
3. Select environment
4. Set database password
5. Click **Run workflow**
6. Wait for completion (~5 minutes)

**What it does:**
- Installs PostgreSQL
- Creates database user `erp_user`
- Creates database `erp_dev_db`
- Configures remote access
- Enables PostgreSQL service

**Output:**
- PostgreSQL installed ✅
- Database user created ✅
- Database configured ✅
- Remote connections allowed ✅

---

### 2️⃣ Run Database Migrations

**When to use:** After code changes with migrations or after database setup

**Steps:**
1. Go to **Actions** → **Run Database Migrations**
2. Click **Run workflow**
3. Select environment
4. Click **Run workflow**
5. Wait for completion (~2 minutes)

**What it does:**
- Connects to app server via SSH
- Packages Django project files
- Transfers to app server
- Runs `python manage.py migrate`
- Verifies migrations applied

**Output:**
- Migrations applied ✅
- All tables created ✅
- Database ready ✅

---

### 3️⃣ Create Django Superuser

**When to use:** To create admin user or additional superusers

**Steps:**
1. Go to **Actions** → **Create Django Superuser**
2. Click **Run workflow**
3. Enter configuration:
   - Environment: development/staging/production
   - Username: admin (or other username)
   - Email: admin@company.com
   - Password: (leave empty for auto-generated or enter custom)
4. Click **Run workflow**
5. Wait for completion (~2 minutes)

**What it does:**
- Connects to app server
- Creates Django superuser
- Sets password
- Verifies creation
- Logs superuser details

**Output:**
- Superuser created ✅
- Login credentials confirmed ✅
- Ready for admin access ✅

---

### 4️⃣ Deploy Prerequisites

**When to use:** Deploy app server dependencies and configuration

**Steps:**
1. Go to **Actions** → **Deploy Prerequisites**
2. Click **Run workflow**
3. Select environment
4. Click **Run workflow**
5. Wait for completion (~10 minutes)

**What it does:**
- Installs system packages
- Sets up Python environment
- Creates virtual environment
- Installs Python dependencies
- Configures Gunicorn/Daphne
- Enables services

**Output:**
- System packages installed ✅
- Python environment ready ✅
- Dependencies installed ✅
- Services configured ✅

---

## 🎯 Complete Deployment Sequence

### First-Time Deployment (Development)

```
Step 1: Setup Database Server (5 min)
   ↓
Step 2: Deploy Prerequisites (10 min)
   ↓
Step 3: Run Migrations (2 min)
   ↓
Step 4: Create Superuser (2 min)
   ↓
✅ DEPLOYMENT COMPLETE (19 minutes total)
```

### Code Update Deployment

```
Step 1: Deploy Prerequisites (pulls latest code) (5 min)
   ↓
Step 2: Run Migrations (if needed) (2 min)
   ↓
✅ DEPLOYMENT COMPLETE (7 minutes total)
```

---

## 📊 Workflow Status & Logs

### Viewing Workflow Status

1. Go to **Actions** tab
2. Select workflow from list
3. Click on the run you want to view
4. See summary and status of each job
5. Click on job to expand logs

### Understanding Status Colors

- 🟢 **Green**: Workflow completed successfully
- 🔴 **Red**: Workflow failed
- 🟡 **Yellow**: Workflow in progress
- ⚫ **Gray**: Workflow cancelled or skipped

### Checking Logs

1. Click failed job to expand
2. Find the failing step
3. Click step to see error message
4. Fix issue and re-run workflow

---

## 🔍 Troubleshooting

### SSH Connection Failed

**Error:** `Permission denied (publickey)`

**Fix:**
1. Verify SSH private key is correctly pasted in `DEV_SSH_PRIVATE_KEY` secret
2. Ensure public key is on server at `~/.ssh/authorized_keys`
3. Test SSH locally: `ssh -i ~/.ssh/id_rsa zubair@192.168.6.128`

### Database Connection Failed

**Error:** `FATAL: remaining connection slots reserved for non-replication superuser connections`

**Fix:**
1. Increase PostgreSQL max_connections
2. On database server:
   ```bash
   sudo -u postgres psql -c "ALTER SYSTEM SET max_connections = 200;"
   sudo systemctl restart postgresql
   ```

### Migrations Failed

**Error:** `ModuleNotFoundError: No module named 'django'`

**Fix:**
1. Ensure requirements.txt is in repository root
2. Verify all dependencies are listed
3. Re-run workflow with force reinstall

### Superuser Creation Failed

**Error:** `User already exists`

**Fix:**
1. Use different username, OR
2. Delete existing user from admin panel, OR
3. Manually update password:
   ```python
   python manage.py shell
   from django.contrib.auth.models import User
   u = User.objects.get(username='admin')
   u.set_password('newpassword')
   u.save()
   ```

---

## 🔐 Security Best Practices

### SSH Key Management

✅ **DO:**
- Store SSH private key in GitHub Secrets
- Use separate keys for different environments
- Rotate keys periodically
- Use strong passphrases
- Restrict key file permissions (600)

❌ **DON'T:**
- Commit private keys to repository
- Share private keys between team members
- Use same key for multiple purposes
- Store keys in plaintext files
- Hardcode credentials in workflows

### GitHub Secrets Management

✅ **DO:**
- Use unique names for secrets
- Rotate passwords regularly
- Use strong passwords (20+ chars)
- Document what each secret is for
- Review secret access logs

❌ **DON'T:**
- Use simple/weak passwords
- Share secrets outside GitHub
- Reuse secrets from other projects
- Log or print secrets
- Commit example secrets with real values

---

## 📈 Monitoring & Maintenance

### After Each Deployment

1. ✅ Verify application is running
2. ✅ Check Django admin loads (`/admin`)
3. ✅ Test API endpoints
4. ✅ Monitor server logs for errors
5. ✅ Check database connections
6. ✅ Verify static files are served

### Regular Maintenance Tasks

**Daily:**
- Check GitHub Actions for failed runs
- Monitor server performance metrics
- Review error logs

**Weekly:**
- Update dependencies
- Review database backups
- Check disk space usage

**Monthly:**
- Rotate SSH keys
- Review security logs
- Update documentation

---

## 📚 Additional Resources

| Resource | Location | Purpose |
|----------|----------|---------|
| Settings Guide | `ENVIRONMENTS.md` | Environment configuration |
| Troubleshooting | `docs/DEPLOYMENT_SETUP_COMPLETE.md` | Detailed troubleshooting |
| API Docs | `README/06-API_DOCUMENTATION.md` | API reference |
| Checklist | `POST_DEPLOYMENT_CHECKLIST.md` | Post-deployment verification |

---

## ✨ Summary

With this GitHub Actions setup:

- ✅ **No manual SSH required** for deployment
- ✅ **Fully automated** database and app setup
- ✅ **Consistent deployments** every time
- ✅ **Complete audit trail** of all deployments
- ✅ **Easy rollback** if needed
- ✅ **Team visibility** of deployment progress
- ✅ **Repeatable process** for all environments

---

## 🆘 Support

For issues or questions:
1. Check the logs in GitHub Actions
2. Review troubleshooting section above
3. Check infrastructure status: `INFRASTRUCTURE_STATUS.txt`
4. Review deployment documentation: `docs/`
5. Contact DevOps team

**Last Updated:** January 2024  
**Next Review:** March 2024
