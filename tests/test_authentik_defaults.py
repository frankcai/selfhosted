"""Regression tests for Authentik defaults."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _load_yaml(path: str) -> Any:
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


def test_authentik_service_waits_for_postgres_health() -> None:
  tasks = _load_yaml("roles/external/services/authentik.yml")
  assert isinstance(tasks, list), "Authentik service definition should be a list of tasks"
  wait_tasks = [
    task
    for task in tasks
    if task.get("name") == "External | Services | Authentik | Wait for Postgres to be healthy"
  ]
  assert wait_tasks, "Authentik service should wait for Postgres health"
  wait_task = wait_tasks[0]
  assert (
    wait_task.get("register") == "external_authentik_pg_info"
  ), "Wait task should register an external-scoped result"
  assert (
    "community.docker.docker_container_info" in wait_task
  ), "Wait task must inspect container health"
