.ONESHELL:
.PHONY: clean help install venv

help:
	@echo "Comand Toolkits makefile"
	@echo
	@echo "Usage: make <target>"
	@echo "Targets avaliable:"
	@echo "  clean       Remove nnecessary files and folders."
	@echo "  help        Help interface."
	@echo "  install     Install project in editable mode."
	@echo "  venv        Create virtual environment."
	@echo "  venv-deps   Install deps from requirements.txt."

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete


venv:
	@rm -rf .venv
	@python3 -m venv .venv
	@.venv/bin/pip config --site --quiet set global.index-url "https://mirrors.cloud.tencent.com/pypi/simple"
	@.venv/bin/pip install -U pip


deps: requirements.txt
	@.venv/bin/pip install -r requirements.txt

test:


install:
	@.venv/bin/pip install -e .
