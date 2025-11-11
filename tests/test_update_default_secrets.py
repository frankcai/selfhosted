"""Tests for update_default_secrets utility functions."""

import sys
from copy import deepcopy
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from update_default_secrets import replace_values_with_changeme


def test_replace_values_with_changeme_replaces_scalars_and_nested_structures():
    sample = {
        "root_key": "original",
        "nested": {
            "child_key": "child_value",
            "inner_list": ["item_one", "item_two"],
        },
    }

    result = replace_values_with_changeme(deepcopy(sample))

    assert result == {
        "root_key": "CHANGEME",
        "nested": {
            "child_key": "CHANGEME",
            "inner_list": ["CHANGEME", "CHANGEME"],
        },
    }


def test_replace_values_with_changeme_preserves_local_domains_placeholder():
    sample = {
        "config": {
            "LOCAL_DOMAINS": {"existing.domain": "should_be_replaced"},
            "other_values": ["still_here"],
        }
    }

    result = replace_values_with_changeme(deepcopy(sample))

    assert result["config"]["LOCAL_DOMAINS"] == {
        "subdomain1.domain": "CHANGEME",
        "subdomain2.domain": "CHANGEME",
    }
    assert result["config"]["other_values"] == ["CHANGEME"]
