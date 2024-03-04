<div align="center">

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![coverage](https://raw.githubusercontent.com/Bilbottom/grid-hooks/main/coverage.svg)](https://github.com/dbrgn/coverage-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/Bilbottom/grid-hooks)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

</div>

---

# Grid Hooks

Pre-commit hooks for Grid.

## Usage

Add the following hook to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/Bilbottom/grid-hooks
  rev: v0.0.1
  hooks:
    - id: version-badge
      name: Add Grid version badge
```

This will generate an SVG for the badge which you can then add to your README.md.
