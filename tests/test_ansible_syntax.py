"""Test suite validating Ansible playbooks and roles."""

from __future__ import annotations

from collections.abc import Iterator
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
ANSIBLE_PLAYBOOK = os.environ.get("ANSIBLE_PLAYBOOK") or shutil.which("ansible-playbook")

if ANSIBLE_PLAYBOOK is None:  # pragma: no cover - depends on environment
    pytest.skip(
        "ansible-playbook executable not found; set $ANSIBLE_PLAYBOOK to override",
        allow_module_level=True,
    )


@pytest.fixture(scope="session", autouse=True)
def configure_vault_password(
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[None]:
    """Ensure Ansible sees a vault password file during syntax checks."""

    original_vault = os.environ.get("ANSIBLE_VAULT_PASSWORD_FILE")
    original_roles = os.environ.get("ANSIBLE_ROLES_PATH")
    vault_file = tmp_path_factory.mktemp("ansible") / "vault_pass.txt"
    vault_file.write_text("dummy\n", encoding="utf-8")
    os.environ["ANSIBLE_VAULT_PASSWORD_FILE"] = str(vault_file)
    os.environ["ANSIBLE_ROLES_PATH"] = str(REPO_ROOT / "roles")

    try:
        yield
    finally:
        if original_vault is None:
            os.environ.pop("ANSIBLE_VAULT_PASSWORD_FILE", None)
        else:
            os.environ["ANSIBLE_VAULT_PASSWORD_FILE"] = original_vault

        if original_roles is None:
            os.environ.pop("ANSIBLE_ROLES_PATH", None)
        else:
            os.environ["ANSIBLE_ROLES_PATH"] = original_roles


def run_syntax_check(playbook: Path) -> subprocess.CompletedProcess[str]:
    """Run ``ansible-playbook --syntax-check`` for the given playbook."""
    return subprocess.run(
        [str(ANSIBLE_PLAYBOOK), "--syntax-check", str(playbook)],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
    )


@pytest.mark.parametrize("playbook", [REPO_ROOT / "site.yml"])
def test_project_playbooks_are_valid(playbook: Path) -> None:
    """Ensure top-level playbooks pass Ansible's syntax check."""
    result = run_syntax_check(playbook)
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("role_dir", sorted((REPO_ROOT / "roles").iterdir()))
def test_each_role_compiles(role_dir: Path, tmp_path: Path) -> None:
    """Ensure every role can be parsed by Ansible."""
    playbook = tmp_path / f"validate_{role_dir.name}.yml"
    playbook.write_text(
        "- hosts: all\n"
        "  gather_facts: false\n"
        "  roles:\n"
        f"    - {role_dir.name}\n",
        encoding="utf-8",
    )

    result = run_syntax_check(playbook)
    assert result.returncode == 0, result.stdout
