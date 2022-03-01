.ONESHELL:
.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint venv
.DEFAULT_GOAL := help
PYTHONVENV ?= .venv
BINDIR := $(PYTHONVENV)/bin
PYTHON := $(BINDIR)/python


define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := $(PYTHON) -c "$$BROWSER_PYSCRIPT"

help:
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache


docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/pycmd.rst
	rm -f docs/modules.rst
	$(BINDIR)/sphinx-apidoc -o docs/ pycmd
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	$(BINDIR)/watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

coverage: ## check code coverage quickly with the default Python
	@$(BINDIR)/coverage run --source pycmd -m pytest
	@$(BINDIR)/coverage report -m
	@$(BINDIR)/coverage html
	@$(BROWSER) htmlcov/index.html


format: ## format style with isort, black
	$(BINDIR)/isort --profile=black --lines-after-imports=2 pycmd tests
	$(BINDIR)/black pycmd tests

lint: ## check style with isort, black, flake8, bandit
	$(BINDIR)/isort --profile=black --lines-after-imports=2 --check-only pycmd tests
	$(BINDIR)/black --check pycmd tests
	$(BINDIR)/flake8 pycmd tests
	$(BINDIR)/bandit -r pycmd

test: ## run tests quickly with the default Python
	$(PYTHON) -m pytest

test-all: ## run tests on every Python version with tox
	$(BINDIR)/tox

dist: clean ## builds source and wheel package
	$(PYTHON) -m setup sdist
	$(PYTHON) -m setup bdist_wheel
	ls -l dist

release: dist ## package and upload a release
	$(BINDIR)/twine upload dist/*

install: clean ## install the package to the active Python's site-packages
	$(PYTHON) -m pip install .

pre-commit: ## install pre-commit hook into .git
	$(BINDIR)/pre-commit install

venv: ## create virtual environment, install dev requirements
	@test -d .venv || python3 -m venv .venv
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -r requirements_dev.txt
