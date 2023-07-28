# SRC: https://github.com/aiogram/magic-filter/blob/3c5e38fd5cd359fd961e26bab17e65201b02c1c6/Makefile
.DEFAULT_GOAL := help

py := poetry run
python := $(py) python

reports_dir := reports

package_dir := app
code_dir := $(package_dir) tests

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo " - help            : Show this help message"
	@echo " - reformat        : Reformat code using isort and black"
	@echo " - lint            : Run linters: isort, black, flake8, mypy"
	@echo " - test            : Run tests"
	@echo " - pre             : Run reformat and lint. Use it before commit"
	@echo " - generate_env    : Generated example.env file"
	@echo " - generate_stub   : Generate fluent stub file"
	@echo " - watch_stub      : Generate fluent stub file and watch for changes"


# =================================================================================================
# Code quality
# =================================================================================================

isort:
	$(py) isort $(code_dir)

black:
	$(py) black $(code_dir)

flake8:
	$(py) flake8 $(code_dir)

flake8-report:
	mkdir -p $(reports_dir)/flake8
	$(py) flake8 --format=html --htmldir=$(reports_dir)/flake8 $(code_dir)

mypy:
	$(py) mypy $(package_dir)

mypy-report:
	$(py) mypy $(package_dir) --html-report $(reports_dir)/typechecking

lint:
	$(py) isort --check-only $(code_dir)
	$(py) black --check --diff $(code_dir)
	$(py) flake8 $(code_dir)

reformat:
	$(py) isort $(code_dir)
	$(py) black $(code_dir)

pre: reformat lint

# =================================================================================================
# Tests
# =================================================================================================

test:
	$echo "Tests are not implemented yet"

# =================================================================================================
# Other
# =================================================================================================
generate_env:
	$(python) -m app.config_reader

generate_stub:
	$(python) -m fluentogram -dir-ftl ./app/services/fluent/locales/ru -stub fluent_stub.pyi

stub: generate_stub  # Alias for generate_stub

watch_stub:
	$(python) -m fluentogram -dir-ftl ./app/services/fluent/locales/ru -stub fluent_stub.pyi -track-ftl ./app/services/fluent/locales/ru

# =================================================================================================
# Docker compose related
# =================================================================================================
postgres-shell:
	docker compose exec -it postgres psql -U postgres

redis-shell:
	docker compose exec -it redis redis-cli
