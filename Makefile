SHELL:=/bin/bash

.ONESHELL:

all: build

build: FORCE setup
	poetry build

setup: FORCE
	poetry install

test: FORCE
	pytest -v

shell: FORCE
	poetry shell

requirements: FORCE
	poetry export --output requirements.txt

.PHONY: FORCE
FORCE:
