"""
Tests for the ``grid_version_badge`` module.
"""

import pathlib

import pytest

import grid_hooks.grid_version_badge as grid_version_badge

BADGE = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="71.1" height="20">
    <linearGradient id="smooth" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <clipPath id="round">
        <rect width="71.1" height="20" rx="3" fill="#fff"/>
    </clipPath>
    <g clip-path="url(#round)">
        <rect width="33.1" height="20" fill="#555"/>
        <rect x="33.1" width="38.0" height="20" fill="#007ec6"/>
        <rect width="71.1" height="20" fill="url(#smooth)"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="110">
        <text x="175.5" y="150" fill="#010101" fill-opacity=".3" transform="scale(0.1)" textLength="231.0" lengthAdjust="spacing">Grid</text>
        <text x="175.5" y="140" transform="scale(0.1)" textLength="231.0" lengthAdjust="spacing">Grid</text>
        <text x="511.0" y="150" fill="#010101" fill-opacity=".3" transform="scale(0.1)" textLength="280.0" lengthAdjust="spacing">1.2.3</text>
        <text x="511.0" y="140" transform="scale(0.1)" textLength="280.0" lengthAdjust="spacing">1.2.3</text>
    </g>
</svg>
"""


@pytest.fixture(scope="session")
def grid_project_root(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """
    Create a temporary directory corresponding to a Grid project.
    """
    return tmp_path_factory.mktemp("grid_project_root")


@pytest.fixture(scope="session")
def copier_answers_path(grid_project_root: pathlib.Path) -> pathlib.Path:
    """
    Create a temporary file with the copier answers.
    """
    answers = grid_project_root / ".copier-answers.yml"
    answers.write_text("_commit: 1.2.3")

    return answers


def test__main(
    monkeypatch: pytest.MonkeyPatch,
    grid_project_root: pathlib.Path,
    copier_answers_path: pathlib.Path,
) -> None:
    """
    Test the ``main`` function.
    """
    badge_path = grid_project_root / "grid-version.svg"

    monkeypatch.setattr(grid_version_badge, "DEFAULT_ANSWERS_PATH", copier_answers_path)
    monkeypatch.setattr(grid_version_badge, "DEFAULT_BADGE_PATH", badge_path)

    grid_version_badge.main()
    expected = BADGE.replace("\n", "").replace("    ", "")

    assert badge_path.read_text() == expected
