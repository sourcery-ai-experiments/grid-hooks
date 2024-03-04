"""
Pull the Grid template version number from the copier answers and save
it as a badge.

Inspired by:

- https://github.com/dbrgn/coverage-badge
"""

import pathlib

import pybadges
import yaml

# In the calling project
DEFAULT_ANSWERS_PATH = pathlib.Path(".copier-answers.yml")
DEFAULT_BADGE_PATH = pathlib.Path("grid-version.svg")


def _get_version(path: pathlib.Path) -> str:
    copier_answers = yaml.safe_load(path.read_text())

    return copier_answers["_commit"]


def _save_badge(version: str, target: pathlib.Path) -> None:
    """
    Save the badge to the specified path.
    """
    badge = pybadges.badge(left_text="Grid", right_text=version)
    target.write_text(badge, encoding="utf-8")


def main() -> None:
    """
    Save the Grid template version number as a badge.
    """
    version = _get_version(DEFAULT_ANSWERS_PATH)
    _save_badge(version, DEFAULT_BADGE_PATH)
