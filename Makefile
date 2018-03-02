all:
	tox -e py36,coverage
	flake8 tests syncr_tracker
	pycodestyle tests syncr_tracker

clean-test:
	rm -rf .tox/
