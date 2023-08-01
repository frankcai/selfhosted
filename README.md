## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [FAQ](#faq)

## Overview
This repository contains my production Docker services, which are accessible from anywhere via HTTPS using Traefik. These services are run on a single Ubuntu server, with data volumes segregated on a Synology NAS.

## Installation
1. Install [Ubuntu LTS](https://releases.ubuntu.com/)
2. Update and secure the server
```bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install openssh-server -y

# Deactivate Root Login
echo "PermitRootLogin no" >> /etc/ssh/sshd_config 
echo "PermitEmptyPasswords no" /etc/ssh/sshd_config

# Activate Firewall
sudo ufw allow OpenSSH
sudo ufw allow proto tcp from any to any port 80,443
sudo ufw enable
```
3. [Enable Unattended Upgrades](https://help.ubuntu.com/community/AutomaticSecurityUpdates)
4. [Setup SSH Keys](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#) und SSH-Agent 
```bash
eval "$(ssh-agent)"
ssh-add -k ~/.ssh/id_rsa
```
5. Clone this repo
```bash
git clone git@github.com:frankcai/selfhosted.git
```
6. Install [docker](https://docs.docker.com/engine/install/ubuntu/)
7. Setup logrotate
```bash
# install logrotate
systenctl --user link $HOME/projects/selfhosted/logrotate.timer
systenctl --user link $HOME/projects/selfhosted/logrotate.service
systemctl --user enable logrotate.timer --now

# enable traefik logrotate
cp etc/traefik-logrotate.conf /etc/logrotate.d/traefik
```
8. Edit the environment file
```bash
cp .env.example .env
```
9. Mount remote drives using fstab
```bash
sudo apt-get install nfs-common -y
sudo vi /etc/fstab
```

## FAQ
How to update running containers?
```bash
docker-compose down && docker-compose pull && docker-compose up -d --remove-orphans && docker image prune -a -f 
```
How to restart after changing or adding new containers?
```bash
docker-compose up -d
```
Sometimes a container build must be forced (e.g. rebuilding the traefik container for port changes in services)
```bash
docker-compose up -d --force-recreate traefik
```

How to browse files inside a container?  
docker exec -it <containername> /bin/bash

Why are the routes from the services.yml file not found?  
Traefik uses the internal Docker DNS. Therefore, for external services, a DNS entry must be entered in /etc/docker/daemon.json. E.g.: "dns": ["192.168.168.39", "1.1.1.1"]

What should be done after a server restart?
```bash
sudo service apache2 stop && sudo service nginx stop 
```

Encountering the "Bind: address already in use" error when starting traefik?    
Use netstat -tulpn and kill <pid> to delete the process using the same port.

Why is nodered unreachable?  
Nodered needs to run in host mode and the server needs to allow local connections:
```bash
sudo ufw allow from 192.168.0.0/16
sudo ufw allow from 172.0.0.0/10
```