# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./pythonenv/bin:$(PATH)

default: dependencies check test

check:
	-find rewards -name '*.py' | xargs pep8
	-pylint rewards

test:
	python manage.py test --verbosity=1 rewards

dependencies:
	virtualenv pythonenv
	pip -q install -E pythonenv -r requirements.txt
	./pythonenv/bin/python manage.py syncdb

build:
	python setup.py build sdist

upload: build
	sudo python setup.py sdist upload

install: build
	sudo python setup.py install

runserver:
	python manage.py runserver

clean:
	rm -Rf pythonenv build dist html test.db sloccount.sc pylint.out
	find . -name '*.pyc' -or -name '*.pyo' -delete

.PHONY: test build clean install upload check statistics dependencies
