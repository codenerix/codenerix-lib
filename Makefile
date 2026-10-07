.PHONY: default cleancache lint stopwords test coverage coverage_html tox precommit

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
