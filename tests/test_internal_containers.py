from pathlib import Path

import yaml


def test_internal_container_images_include_tag():
    vars_path = Path("roles/internal/vars/main.yml")
    contents = vars_path.read_text(encoding="utf-8")
    data = yaml.safe_load(contents)
    containers = data.get("internal_docker_containers", [])
    missing_tags = [c["name"] for c in containers if ":" not in c.get("image", "")]
    assert not missing_tags, (
        "Expected every container image to specify an explicit tag; missing tags for: "
        + ", ".join(missing_tags)
    )
