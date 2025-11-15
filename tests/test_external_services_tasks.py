"""Regression-style tests for external services Ansible tasks."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SERVICES_DIR = REPO_ROOT / "roles" / "external" / "services"
SERVICES_TASKS_FILE = REPO_ROOT / "roles" / "external" / "tasks" / "services.yml"
HANDLERS_FILE = REPO_ROOT / "roles" / "external" / "handlers" / "main.yml"


def _load_yaml_documents(path: Path) -> list[dict[str, object]]:
    """Load a YAML file containing a single list of task dictionaries."""

    content = path.read_text(encoding="utf-8")
    data = yaml.safe_load(content)
    if not isinstance(data, list):  # pragma: no cover - defensive branch
        raise TypeError(f"Expected list of tasks in {path}, got {type(data)!r}")
    return data


def _iter_service_task_files() -> Iterable[Path]:
    """Yield every external service task file."""

    return sorted(SERVICES_DIR.glob("*.yml"))


def test_services_task_includes_all_known_services() -> None:
    """Ensure ``tasks/services.yml`` includes each concrete service file."""

    service_tasks = _load_yaml_documents(SERVICES_TASKS_FILE)
    included_files = {
        task.get("ansible.builtin.include_tasks")
        for task in service_tasks
        if isinstance(task, dict)
    }

    expected_files = {
        f"services/{path.name}"
        for path in _iter_service_task_files()
    }

    assert included_files == expected_files


def test_each_service_task_notifies_existing_handler() -> None:
    """Verify that services notify handlers defined in ``handlers/main.yml``."""

    handler_tasks = _load_yaml_documents(HANDLERS_FILE)
    handler_names = {
        task.get("name")
        for task in handler_tasks
        if isinstance(task, dict)
    }

    assert handler_names, "Expected handlers to be defined"

    for service_file in _iter_service_task_files():
        for task in _load_yaml_documents(service_file):
            notify = task.get("notify") if isinstance(task, dict) else None
            if isinstance(notify, str):
                notifications = {notify}
            elif isinstance(notify, list):
                notifications = set(notify)
            else:
                notifications = set()

            missing_handlers = notifications - handler_names
            assert not missing_handlers, (
                f"Service task {service_file.name} notifies missing handlers: "
                f"{sorted(missing_handlers)}"
            )


@pytest.mark.parametrize("service_file", list(_iter_service_task_files()))
def test_service_tasks_use_docker_container_module(service_file: Path) -> None:
    """Ensure every service defines container tasks with restart policies."""

    tasks = _load_yaml_documents(service_file)
    assert tasks, f"Expected at least one task in {service_file.name}"

    container_tasks = [
        task
        for task in tasks
        if isinstance(task, dict) and "community.docker.docker_container" in task
    ]
    assert container_tasks, f"{service_file.name} must define at least one container task"

    for task in container_tasks:
        container_config = task["community.docker.docker_container"]
        assert isinstance(
            container_config, dict
        ), f"Task in {service_file.name} must use docker_container module"
        assert (
            container_config.get("restart_policy") == "always"
        ), f"{service_file.name} must set restart_policy to 'always'"
