# Selfhosted using Ansible

Automate a full self-hosting stack across five Ubuntu servers with a single Ansible entry point. Each host focuses on a specific concern (DNS, monitoring, VPN, internal-facing apps, and external services) so maintenance stays predictable and new infrastructure can be added without disturbing the rest of the fleet. The playbooks here configure Docker, deploy applications, and wire Nginx frontends using the same conventions throughout.

## Architecture at a Glance

| Role      | Purpose                                                                    |
|-----------|----------------------------------------------------------------------------|
| `dns`     | Authoritative DNS + DHCP helpers.                                          |
| `monitoring` | Metrics, log shipping, and synthetic checks for every other host.       |
| `vpn`     | Secure entry point into the internal network.                              |
| `internal`| Runs internal-only applications (home automation, media, tooling, etc.).   |
| `external`| Serves internet-facing sites while still being reachable from the LAN.     |

Provision these servers on your own hardware or virtualize them with a platform such as [Proxmox](https://www.proxmox.com/).

## Requirements

* Control node with Python 3.10+, Ansible 2.15+, `ansible-lint`, and `python3-pip`.
* SSH access to every managed host using a keypair (`ssh-copy-id user@host`).
* Passwordless sudo on each host for the Ansible user. Use `visudo` and add either `youruser ALL=(ALL:ALL) NOPASSWD:ALL` or `%sudo ALL=(ALL:ALL) NOPASSWD:ALL` as needed.
* SSH password authentication disabled on the managed nodes once keys are in place.

## Getting Started

1. **Clone and bootstrap**
   ```bash
   git clone git@github.com:<you>/selfhosted.git
   cd selfhosted
   cp secrets.default.yml secrets.yml
   ```
2. **Configure inventory**  
   Edit `inventory.ini` and `group_vars/all.yml` to match hostnames, SSH usernames, and private key paths.
3. **Manage secrets**  
   All sensitive data lives in `secrets.yml`. Encrypt it with Ansible Vault:
   ```bash
   ansible-vault edit secrets.yml
   ```
   Optionally create a local `vault_pass.txt` (already in `.gitignore`) and reference it from `ansible.cfg` so CI/cron tasks can unlock the vault automatically.
4. **Keep defaults in sync**  
   When new secrets are added, run `python update_default_secrets.py` to regenerate `secrets.default.yml` and document the placeholder values for other operators.

## Running the Automation

These commands mirror the CI expectations. Running them locally before a PR keeps drift to a minimum.

```bash
ansible-lint
ansible-playbook --syntax-check site.yml
python -m pytest
```

Apply the full configuration:

```bash
sudo ansible-playbook site.yml
```

Target a specific host/role:

```bash
sudo ansible-playbook site.yml --limit internal
```

Because many roles manage Docker containers, ensure the target hosts can reach any required registries (public or private) and that credentials are stored in `secrets.yml`.

## Local Git Hooks

Point Git at the repo-provided hooks to require the same lint/syntax/test checks before every commit:

```bash
git config core.hooksPath .githooks
```

The pre-commit hook runs `ansible-lint`, `ansible-playbook --syntax-check site.yml`, and `python -m pytest`. It expects a local `vault_pass.txt` so Ansible can unlock vaulted variables.

## Operational Tips

* Use the provided cron snippets to keep the control node tidy and automatically re-apply the playbooks:
  * Daily 04:00 – remove stale VS Code server directories.  
    `0 4 * * * rm -rf /home/<user>/.vscode-server /home/<user>/.vscode-server-insiders`
  * Weekly Saturday 03:00 – run the full site play.  
    `0 3 * * 6 cd ~/selfhosted && sudo ansible-playbook site.yml`
* Follow the shared conventions in `AGENTS.md` when adding services or roles (two-space YAML indentation, module-driven tasks, handler naming, etc.).
* Never commit real credentials. If a service requires a new secret, add it to `secrets.default.yml`, document it in the relevant role README, and store the live value only in the vaulted `secrets.yml`.

## License

MIT License – see `LICENSE` for the full text.
