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

test:
	@echo "Running test..."
	rm -f .coverage
	nosetests ./tests/
