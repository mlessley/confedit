import paramiko
import time

def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)

    while not stdout.channel.exit_status_ready():
        time.sleep(1)

    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    return output, error

def establish_ssh_connection(server_ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, username=username, password=password)
    return ssh

def close_ssh_connection(ssh):
    ssh.close()

# Usage example
server_ip = 'remote_server_ip'
username = 'username'
password = 'password'

ssh = establish_ssh_connection(server_ip, username, password)

commands = [
    'command1',
    'command2',
    'command3',
    # Add more commands as needed
]

outputs = []

for command in commands:
    output, error = run_command(ssh, command)
    outputs.append(output)

close_ssh_connection(ssh)
