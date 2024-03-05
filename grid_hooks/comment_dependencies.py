import logging
import os
import pathlib
import typing as t

import github
import yaml

ORG_NAME = "sainsburys-tech"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
DEFAULT_COPIER_NAME = ".copier-answers.yml"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_config_contents(path: pathlib.Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            "Pre-commit passed a filename I could not find. Something has gone wrong"
        )

    contents = yaml.safe_load(path.read_text(encoding="utf-8"))
    if contents.get("transforms") is None:
        raise KeyError("File passed is not a valid Grid config")

    return contents


def get_grid_process_owner(grid_set_name: str) -> t.Optional[str]:
    if grid_set_name.lower().startswith("ext_"):
        logger.info(f"Set {grid_set_name} is an external grid process. Ignoring it.")
        return

    if GITHUB_TOKEN is None:
        raise OSError(
            "Please add a github token to your environment under the key GITHUB_TOKEN"
        )
    # We can check this from Grid-API instead (and include external processes there)

    g = github.Github(auth=github.Auth.Token(GITHUB_TOKEN))
    repo = g.get_repo(f'{ORG_NAME}/{grid_set_name.replace("_", "-")}')
    copier_file = repo.get_contents(DEFAULT_COPIER_NAME)
    copier_yaml = yaml.safe_load(copier_file.decoded_content)
    return copier_yaml.get("squad_name") or copier_yaml.get("squad_email")


def add_config_comments(config: dict) -> dict:
    dependencies = list(config.get("transforms").get("depends_on"))
    commented_dependencies = [
        f"{dependency}\t# {get_grid_process_owner(grid_set_name=dependency)}"
        for dependency in dependencies
    ]

    config["transforms"]["depends_on"] = commented_dependencies
    return config


def _comment_dependencies(filepaths: list[pathlib.Path]) -> None:
    for path in filepaths:
        if isinstance(path, str):
            path = pathlib.Path(path)

        config = get_config_contents(path)
        if config.get("transforms").get("depends_on") is None:
            logger.debug(f"File {path} has no depends_on block, skipping this file")
            continue

        config = add_config_comments(config=config)

        path.write_text(yaml.dump(config))


def main(filepaths: list[pathlib.Path]) -> None:
    # Handling depending on how pre-commit passes names in
    if not isinstance(filepaths, list):
        filepaths = [filepaths]
    _comment_dependencies(filepaths=filepaths)
