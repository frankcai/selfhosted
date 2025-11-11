"""Utilities for generating placeholder values for encrypted secrets."""

from pathlib import Path
from typing import Any, MutableMapping, MutableSequence, Union


def load_encrypted_secrets(file_path: str, vault_password_file: str) -> str:
    """Decrypt an Ansible vault file using the provided password file."""

    from ansible.parsing.vault import VaultLib, VaultSecret

    with open(vault_password_file, "r", encoding="utf-8") as pw_file:
        vault_password = pw_file.read().strip()

    vault = VaultLib([(None, VaultSecret(vault_password.encode()))])
    with open(file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = vault.decrypt(encrypted_data).decode("utf-8")
    return decrypted_data


def replace_values_with_changeme(
    data: Union[str, MutableMapping[str, Any], MutableSequence[Any]]
) -> Any:
    """Load YAML data and replace every scalar with a ``CHANGEME`` placeholder."""

    if isinstance(data, str):
        from ruamel.yaml import YAML

        yaml = YAML()
        yaml.preserve_quotes = True
        content = yaml.load(data)
    else:
        content = data

    def replace(node: Any) -> None:
        if isinstance(node, MutableMapping):
            for key, value in node.items():
                if key == "LOCAL_DOMAINS":
                    # Replace with placeholder subdomains
                    node[key] = {
                        "subdomain1.domain": "CHANGEME",
                        "subdomain2.domain": "CHANGEME",
                    }
                    continue
                if isinstance(value, (MutableMapping, MutableSequence)):
                    replace(value)
                else:
                    node[key] = "CHANGEME"
        elif isinstance(node, MutableSequence):
            for index, item in enumerate(node):
                if isinstance(item, (MutableMapping, MutableSequence)):
                    replace(item)
                else:
                    node[index] = "CHANGEME"

    replace(content)
    return content


def main(
    secrets_file: str = "secrets.yml",
    vault_password_file: str = "vault_pass.txt",
    output_file: str = "secrets.default.yml",
) -> None:
    """Generate a default secrets file with placeholder values."""

    decrypted_content = load_encrypted_secrets(secrets_file, vault_password_file)

    from ruamel.yaml import YAML

    yaml = YAML()
    yaml.preserve_quotes = True
    updated_content = replace_values_with_changeme(decrypted_content)

    output_path = Path(output_file)
    with output_path.open("w", encoding="utf-8") as output:
        output.write("---\n")
        yaml.dump(updated_content, output)


if __name__ == "__main__":
    main()
