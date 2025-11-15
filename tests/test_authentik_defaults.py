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


def test_authentik_role_defaults_exist() -> None:
  defaults = _load_yaml("roles/external/defaults/main.yml")
  for key in [
    "external_authentik_pg_image",
    "external_authentik_image",
    "external_authentik_pg_data_dir",
    "external_authentik_media_dir",
    "external_authentik_config_dir",
    "external_authentik_http_port",
    "external_authentik_https_port",
    "external_authentik_redis_host",
    "external_authentik_redis_port",
  ]:
    assert key in defaults, f"Missing {key} in external defaults"
