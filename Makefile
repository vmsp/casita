dev: requirements.txt requirements-dev.txt
	pip-sync $^

requirements.txt: requirements.in
	pip-compile --generate-hashes $<

requirements-dev.txt: requirements-dev.in
	pip-compile --generate-hashes $<

.PHONY: dev
