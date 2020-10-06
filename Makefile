.PHONY: build deploy help

default: build

build:  ## Generate a source distribution tarball
	python setup.py sdist

docs:  datastructure.py  ## Generate docs in Markdown
	pdoc datastructure.py > docs.md

help: ## Show this help message
	@echo "Usage:"
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'