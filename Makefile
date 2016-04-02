SHELL := /bin/bash

all: clean setup test

clean:
	@echo "Removing junk..."
	rm -f .coverage
	rm -f *.txt~
	rm -f tests/*.py~
	rm -f pytchfork/*.py~

init:
	@echo "Building devmode..."
	python setup.py develop
	@echo "Building devmode..."
	pip install -r requirements.txt

setup:
	@echo "Installing package locally..."
	python setup.py install

install:
	@echo "Installing requirements..."
	pip install -r requirements.txt

publish: clean tag
	@if [ -e "$$HOME/.pypirc" ]; then \
                echo "Uploading to pypi"; \
                git stash
		python setup.py sdist upload \
		git stash apply
	else \
                echo "You should create a file called '.pypirc' under your home dir.\n"; \
		exit 1; \
        fi

tag:
	@if [ $$(git rev-list $$(git describe --abbrev=0 --tags)..HEAD --count) -gt 0 ]; then \
                if [ $$(git log  -n 1 --oneline $$(git describe --abbrev=0 --tags)..HEAD CHANGELOG.md | wc -l) -gt 0 ]; then \
                        git tag $$(python setup.py --version) && git push --tags || echo 'Version already released, update your version!'; \
                else \
                        echo "CHANGELOG not updated since last release!"; \
                        exit 1; \
                fi; \
        else \
                echo "No commits since last release!"; \
                exit 1;\
        fi

test:
	@echo "Running test..."
	rm -f .coverage
	python setup.py test
