.PHONY: install test run

install:
	@python -c "import sys; assert sys.version_info >= (3, 10), 'Python 3.10+ required'; print('Standard library only: ready')"

test: install
	@python -m unittest discover -s tests -v

run:
	python -m app.server
