# python_template

A starter template for Python projects: a package skeleton, `uv`-managed dependencies,
ruff linting enforced by tests, and GitHub Actions for testing, versioning, tagging,
and publishing to PyPI.

## Requirements

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Getting started

```bash
uv sync --all-extras
uv run python -m python_template --version
```

With pip instead:

```bash
python -m venv .venv
.venv\Scripts\activate.ps1      # Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
python -m python_template --version
```

## Layout

```
python_template/     Package source
  __main__.py        Module entrypoint (python -m python_template)
  main.py            Argument parsing and program entry
  constants.py       Shared constants
tests/               Pytest suite
.github/workflows/   CI: tests, version check, tagging, PyPI publish
VERSION.txt          Single source of truth for the version
CHANGELOG.md         Keep a Changelog style release notes
```

## Development

Run the tests:

```bash
uv run pytest .
```

Lint and format:

```bash
uv run ruff check .
uv run ruff format .
```

Linting is not optional — `tests/test_linting.py` fails the suite if the tree is
unformatted or has ruff errors that ruff could fix on its own. Ruff is configured in
`pyproject.toml` with a 120 character line length and the `E`, `F`, `I`, `PL`, and `UP`
rule sets.

## Releasing

Every pull request into `main` must bump the version and describe the change:

1. Bump `VERSION.txt` to a new semver string
2. Add a matching `## [x.y.z]` section to `CHANGELOG.md`

`version_check.yml` enforces both on every PR. Add the `skip-version-check` label to
bypass it for docs-only or CI-only changes.

Once the PR merges, `tag.yml` creates the `vx.y.z` tag and a GitHub Release using the
changelog section as the release notes. The tag push then triggers `publish.yml`, which
builds the distribution and publishes it to PyPI through the `pypi` environment using
trusted publishing.

## Using this template

Rename the `python_template` package directory, update the `name` field in
`pyproject.toml` (currently empty), and write an initial version into `VERSION.txt`.

## License

MIT — see [LICENSE](LICENSE).
