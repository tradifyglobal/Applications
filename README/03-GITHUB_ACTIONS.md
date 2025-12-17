# GitHub Actions CI/CD Setup

This guide explains how to configure GitHub Actions for automated testing and deployment of the ERP system.

## Overview

GitHub Actions automates:
1. **Testing** - Runs unit/integration tests on each push
2. **Building** - Creates Docker images
3. **Deployment** - Deploys to app server via SSH
4. **Verification** - Health checks after deployment

## Prerequisites

Before setting up GitHub Actions, ensure:

1. GitHub repository is created
2. SSH keys are generated (see `02-SSH_SETUP.md`)
3. GitHub Secrets are configured
4. Servers are accessible from GitHub Actions

## Step 1: Configure GitHub Secrets

GitHub Secrets are encrypted environment variables for your workflows.

### Access GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

### Add Required Secrets

| Secret Name | Description | Example |
|---|---|---|
| `SSH_PRIVATE_KEY` | Your SSH private key | `-----BEGIN RSA PRIVATE...` |
| `APP_SERVER_IP` | App server IP address | `203.0.113.45` |
| `APP_SERVER_USER` | SSH user for app server | `deploy` |
| `APP_SERVER_PORT` | SSH port | `22` |
| `DB_SERVER_IP` | Database server IP | `203.0.113.46` |
| `DB_SERVER_USER` | SSH user for DB server | `deploy` |

### How to Add Each Secret

#### 1. SSH_PRIVATE_KEY

```bash
# On your local machine
cat ~/.ssh/id_rsa
```

- Copy entire output (including BEGIN/END lines)
- In GitHub: Click "New repository secret"
- Name: `SSH_PRIVATE_KEY`
- Value: Paste the private key
- Click "Add secret"

#### 2. APP_SERVER_IP

- Name: `APP_SERVER_IP`
- Value: Your app server public IP
- Example: `203.0.113.45`

#### 3. APP_SERVER_USER

```bash
# Get the SSH user
ssh deploy@app-server-ip "whoami"
```

- Name: `APP_SERVER_USER`
- Value: Username returned above

#### 4. APP_SERVER_PORT

- Name: `APP_SERVER_PORT`
- Value: `22` (or your SSH port)

#### 5. DB_SERVER_IP

- Name: `DB_SERVER_IP`
- Value: Your database server public IP

#### 6. DB_SERVER_USER

- Name: `DB_SERVER_USER`
- Value: SSH user on DB server

## Step 2: Understand Workflow Files

Workflows are YAML files in `.github/workflows/` directory.

### File Structure

```yaml
name: Deploy HR Module                    # Workflow name

on:                                       # Trigger conditions
  push:
    branches: [ main, develop ]
    paths:
      - 'apps/hr/**'
  workflow_dispatch:

env:                                      # Environment variables
  APP_SERVER_IP: ${{ secrets.APP_SERVER_IP }}

jobs:                                     # Jobs to run
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Running tests"

  build:
    needs: test                           # Depends on test job
    steps:
      - run: echo "Building..."

  deploy:
    needs: build                          # Depends on build job
    steps:
      - run: echo "Deploying..."
```

## Step 3: Available Workflows

The system includes pre-configured workflows:

### 1. HR Module Workflow
**File**: `.github/workflows/deploy-hr.yml`

Triggers on:
- Push to `main` or `develop` branches
- Changes in `apps/hr/` or `core/`
- Manual trigger

Runs:
- Tests for HR module
- Builds Docker image
- Deploys to app server

### 2. Inventory Module Workflow
**File**: `.github/workflows/deploy-inventory.yml`

Similar to HR module but for inventory.

### 3. Full Application Workflow
**File**: `.github/workflows/deploy-full.yml`

Triggers on:
- Push to `main` branch
- Changes in `core/` or `requirements.txt`

Runs all tests and deploys entire application.

## Step 4: Understanding Workflow Execution

### Trigger Events

Workflows trigger on:

```yaml
on:
  push:
    branches: [ main, develop ]      # Push to these branches
    paths:                           # Only if these files changed
      - 'apps/hr/**'
      - 'core/**'
      - 'requirements.txt'
  workflow_dispatch:                 # Manual trigger from UI
```

### Job Dependencies

```yaml
jobs:
  test:                              # Step 1: Run tests
    runs-on: ubuntu-latest

  build:                             # Step 2: Build image
    needs: test                      # Wait for test to pass
    runs-on: ubuntu-latest

  deploy:                            # Step 3: Deploy
    needs: build                     # Wait for build to complete
    runs-on: ubuntu-latest
```

### Workflow Status

After pushing code, GitHub shows workflow status:

1. ✓ **Queued** - Waiting to run
2. ⟳ **In progress** - Running
3. ✓ **Success** - All jobs passed
4. ✗ **Failed** - One or more jobs failed

## Step 5: Monitor Workflow Execution

### View Workflow Runs

1. Go to GitHub repository
2. Click **Actions** tab
3. Select workflow from left sidebar
4. Click a run to see details

### View Job Logs

Click on any job to see:
- Step-by-step execution
- Console output
- Errors and warnings

### Enable Notifications

1. Go to GitHub Settings
2. Notifications → Actions
3. Configure email alerts for:
   - Workflow run failures
   - Deployment status

## Step 6: Test Workflow Manually

### Manual Workflow Trigger

```yaml
on:
  workflow_dispatch:                  # Enables manual trigger
```

To trigger manually:

1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Select branch
5. Click "Run workflow"

## Step 7: Customize Workflows

### Add a New Module Workflow

Create `.github/workflows/deploy-sales.yml`:

```yaml
name: Deploy Sales Module

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'apps/sales/**'
      - 'core/**'
      - 'requirements.txt'
  workflow_dispatch:

env:
  APP_SERVER_IP: ${{ secrets.APP_SERVER_IP }}
  APP_SERVER_USER: ${{ secrets.APP_SERVER_USER }}
  APP_SERVER_PORT: ${{ secrets.APP_SERVER_PORT }}
  SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}

jobs:
  test:
    runs-on: ubuntu-latest
    name: Test Sales Module
    
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: test_erp
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-django pytest-cov
      
      - name: Run tests
        env:
          DEBUG: False
          SECRET_KEY: test-secret-key
          DB_ENGINE: django.db.backends.postgresql
          DB_NAME: test_erp
          DB_USER: test_user
          DB_PASSWORD: test_pass
          DB_HOST: localhost
          DB_PORT: 5432
        run: |
          pytest apps/sales/ --cov=apps.sales --cov-report=xml
```

### Skip Deployment

Add `[skip deploy]` to commit message:

```bash
git commit -m "Update docs [skip deploy]"
```

## Step 8: Troubleshooting Workflows

### Common Workflow Failures

#### 1. SSH Connection Failed

**Error**:
```
Host key verification failed
```

**Solution**:
- Verify SSH private key in secrets
- Check `app_server_ip` is correct
- Ensure servers are accessible

#### 2. Docker Build Failed

**Error**:
```
failed to solve with frontend dockerfile.v0
```

**Solution**:
- Check Dockerfile syntax
- Verify requirements.txt
- Check Python version compatibility

#### 3. Tests Failed

**Error**:
```
FAILED apps/hr/tests.py::test_something
```

**Solution**:
- Fix failing tests in code
- Test locally: `pytest apps/hr/`
- Push fix to repository

#### 4. Database Connection Error

**Error**:
```
could not connect to server
```

**Solution**:
- Check DB connection string in .env
- Verify database service is running
- Check firewall rules

### Debug Workflow

Add debug logging:

```yaml
- name: Debug
  run: |
    echo "SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}"  # Don't do this!
    echo "APP_SERVER_IP: ${{ secrets.APP_SERVER_IP }}"
    ls -la ~/.ssh/
```

**Note**: Be careful with secrets! Don't output them.

### View Workflow Syntax

Check syntax without running:

```bash
# Install GitHub CLI
brew install gh

# Check workflow
gh workflow view .github/workflows/deploy-hr.yml
```

## Step 9: Advanced Configuration

### Matrix Build (Test Multiple Python Versions)

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']

steps:
  - uses: actions/setup-python@v4
    with:
      python-version: ${{ matrix.python-version }}
```

### Run Only on Certain Branches

```yaml
on:
  push:
    branches:
      - main
      - 'release/*'
      - '!draft'
```

### Scheduled Deployments

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

### Run Specific Job

```yaml
if: github.ref == 'refs/heads/main'
```

## Step 10: Security Best Practices

### 1. Rotate Secrets

Regularly rotate SSH keys:

1. Generate new key: `ssh-keygen -f ~/.ssh/id_rsa_new`
2. Add new key to servers
3. Update GitHub secret
4. Remove old key from servers

### 2. Limit Branch Access

Use branch protection rules:

1. Go to Settings → Branches
2. Add protection rule for `main`
3. Require status checks to pass
4. Require pull request reviews

### 3. Audit Workflow Access

```bash
# Check secrets usage in workflows
grep -r "secrets\." .github/workflows/
```

### 4. Use GitHub Environments

Create separate environments for staging/production:

1. Settings → Environments
2. Create `staging` and `production`
3. Set environment-specific secrets
4. Add approval requirements

### 5. Review Workflow Permissions

Settings → Actions → General:

- Allow actions from approved creators
- Limit workflow permissions (read-only)

## Step 11: Monitor and Maintain

### Weekly Maintenance

- Check workflow run history
- Review failed runs
- Update dependencies in requirements.txt

### Monthly Tasks

- Review GitHub Actions usage
- Audit secrets access
- Check for deprecated actions

### Security Audit

- Verify SSH key not exposed
- Check deployment logs
- Review code changes

## Integration with GitHub

### Pull Request Checks

Workflows run on pull requests (PR):

```yaml
on:
  pull_request:
    branches: [ main ]
```

Shows status in PR:
- ✓ Tests passed
- ✗ Tests failed
- ⟳ Running

## Next Steps

1. Configure all required secrets
2. Push a test commit to trigger workflow
3. Monitor first deployment in Actions tab
4. Adjust workflows as needed
5. Set up branch protection rules

## Useful Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Reference](https://docs.github.com/en/actions/learn-github-actions)
- [Docker GitHub Actions](https://github.com/docker/build-push-action)

---

**Quick Command Reference**:
```bash
# View GitHub secrets
gh secret list

# Set a secret
gh secret set SECRET_NAME -b "secret_value"

# Delete a secret
gh secret delete SECRET_NAME
```
