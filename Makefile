# Developing
install-all:
	poetry install --with dev

format-code:
	isort . --skip docs && black . --exclude docs

update-deps:
	poetry update
	poetry export --without-hashes -f requirements.txt --output requirements.txt
	poetry export --without-hashes --with dev -f requirements.txt --output requirements-dev.txt

serve-docs:
	mkdocs serve

pytest:
	python -m pytest
