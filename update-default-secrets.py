from ruamel.yaml import YAML
from ansible.parsing.vault import VaultLib, VaultSecret

def load_encrypted_secrets(file_path, vault_password_file):
    with open(vault_password_file, 'r') as pw_file:
        vault_password = pw_file.read().strip()

    vault = VaultLib([(None, VaultSecret(vault_password.encode()))])
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = vault.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data

def replace_values_with_changeme(data):
    yaml = YAML()
    yaml.preserve_quotes = True
    content = yaml.load(data)

    def replace(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == 'LOCAL_DOMAINS':
                    # Replace with placeholder subdomains
                    node[key] = {'subdomain1.domain': 'CHANGEME', 'subdomain2.domain': 'CHANGEME'}
                    continue
                if isinstance(value, (dict, list)):
                    replace(value)
                else:
                    node[key] = 'CHANGEME'
        elif isinstance(node, list):
            for i, item in enumerate(node):
                if isinstance(item, (dict, list)):
                    replace(item)
                else:
                    node[i] = 'CHANGEME'

    replace(content)
    return content

vault_password_file = 'vault_pass.txt'
decrypted_content = load_encrypted_secrets('secrets.yml', vault_password_file)

yaml = YAML()
yaml.preserve_quotes = True
updated_content = replace_values_with_changeme(decrypted_content)

with open('secrets.default.yml', 'w') as f:
    f.write("---\n")
    yaml.dump(updated_content, f)
