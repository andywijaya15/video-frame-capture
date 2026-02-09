# Nama venv
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

# Script utama
SCRIPT = src/main.py

.PHONY: all venv install run clean

# Default target
all: run

# Buat venv
venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)"

# Install dependencies
install: venv
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed"

# Jalankan script
run: install
	@echo "Running script..."
	$(PYTHON) $(SCRIPT)

# Bersih-bersih
clean:
	@echo "Removing venv and __pycache__..."
	rm -rf $(VENV_DIR) __pycache__ src/__pycache__
	@echo "Clean done"
