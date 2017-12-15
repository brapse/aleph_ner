test:
	PYTHONPATH="$PYTHONPATH:." py.test -s -v tests

.PHONY: test
