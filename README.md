# Selfhosted using Ansible
## Overview
This repository houses Ansible playbooks tailored for a self-hosted setup designed to run seamlessly on five distinct Ubuntu servers. The design concept behind this architecture categorizes each server with a unique role, ensuring optimized performance and manageability.

### Server Roles:
* DNS: Handles domain name resolution.
* Monitoring: Monitors all servers using comprehensive metrics and logs.
* VPN: Acts as an endpoint for VPN connections, granting secure access to the internal network.
* Internal: Hosts internal-facing websites.
* External: Serves websites accessible both internally and externally from the internet.

For those looking into virtualization solutions, I highly recommend using [Proxmox](https://www.proxmox.com/) for its reliability and ease of use.

## Prerequisites
Before running the Ansible tasks, ensure you've taken care of the following preparations:

### 1. SSH Key Distribution:
Copy the public SSH key of the Ansible control server to each of the nodes.

```bash
ssh-copy-id user@host_ip
```
### 2. Sudo Access Without Password:

#### Edit the sudoers file:
Use the visudo command instead of directly editing the /etc/sudoers file. This prevents potential syntax errors.

```bash
sudo visudo
```
#### Add a NOPASSWD directive:
For a specific user to run all commands without a password, append:

```bash
yourusername ALL=(ALL:ALL) NOPASSWD: ALL
```
For a group, like sudo:

```bash
%sudo ALL=(ALL:ALL) NOPASSWD: ALL
```
#### Save and exit:
In nano: CTRL + O to save and CTRL + X to exit.
In vi: ESC, type :wq, and hit Enter.

#### Test:
Run a sudo command to check; you shouldn't be prompted for a password.

### 3. Set the required secrets using ansible vault

```bash
ansible-vault edit secrets.yml
```

### Useful Commands
#### Run All Tasks:

```bash
sudo ansible-playbook site.yml`
```
#### Run Tasks for Specific Role (e.g., dns):

```bash
sudo ansible-playbook site.yml --limit dns`
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.