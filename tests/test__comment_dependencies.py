import json
import pathlib

import pytest
import yaml

from grid_hooks import comment_dependencies

# This is less rigid than I would like as it relies on these not changing, but without maintain one or two standard
# repos we can always reference I have nothing better at this time
# It also requires proper github token setup, so not ideal
GRID_REPOS_AND_OWNERS = {
    "dp_f6oe_inventory_constraints": "avocado",
    "dp-m3lq-despatch-unit": "dragonfruit",
    "dp_0000_capabilities_grid_testing": "peach",
    "ext_fact_purchase_order_item0800_pl_table": None,  # Checking external processes are skipped properly
}
FIXTURE_CONFIG = pathlib.Path(__file__).parent / "fixtures" / "dummy_config.yaml"


def test__get_config_contents(tmp_path):
    sample_content = {
        "key_1": "some string data",
        "transforms": "some other string data",
        "key_2": 123_023,
    }
    file_path = tmp_path / "sample_config.yaml"
    file_path.write_text(json.dumps(sample_content))

    with pytest.raises(FileNotFoundError):
        comment_dependencies.get_config_contents(
            pathlib.Path("some_incorrect_path.yaml")
        )

    file_contents = comment_dependencies.get_config_contents(file_path)
    assert file_contents == sample_content


def test__get_grid_process_owner():
    for repo, owner in GRID_REPOS_AND_OWNERS.items():
        assert comment_dependencies.get_grid_process_owner(repo) == owner


def test__add_config_comments(monkeypatch):
    def mock_owner(grid_set_name):
        return f"owned_by_{grid_set_name}"

    monkeypatch.setattr(comment_dependencies, "get_grid_process_owner", mock_owner)
    dummy_config = yaml.safe_load(FIXTURE_CONFIG.read_text())

    old_dependencies = list(dummy_config.get("transforms").get("depends_on"))
    new_config = comment_dependencies.add_config_comments(dummy_config)
    for i, new_dependency in enumerate(new_config.get("transforms").get("depends_on")):
        assert (
            new_dependency == f"{old_dependencies[i]}\t# owned_by_{old_dependencies[i]}"
        )
