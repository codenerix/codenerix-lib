.PHONY: default cleancache lint stopwords test coverage coverage_html tox precommit release-guards build-check publish

VERSION := $(shell grep -oP '__version__ = "\K[^"]+' codenerix_lib/__init__.py)

default: test

cleancache:
	-# Clean cache...
	@for d in __pycache__ .mypy_cache .pytest_cache .ruff_cache .cache .tox ; do \
		find . -type d -name "$$d" -exec rm -rf {} +; \
	done

lint:
	-# Lint and type checks, same commands as the CI workflow...
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy codenerix_lib
	uv run basedpyright codenerix_lib

stopwords:
	@# The tests need the NLTK stopwords corpus; download it only when missing.
	@# The downloader exits 0 even when the download fails, so find() decides.
	@uv run python -c "import nltk; nltk.data.find('corpora/stopwords')" 2>/dev/null || { \
		uv run python -m nltk.downloader -q stopwords && \
		uv run python -c "import nltk; nltk.data.find('corpora/stopwords')"; }

test: stopwords
	-# Run tests...
	uv run python -m pytest

coverage: stopwords
	-# Executing coverage...
	uv run coverage run -m pytest
	uv run coverage report -m

coverage_html: coverage
	-# Prepare coverage HTML report...
	uv run coverage html
	xdg-open htmlcov/index.html 2>/dev/null 1>&2 || true

tox:
	-# Run tests in all environments...
	uv run tox

precommit:
	uv run pre-commit run -a

release-guards:
	-# Pre-flight checks for $(VERSION)...
	@test -n "$(VERSION)" || { echo "ERROR: could not read __version__"; exit 1; }
	@if git rev-parse "v$(VERSION)" >/dev/null 2>&1; then \
		echo "ERROR: tag v$(VERSION) already exists locally (forgot to bump __version__?)"; exit 1; fi
	@if git ls-remote --tags --exit-code origin "refs/tags/v$(VERSION)" >/dev/null 2>&1; then \
		echo "ERROR: tag v$(VERSION) already exists on origin (forgot to bump __version__?)"; exit 1; fi
	@grep -q "^## \[$(VERSION)\]" CHANGELOG || { \
		echo "ERROR: no CHANGELOG entry for $(VERSION)"; exit 1; }
	@# `git commit -am` below only picks up TRACKED files, so an untracked file
	@# that belongs in the release would be silently left out of it.
	@untracked=$$(git ls-files --others --exclude-standard); \
	 if [ -n "$$untracked" ]; then \
		echo "ERROR: untracked files present -- git add them, or add them to .gitignore:"; \
		echo "$$untracked" | sed 's/^/  /'; exit 1; fi
	@echo "OK: $(VERSION) ready (tag free locally and on origin, changelog present, no untracked files)"

build-check:
	-# Local build and wheel content verification...
	@rm -rf dist
	uv build
	@# Same guard as release.yml: the wheel must ship the PEP 561 marker
	@unzip -l dist/*.whl | grep -q 'codenerix_lib/py.typed' || { \
		echo "ERROR: wheel is missing codenerix_lib/py.typed"; exit 1; }
	@echo "OK: wheel ships codenerix_lib/py.typed"

publish: release-guards lint test build-check
	-# Commit, tag and push $(VERSION)...
	@# Skip the commit when the version bump is already committed
	git diff --quiet HEAD || git commit -am "Release $(VERSION)"
	@# Annotated tag, so the release notes live in the tag itself. The message
	@# is the CHANGELOG section for this version, which release-guards already
	@# verified is present.
	@awk '/^## \[$(VERSION)\]/{f=1;print;next} f&&/^## \[/{exit} f' CHANGELOG > .tagmsg
	git tag -a "v$(VERSION)" -F .tagmsg
	@rm -f .tagmsg
	git push origin master --tags
	-# Wait for CI on the pushed commit BEFORE publishing anything...
	@# The local gate only covers one Python; CI runs the whole matrix. A red
	@# CI must stop the release, not be discovered after it is public.
	@# `// empty` matters: without it jq prints the literal string "null" when
	@# no run exists yet, the -n test passes and the loop breaks on the very
	@# race it is here to absorb.
	@sha=$$(git rev-parse HEAD); \
	 echo "Waiting for a CI run on $$sha..."; \
	 for i in $$(seq 1 30); do \
		id=$$(gh run list --commit "$$sha" --workflow CI --limit 1 \
			--json databaseId --jq '.[0].databaseId // empty' 2>/dev/null); \
		[ -n "$$id" ] && break; \
		sleep 5; \
	 done; \
	 test -n "$$id" || { echo "ERROR: no CI run found for $$sha after 150s"; exit 1; }; \
	 gh run watch "$$id" --exit-status
	-# CI is green, publish the release (this triggers the PyPI workflow)...
	gh release create "v$(VERSION)" --title "$(VERSION)" --notes-from-tag
	-# Wait for the PyPI publish run, matched to this commit...
	@# Bare `gh run watch` looks at whatever is in progress right now, so just
	@# after creating the release it finds nothing, prints "found no in progress
	@# runs to watch" and exits 0 -- success that was never checked. Poll for
	@# the Release run whose head commit is ours instead.
	@sha=$$(git rev-parse HEAD); \
	 echo "Waiting for the Release run on $$sha..."; \
	 for i in $$(seq 1 30); do \
		id=$$(gh run list --workflow Release --event release --limit 10 \
			--json databaseId,headSha \
			--jq "[.[] | select(.headSha==\"$$sha\")] | .[0].databaseId // empty" \
			2>/dev/null); \
		[ -n "$$id" ] && break; \
		sleep 5; \
	 done; \
	 test -n "$$id" || { echo "ERROR: no Release run found for $$sha after 150s"; exit 1; }; \
	 gh run watch "$$id" --exit-status
