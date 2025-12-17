# Quick Start: GitHub Actions Deployment

## ⚡ 5-Minute Setup

### Step 1: Add GitHub Secrets (2 min)
Go to: https://github.com/tradifyglobal/Applications/settings/secrets/actions

Add these 4 secrets:
| Secret Name | Value |
|-------------|-------|
| `DEV_APP_SERVER_IP` | `192.168.6.128` |
| `DEV_APP_SERVER_USER` | `zubair` |
| `DEV_APP_SERVER_PORT` | `22` |
| `DEV_SSH_PRIVATE_KEY` | (Your full SSH private key) |

### Step 2: Trigger Deployment (1 min)
1. Go to: Actions → Deploy Prerequisites to Dev Server
2. Click "Run workflow"
3. Click "Run workflow" button

### Step 3: Monitor (2 min)
Watch the workflow run in real-time. Look for ✅ checkmarks.

## 📊 What Gets Installed

After workflow completes on `192.168.6.128`:

```
✅ System Packages          (Python, build tools, database clients)
✅ Python Virtual Env       (~/erp-deployment/venv)
✅ Django 4.2.7            (Web framework)
✅ Django REST Framework   (API framework)
✅ PostgreSQL Client       (Database tools)
✅ All Dependencies        (from requirements.txt)
✅ Environment Config      (.env file)
✅ Source Code             (Cloned from GitHub)
```

## 🚀 Next Steps After Workflow

SSH into your dev server:
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.128
cd ~/erp-deployment
source venv/bin/activate
```

Configure database and run migrations:
```bash
# Edit .env with your database settings
nano .env

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver 0.0.0.0:8000
```

Visit: `http://192.168.6.128:8000`

## 🔍 Check Workflow Logs

If something fails:
1. Go to Actions tab
2. Click the failed workflow
3. Scroll down to see error messages
4. Common issues:
   - SSH key format incorrect
   - Secrets not configured
   - Server connectivity issues

## 📁 Files on Dev Server

After deployment:
```
~/erp-deployment/
├── venv/                    # Python environment (4 GB+)
├── apps/                    # Django apps
├── core/                    # Django config
├── scripts/                 # Setup scripts
├── manage.py               # Django management
├── requirements.txt        # Python packages
├── .env                    # Configuration
├── DEPLOYMENT_CHECKLIST.md # Next steps
└── DEPLOYMENT_SUMMARY.txt  # Summary report
```

## ⚙️ Environment Variables

Development defaults in `~/.erp-deployment/.env`:
```
ENVIRONMENT=development
DEBUG=True
DB_NAME=erp_dev_db
DB_HOST=localhost
DB_PORT=5432
```

## 🆘 Troubleshooting Quick Fixes

| Error | Fix |
|-------|-----|
| SSH Permission Denied | Re-add SSH private key to `DEV_SSH_PRIVATE_KEY` secret |
| Secret Not Found | Go to Settings > Secrets > Actions, verify all 4 secrets |
| pip Not Found | Check virtual environment activation: `source venv/bin/activate` |
| Database Connection Failed | Check PostgreSQL is running on dev server |
| Django Commands Not Found | Ensure in correct directory: `cd ~/erp-deployment` |

## 📞 Support

Full documentation: `docs/GITHUB_ACTIONS_DEPLOYMENT.md`

## ✨ Done!

Your dev server is now ready for development. The workflow:
- ✅ Can be re-run anytime
- ✅ Is idempotent (safe to run multiple times)
- ✅ Creates detailed logs
- ✅ Generates checklist for next steps
