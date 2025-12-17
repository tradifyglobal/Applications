# Setup SSH public key authentication on remote server
# This script uploads the SSH public key and configures authorized_keys

$remoteHost = "192.168.6.128"
$remoteUser = "zubair"
$remotePass = "erp"
$pubKeyPath = "$env:USERPROFILE\.ssh\id_rsa.pub"

# Read the public key
$pubKey = Get-Content $pubKeyPath

# Commands to run on remote server
$setupCommands = @"
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo '$pubKey' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo "SSH public key setup complete"
echo "Authorized keys:"
cat ~/.ssh/authorized_keys
"@

# Save commands to a temporary file
$tempScript = "$env:TEMP\setup-ssh.sh"
$setupCommands | Out-File -Encoding ASCII $tempScript

Write-Host "Uploading SSH public key to $remoteHost..."
Write-Host "Public key: $pubKey"
Write-Host ""

# Upload and execute setup
Write-Host "Connecting to $remoteHost and setting up SSH key authentication..."

# Use scp to copy the public key
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL $pubKeyPath "$remoteUser@$remoteHost:/tmp/id_rsa.pub"

# Connect and add the key to authorized_keys
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL "$remoteUser@$remoteHost" `
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat /tmp/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && echo 'SSH key setup complete'"

Write-Host ""
Write-Host "SSH public key authentication setup complete!"
Write-Host "You can now connect using: ssh $remoteUser@$remoteHost"
