SHELL:=/bin/bash

.ONESHELL:

all: build

build: FORCE
	poetry build

requirements: FORCE
	poetry export --output requirements.txt



.PHONY: FORCE
FORCE:
