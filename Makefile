.PHONY: default
default:
	make test

.PHONY: test
test:
	(. ./venv/bin/activate && python -m pytest -s -vv tests)

.PHONY: coverage
coverage:
	-### Executing coverage...
	(. ./venv/bin/activate && coverage run -m pytest tests)
	make coverage_report

.PHONY: coverage_report
coverage_report:
	(. ./venv/bin/activate && coverage html)
	open htmlcov/index.html 2>/dev/null 1>&2

.PHONY: tox
tox:
	(. ./venv/bin/activate && python -m tox)

.PHONY: prepare
prepare:
	sudo apt-get -y install python3-pip python3-virtualenv

.PHONY: venv
venv:
	test ! -f venv && virtualenv -p python3 venv || true
	(. ./venv/bin/activate && pip install -r requirements-dev.txt)

.PHONY: requirements
requirements:
	@rm -f requirements*.txt
	@pip-compile requirements.in
	@pip-compile requirements-dev.in

.PHONY: syncrequirements
syncrequirements: requirements
	(. ./venv/bin/activate && pip-sync requirements*.txt)

.PHONY: deps
deps:
	python3 -c 'import pathlib, pkg_resources; requirements_txt=pathlib.Path("requirements.txt").open(); install_requires = [str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)]; requirements_txt.close(); print(install_requires)'

.PHONY: precommit
precommit:
	pre-commit run -a
