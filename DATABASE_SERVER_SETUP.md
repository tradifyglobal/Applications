# Database Server Configuration - Complete

## ✅ SSH Public Key Authentication Setup

### Database Server Details
- **IP Address**: 192.168.6.129
- **Username**: zubair
- **Hostname**: dev-database-srv
- **OS**: Ubuntu Linux (6.8.0-90-generic)
- **Architecture**: x86_64

### SSH Configuration Status
✅ **SSH Public Key Authentication**: ENABLED

**Status**: Successfully configured! You can now connect without password.

### Connection Methods

#### Method 1: SSH with Public Key (No Password)
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129
```

#### Method 2: SSH with Default Key
```bash
ssh zubair@192.168.6.129
```

#### Method 3: SCP File Transfer
```bash
# Copy file to server
scp -i ~/.ssh/id_rsa /path/to/local/file zubair@192.168.6.129:/path/to/remote/location

# Copy file from server
scp -i ~/.ssh/id_rsa zubair@192.168.6.129:/path/to/remote/file /path/to/local/location
```

## Verification Commands

### Test SSH Connection (Public Key)
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "whoami; hostname"
```

### Check SSH Configuration
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "cat ~/.ssh/authorized_keys"
```

### List SSH Keys on Database Server
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "ls -la ~/.ssh/"
```

## Database Server Information

### System Details
| Property | Value |
|----------|-------|
| Hostname | dev-database-srv |
| IP Address | 192.168.6.129 |
| OS | Ubuntu Linux |
| Kernel | 6.8.0-90-generic |
| Architecture | x86_64 (64-bit) |
| SSH User | zubair |

### SSH Authentication
| Method | Status | Command |
|--------|--------|---------|
| Public Key | ✅ Enabled | `ssh -i ~/.ssh/id_rsa zubair@192.168.6.129` |
| Password | Available | `ssh zubair@192.168.6.129` (if needed) |

## Setup Summary

### What Was Completed

1. ✅ **SSH Directory Created**
   - Created `~/.ssh` directory with proper permissions (700)

2. ✅ **Public Key Added**
   - Added local public key to `~/.ssh/authorized_keys` on database server
   - Set proper permissions (600) on authorized_keys

3. ✅ **Connection Tested**
   - Successfully connected without password using public key
   - Verified user and hostname

4. ✅ **SSH Configuration Verified**
   - SSH daemon accepting public key authentication
   - No password required for future connections

## Integration with GitHub Actions

For GitHub Actions to deploy to the database server, add this secret:

**Secret Name**: `DB_SSH_PRIVATE_KEY`
**Value**: Your SSH private key content

The workflow will use this to connect:
```yaml
DB_SERVER_IP: 192.168.6.129
DB_SERVER_USER: zubair
DB_SERVER_SSH_KEY: ${{ secrets.DB_SSH_PRIVATE_KEY }}
```

## Security Notes

✅ **Security Configurations**:
- Public key authentication enabled
- Password-based SSH still available as backup
- SSH key permissions properly set (600 on authorized_keys)
- SSH directory permissions properly set (700)

## Common Tasks

### Check PostgreSQL Installation
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "which psql"
```

### Check MySQL Installation
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "which mysql"
```

### Check Running Services
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "sudo systemctl status postgresql"
```

### Create Database
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "createdb -U postgres erp_dev_db"
```

### Connect to Database
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "psql -U postgres -d erp_dev_db"
```

## Next Steps

### 1. Configure Database
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Create Database User for ERP
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "sudo -u postgres psql -c \"CREATE USER erp_user WITH PASSWORD 'erp_password';\""
```

### 3. Create Database
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "sudo -u postgres psql -c \"CREATE DATABASE erp_dev_db OWNER erp_user;\""
```

### 4. Update Database Credentials in App Server
On app server (.env file):
```
DB_HOST=192.168.6.129
DB_PORT=5432
DB_USER=erp_user
DB_PASSWORD=erp_password
DB_NAME=erp_dev_db
```

## Files and Locations

### Local Machine
- **SSH Private Key**: `~/.ssh/id_rsa`
- **SSH Public Key**: `~/.ssh/id_rsa.pub`

### Database Server
- **SSH Directory**: `~/.ssh/` (permissions: 700)
- **Authorized Keys**: `~/.ssh/authorized_keys` (permissions: 600)

## Troubleshooting

### If Connection Fails
```bash
# Test connection with verbose output
ssh -i ~/.ssh/id_rsa -v zubair@192.168.6.129

# Check if key is being recognized
ssh-add ~/.ssh/id_rsa
```

### If Password Still Needed
```bash
# Verify authorized_keys is readable
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "cat ~/.ssh/authorized_keys"

# Verify permissions
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "ls -la ~/.ssh/"
```

### If SSH Permissions Are Wrong
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

## SSH Quick Reference

### Connect
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129
```

### Run Remote Command
```bash
ssh -i ~/.ssh/id_rsa zubair@192.168.6.129 "command here"
```

### Copy File To Server
```bash
scp -i ~/.ssh/id_rsa /local/path zubair@192.168.6.129:/remote/path
```

### Copy Directory To Server
```bash
scp -r -i ~/.ssh/id_rsa /local/path zubair@192.168.6.129:/remote/path
```

### Copy From Server
```bash
scp -i ~/.ssh/id_rsa zubair@192.168.6.129:/remote/path /local/path
```

### Port Forwarding
```bash
ssh -i ~/.ssh/id_rsa -L local_port:127.0.0.1:remote_port zubair@192.168.6.129
```

---

**Setup Completed**: December 17, 2025

**Status**: ✅ Ready for Production Configuration

**Next Action**: Install and configure database software on 192.168.6.129
