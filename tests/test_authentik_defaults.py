"""Regression tests for Authentik defaults."""

from __future__ import annotations

from pathlib import Path

import yaml


def _load_yaml(path: str) -> dict:
  return yaml.safe_load(Path(path).read_text())


def test_authentik_secret_placeholders_exist() -> None:
  secrets = _load_yaml("secrets.default.yml")
  for key in [
    "AUTHENTIK_PG_DB",
    "AUTHENTIK_PG_USER",
    "AUTHENTIK_PG_PASS",
    "AUTHENTIK_SECRET_KEY",
  ]:
    assert key in secrets, f"Missing {key} in secrets.default.yml"


