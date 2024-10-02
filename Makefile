SHELL:=/bin/bash

.ONESHELL:

include .env
export $(shell sed 's/=.*//' .env)


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

publish: FORCE build
	poetry publish

.PHONY: FORCE
FORCE:
