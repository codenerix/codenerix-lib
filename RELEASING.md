# Releasing codenerix-lib

This document describes how to cut and publish a new release of
`codenerix-lib` to PyPI. The process is the same as in `django-codenerix`.

## How it works

- **Single source of truth for the version:** `codenerix_lib/__init__.py`
  (`__version__ = "X.Y.Z"`). Hatchling reads it at build time via
  `[tool.hatch.version]`.
- **Releases are driven by Git tags + GitHub Releases.** Publishing a
  GitHub Release triggers `.github/workflows/release.yml`, which builds
  the sdist + wheel and uploads them to PyPI.
- **No tokens or secrets.** Publishing uses PyPI Trusted Publishing
  (OIDC): the workflow proves its identity to PyPI with a short-lived
  token that only exists during the run.

The release workflow enforces two guards and refuses to publish if either
fails:

1. **Tag matches `__version__`** — the tag (`vX.Y.Z`) must match the
   version string in `codenerix_lib/__init__.py`.
2. **`py.typed` is bundled** — the wheel must contain
   `codenerix_lib/py.typed`, or downstream type checkers silently stop
   seeing the package's annotations.

## One-time setup

Done once per project; you do **not** repeat this for each release.

1. **PyPI Trusted Publisher.** On PyPI, go to the project
   (`codenerix-lib`) then *Settings → Publishing → Add a new
   publisher*, and register:
   - Owner: `codenerix`
   - Repository: `codenerix-lib`
   - Workflow: `release.yml`
   - Environment: `pypi`
2. **GitHub environment.** In GitHub, go to *Settings → Environments* and
   create an environment named `pypi`. Optionally add required reviewers
   there to require manual approval before each publish.

## Cutting a release

1. **Bump the version** in `codenerix_lib/__init__.py`.
2. **Update the changelog.** Add a `## [X.Y.Z] - YYYY-MM-DD` entry to
   `CHANGELOG`.
3. **Publish:**

   ```bash
   make publish
   ```

`make publish` runs, in order, stopping at the first failure:

1. `release-guards`: the version is readable, the tag `vX.Y.Z` exists
   neither locally nor on origin, `CHANGELOG` has an entry for it, and
   there are no untracked files.
2. `lint` (ruff, mypy, basedpyright), `test` and `build-check` (local
   build plus the `py.typed` guard).
3. Commits the pending changes as `Release X.Y.Z` (skipped if the bump is
   already committed), creates the annotated tag `vX.Y.Z` with the
   `CHANGELOG` section as its message, and pushes `master` and the tag.
4. Waits for the CI run on that commit and stops if it is not green.
5. Creates the GitHub Release from the tag, which triggers
   `release.yml`, and follows that run until it finishes.

A green Release run means it is live on PyPI:
<https://pypi.org/project/codenerix-lib/>

## Versioning convention

Semantic versioning, `MAJOR.MINOR.PATCH`:

- **PATCH** — bug fixes, no API changes.
- **MINOR** — new backwards-compatible features, or behaviour changes that
  need action from users (documented in `CHANGELOG`).
- **MAJOR** — backwards-incompatible changes.

The Git tag is always `v` + the version (e.g. `v1.1.0`).

## Building locally (no publish)

```bash
make build-check
```

## Troubleshooting

- **I pushed the tag but nothing was published.** The tag push does not
  trigger anything on its own. The workflow runs on the *release
  published* event, so a GitHub Release must be created **and published**
  from the tag (`gh release create vX.Y.Z --notes-from-tag`, or the web
  UI). A *draft* release also does nothing until published.
- **Workflow fails on "Tag must match `__version__`".** You tagged a
  version that does not match `codenerix_lib/__init__.py`. Fix the version
  string (or the tag) so they agree, then re-tag.
- **Workflow fails on "Verify py.typed is bundled".** Check
  `[tool.hatch.build.targets.wheel]` in `pyproject.toml`.
- **`uv publish` is rejected by PyPI.** The Trusted Publisher config on
  PyPI does not match this repo/workflow/environment. Re-check owner,
  repository, workflow filename, and environment name.
