lint:
	pep8 ./robostrippy
	find ./robostrippy -name '*.py' | xargs pyflakes
