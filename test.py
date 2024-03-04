import os
import tempfile
import paramiko

# Specify the image name and tag
image_name = "newtondotcom/noauthdiscord"
image_tag = "latest"

# SSH configuration
ssh_host = "141.145.217.120"
ssh_port = 22
ssh_username = "ubuntu"
ssh_private_key = "scripts/key.key"
ssh_public_key = "scripts/key.pub"

def run_remote_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')

def test_ssh_connection():
    # Create SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to SSH server with private key authentication
    ssh_key = paramiko.RSAKey.from_private_key_file(ssh_private_key)
    ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_username, key_filename=ssh_private_key)

    # Test the connection
    try:
        stdout, stderr = run_remote_command(ssh_client, "echo 'Hello, world!'")
        print(stdout)
    except Exception as e:
        print(e)
    stdout, stderr = run_remote_command(ssh_client, "echo 'Hello, world!'")
    print(stdout)

    # Close SSH connection
    ssh_client.close()

test_ssh_connection()