# SSH Configuration and Setup

This guide covers SSH key generation, setup, and configuration for secure communication between your local machine and the remote servers.

## Why SSH Public Key Authentication?

- More secure than password authentication
- Automated deployment without prompts
- Industry standard for production servers
- GitHub Actions can use private keys securely

## Step 1: Generate SSH Key Pair

### On Your Local Machine

If you don't already have an SSH key pair:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -C "your.email@example.com" -N ""
```

Parameters explained:
- `-t rsa`: Key type (RSA)
- `-b 4096`: Key size (4096 bits = strong security)
- `-f ~/.ssh/id_rsa`: File path
- `-C "email"`: Comment/label
- `-N ""`: No passphrase (for automation)

### Check Generated Keys

```bash
ls -la ~/.ssh/
```

You should see:
- `id_rsa` (private key - KEEP SECRET)
- `id_rsa.pub` (public key - safe to share)

Set correct permissions:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

## Step 2: Copy Public Key to App Server

### Option A: Using ssh-copy-id (Recommended)

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub deploy@app-server-ip
```

When prompted, enter the deploy user's password.

### Option B: Manual Copy

```bash
# Create .ssh directory on remote server
ssh deploy@app-server-ip "mkdir -p ~/.ssh && chmod 700 ~/.ssh"

# Copy public key
cat ~/.ssh/id_rsa.pub | ssh deploy@app-server-ip "cat >> ~/.ssh/authorized_keys"

# Set proper permissions
ssh deploy@app-server-ip "chmod 600 ~/.ssh/authorized_keys"
```

### Verify SSH Access

```bash
ssh deploy@app-server-ip "echo 'SSH access successful'"
```

Should print: `SSH access successful` (without password prompt)

## Step 3: Copy Public Key to Database Server

Repeat the same process for the database server:

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub deploy@db-server-ip
```

Verify:

```bash
ssh deploy@db-server-ip "echo 'SSH access successful'"
```

## Step 4: SSH Config File (Optional but Recommended)

Create or edit `~/.ssh/config` to simplify SSH commands:

```bash
nano ~/.ssh/config
```

Add:

```
Host erp-app
    HostName <app-server-ip>
    User deploy
    IdentityFile ~/.ssh/id_rsa
    Port 22
    IdentitiesOnly yes

Host erp-db
    HostName <db-server-ip>
    User deploy
    IdentityFile ~/.ssh/id_rsa
    Port 22
    IdentitiesOnly yes
```

Save and set permissions:

```bash
chmod 600 ~/.ssh/config
```

Now you can connect more easily:

```bash
ssh erp-app
ssh erp-db
```

## Step 5: Configure GitHub Secrets

### Get Your Private Key

```bash
cat ~/.ssh/id_rsa
```

Copy the entire output (including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`).

### Add to GitHub Repository

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add the following secrets:

| Secret Name | Value |
|---|---|
| `SSH_PRIVATE_KEY` | Your private key content (from previous step) |
| `APP_SERVER_IP` | Your app server IP address |
| `APP_SERVER_USER` | Deploy user name (typically `deploy` or `ubuntu`) |
| `APP_SERVER_PORT` | SSH port (typically `22`) |
| `DB_SERVER_IP` | Your database server IP address |
| `DB_SERVER_USER` | Deploy user name on DB server |

### Step-by-Step for GitHub Secrets

1. **SSH_PRIVATE_KEY**:
   - Copy output of `cat ~/.ssh/id_rsa`
   - Paste into GitHub secret

2. **APP_SERVER_IP**:
   - Your app server public IP
   - Example: `203.0.113.45`

3. **APP_SERVER_USER**:
   - Username on app server
   - Usually `deploy`, `ec2-user`, or `ubuntu`
   - Get it: `ssh app-server "whoami"`

4. **APP_SERVER_PORT**:
   - SSH port on app server
   - Usually `22`

5. **DB_SERVER_IP**:
   - Your database server IP
   - Example: `203.0.113.46`

6. **DB_SERVER_USER**:
   - Username on DB server

## Step 6: Test SSH Access

### Test App Server Access

```bash
# Test basic connectivity
ssh deploy@app-server-ip "pwd"

# Test with Docker
ssh deploy@app-server-ip "docker ps"

# Test with Docker Compose
ssh deploy@app-server-ip "docker compose --version"
```

### Test Database Server Access

```bash
# Test basic connectivity
ssh deploy@db-server-ip "pwd"

# Test PostgreSQL
ssh deploy@db-server-ip "psql --version"

# Test database connection
ssh deploy@db-server-ip "psql -U erp_user -d erp_db -h localhost -c 'SELECT version();'"
```

## Step 7: SSH Agent (Optional for Convenience)

Start SSH agent:

```bash
eval "$(ssh-agent -s)"
```

Add your key:

```bash
ssh-add ~/.ssh/id_rsa
```

Check keys loaded:

```bash
ssh-add -l
```

## Advanced SSH Configuration

### SSH Key with Passphrase

For enhanced security, you can add a passphrase:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -C "your.email@example.com"
```

You'll be prompted for a passphrase. This adds a password to your private key.

For GitHub Actions with passphrase keys, use SSH agent:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

### Multiple SSH Keys

If you have multiple keys:

```bash
ssh -i ~/.ssh/id_rsa.erp deploy@app-server-ip
```

Or configure in `~/.ssh/config`:

```
Host erp-app
    HostName <app-server-ip>
    User deploy
    IdentityFile ~/.ssh/id_rsa.erp
```

### SSH Key Rotation

Periodically rotate your SSH keys:

1. Generate new key pair
2. Add new public key to servers
3. Test new key
4. Remove old public key from servers
5. Rotate GitHub secrets

## Troubleshooting

### "Permission denied (publickey)"

```bash
# Check local key exists
ls -la ~/.ssh/id_rsa

# Check remote authorized_keys
ssh deploy@app-server-ip "cat ~/.ssh/authorized_keys"

# Check file permissions on remote
ssh deploy@app-server-ip "ls -la ~/.ssh/"

# Should show:
# drwx------ (700) for .ssh directory
# -rw------- (600) for authorized_keys
```

### SSH Connection Timeout

```bash
# Test connectivity
ping app-server-ip

# Test port 22
telnet app-server-ip 22
# Or
nc -zv app-server-ip 22

# Check firewall
sudo ufw status
sudo ufw allow 22/tcp
```

### "Could not open a connection"

```bash
# Verify server is running
ping app-server-ip

# Check SSH service on remote
ssh deploy@app-server-ip "sudo systemctl status ssh"

# Restart SSH service
ssh deploy@app-server-ip "sudo systemctl restart ssh"
```

### Key Not Found in SSH Agent

```bash
# List SSH keys
ssh-add -l

# Add key to agent
ssh-add ~/.ssh/id_rsa

# For GitHub Actions, ensure key is in secrets (not in agent)
```

### Wrong File Permissions

```bash
# Fix permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/authorized_keys  # On remote servers
```

## Security Best Practices

1. **Never share private keys** - Only share `.pub` files
2. **Keep backups** - Save your private key securely
3. **Rotate keys regularly** - At least annually
4. **Disable password auth** - After SSH keys are working
5. **Monitor SSH logs** - `sudo tail -f /var/log/auth.log`
6. **Use strong passphrases** - If adding passphrase to key
7. **Limit SSH access** - Use firewall rules

## Disable Password Authentication (Optional)

After SSH keys are working, disable password auth on servers:

```bash
sudo nano /etc/ssh/sshd_config
```

Change:

```
PasswordAuthentication yes
```

To:

```
PasswordAuthentication no
```

Restart SSH:

```bash
sudo systemctl restart ssh
```

## Next Steps

1. Proceed to `README/GITHUB_ACTIONS.md` for CI/CD setup
2. Proceed to `README/DEPLOYMENT.md` for deployment
3. Test deployment workflow in GitHub Actions

---

**Security Reminder**: Treat your private key like a password. Never commit it to version control or share it with others.
