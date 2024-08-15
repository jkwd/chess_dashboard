.PHONY: run clean

VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

venv: clean
	@echo "Creating a new virtual environment..."
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate
	$(PIP) install -e ".[dev]"
	@echo "Virtual environment created and packages installed."
	which python
	which dagster

up: $(VENV)/bin/activate
	dagster dev

test: $(VENV)/bin/activate
	pytest chess_tests

clean:
	rm -rf $(VENV)

jupyter:
	jupyter notebook