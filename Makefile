# Makefile to install OpenCV and Pygame in a virtual environment

# Define the Python environment and packages
VENV_DIR := .venv
PYTHON := python3
PIP := $(VENV_DIR)/bin/pip
REQ_FILE := requirements.txt

# Target to create a virtual environment
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)

# Target to install required packages
install: $(VENV_DIR) $(REQ_FILE)
	$(PIP) install -r $(REQ_FILE)

# Target to create a requirements file with OpenCV and Pygame
$(REQ_FILE):
	@echo "opencv-python" > $(REQ_FILE)
	@echo "pygame" >> $(REQ_FILE)
	@echo "numpy" >> $(REQ_FILE)

# Target to check if the installation was successful
check:
	$(VENV_DIR)/bin/python -c "import cv2; print('OpenCV installed successfully')"
	$(VENV_DIR)/bin/python -c "import pygame; print('Pygame installed successfully')"
	$(VENV_DIR)/bin/python -c "import numpy; print('numpy installed successfully')"

# Clean up virtual environment and requirements file
clean:
	rm -rf $(VENV_DIR) $(REQ_FILE)

# Default target
all: install check

