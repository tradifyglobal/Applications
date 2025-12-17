# GitHub Actions Deployment - Quick Start

**Complete automation guide - Everything via GitHub Actions!**

## Available Workflows

- setup-database-server.yml: Install PostgreSQL & database
- run-database-migrations.yml: Apply Django migrations
- create-superuser.yml: Create admin user
- deploy-prerequisites.yml: Deploy app server
- full-deployment.yml: Complete orchestration

---

## First-Time Setup (5 minutes)

### 1. Configure GitHub Secrets

Go to Settings → Secrets and variables → Actions → New repository secret

**Add these secrets:**

| Secret Name | Value |
|------------|-------|
| DEV_APP_SERVER_IP | 192.168.6.128 |
| DEV_APP_SERVER_USER | zubair |
| DEV_APP_SERVER_PORT | 22 |
| DEV_SSH_PRIVATE_KEY | [Your private SSH key] |
| DB_SERVER_IP | 192.168.6.129 |
| DB_SERVER_USER | zubair |
| DB_SERVER_PORT | 22 |
| DB_SSH_PRIVATE_KEY | [Your private SSH key] |

### 2. Get Your SSH Private Key

On your local machine:

```bash
cat ~/.ssh/id_rsa
```

Copy the entire content (including headers/footers)

---

## Deploy Now - Full Automated

1. Go to **Actions** tab
2. Select **Full Application Deployment**
3. Click **Run workflow**
4. Choose deployment options:
   - Deploy Database Server (first time only)
   - Run Migrations (yes)
   - Create Superuser (yes)
   - Deploy App Server (yes)
5. Click **Run workflow**
6. Wait for completion (15-20 minutes)

---

## Deploy Step-by-Step

**Step 1: Setup Database**
- Actions → Setup Database Server → Run workflow

**Step 2: Deploy App Server**
- Actions → Deploy Prerequisites → Run workflow

**Step 3: Run Migrations**
- Actions → Run Database Migrations → Run workflow

**Step 4: Create Admin**
- Actions → Create Django Superuser → Run workflow

---

## Monitor Deployment

1. Go to **Actions** tab
2. Click running workflow
3. Watch progress in real-time
4. Green = Success, Red = Failed
5. Click job to expand logs

---

## Workflow Details

### Setup Database Server

- Time: 5-10 minutes
- Installs: PostgreSQL, creates user, creates database
- Run when: First deployment or database reset

### Deploy Prerequisites

- Time: 5-10 minutes
- Installs: Python packages, Gunicorn, Daphne
- Run when: New deployment or code updates

### Run Database Migrations

- Time: 2-5 minutes
- Runs: python manage.py migrate
- Run when: New migrations in code

### Create Django Superuser

- Time: 1-2 minutes
- Creates: Admin user with credentials
- Run when: Need admin user

---

## Post-Deployment

After successful deployment:

1. Access your app: http://192.168.6.128
2. Access Django Admin: http://192.168.6.128/admin
3. Login with superuser credentials
4. API endpoints available at /api/v1/

---

## Troubleshooting

### Workflow Failed?

1. Click the failed workflow run
2. Find the red X next to failed step
3. Click the step to see error message
4. Fix the issue and try again

### Common Issues

| Error | Solution |
|-------|----------|
| Permission denied (publickey) | SSH key not correct, paste it again |
| Connection refused | Server IP/port wrong in GitHub secrets |
| ModuleNotFoundError: django | Requirements.txt missing or incomplete |
| psql: command not found | PostgreSQL not installed yet - run setup first |

### Check Server Status

```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.128
ps aux | grep python
tail -f logs/django.log
```

---

## Post-Deployment Checklist

- [ ] Application loads at http://192.168.6.128
- [ ] Admin panel loads at http://192.168.6.128/admin
- [ ] Can login with superuser
- [ ] Database tables exist
- [ ] Logs show no errors
- [ ] API endpoints respond

---

## Security Reminders

**Good practices:**
- Store SSH keys in GitHub Secrets only
- Use strong passwords for superuser
- Rotate SSH keys every 90 days
- Review logs for suspicious activity

**Never do this:**
- Commit private keys to repository
- Hardcode passwords in workflows
- Share SSH keys with team
- Store secrets in .env file in repo

---

## More Help

- Detailed Guide: docs/GITHUB_ACTIONS_AUTOMATION_COMPLETE.md
- Full Setup: docs/GITHUB_ACTIONS_DEPLOYMENT.md
- Troubleshooting: docs/DEPLOYMENT_SETUP_COMPLETE.md
- Infrastructure: INFRASTRUCTURE_STATUS.txt

---

**Ready to deploy? Go to Actions tab and click "Full Application Deployment"!**

Last Updated: January 2024
Status: All automation ready
