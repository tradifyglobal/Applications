# Quick Reference - SSH Public Key Setup

## ✅ Status: Complete

SSH public key authentication has been successfully configured on dev-app-srv (192.168.6.128).

---

## Quick Connection

### From Windows PowerShell:
```powershell
ssh zubair@192.168.6.128
```

### From Command Line / Git Bash:
```bash
ssh zubair@192.168.6.128
```

### With Explicit Key:
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.128
```

---

## Key Details

| Property | Value |
|----------|-------|
| **Server** | 192.168.6.128 (dev-app-srv) |
| **Username** | zubair |
| **Auth Method** | SSH Public Key (RSA 4096) |
| **Private Key** | `~/.ssh/id_rsa` |
| **Public Key** | `~/.ssh/id_rsa.pub` |
| **Fingerprint** | `SHA256:MQNbRkuRX6OcRPElJLpSLb7Fr1ZEvFfBmCt5sBBeFnw` |

---

## Verification

```bash
# Test connection (should not ask for password)
ssh zubair@192.168.6.128 "echo 'Connected!'"
```

**Expected Output:**
```
Connected!
```

---

## For Deployment Scripts

Update your deployment scripts to use SSH instead of password:

**Before (password auth):**
```bash
sshpass -p "erp" ssh zubair@192.168.6.128 "command"
```

**After (key auth):**
```bash
ssh zubair@192.168.6.128 "command"
```

---

## SCP File Transfer

```bash
# Upload file to server
scp /local/path/file.txt zubair@192.168.6.128:/remote/path/

# Download file from server
scp zubair@192.168.6.128:/remote/path/file.txt /local/path/
```

---

## SSH Config (Optional - for easier access)

Create or edit `~/.ssh/config`:
```
Host dev-app
    HostName 192.168.6.128
    User zubair
    IdentityFile ~/.ssh/id_rsa
    StrictHostKeyChecking no
```

Then connect with:
```bash
ssh dev-app
scp file.txt dev-app:/path/
```

---

## Environment Setup Files Created

| File | Purpose |
|------|---------|
| `ENVIRONMENTS.md` | Complete environment configuration guide |
| `SSH_SETUP_COMPLETE.md` | SSH setup documentation |
| `core/settings/base.py` | Common settings for all environments |
| `core/settings/development.py` | Development environment settings |
| `core/settings/staging.py` | Staging environment settings |
| `core/settings/production.py` | Production environment settings |
| `.env.example` | Updated with ENVIRONMENT variable |

---

## Using Environment Variables

```bash
# Set environment (Windows)
set ENVIRONMENT=development
python manage.py runserver

# Set environment (Unix/Linux/Mac)
export ENVIRONMENT=development
python manage.py runserver
```

---

## Troubleshooting

**Connection refused?**
```bash
ssh -v zubair@192.168.6.128  # Use -v for verbose output
```

**Permission denied?**
```bash
ssh zubair@192.168.6.128 "ls -la ~/.ssh/authorized_keys"
```

**Check key fingerprint:**
```bash
ssh-keygen -l -f ~/.ssh/id_rsa.pub
```

---

## All Set! 🎉

You can now:
- ✅ SSH into dev-app-srv without password
- ✅ Run deployment scripts with key authentication
- ✅ Copy files securely with SCP
- ✅ Use Production, Staging, or Development environment configurations

**Next Steps:**
1. Deploy application to dev-app-srv
2. Set `ENVIRONMENT=development` on dev server
3. Configure database on dev server
4. Run Django migrations
5. Start the application
