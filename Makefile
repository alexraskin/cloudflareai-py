PYTHON = python3
BLACK = black
TWINE = twine
SOURCE_DIR = cloudflareai/
BUILD_DIR = dist/

.PHONY: all clean build format upload

# Default target
all: format build

# Clean build artifacts
clean:
	@echo "Cleaning up build artifacts..."
	rm -rf $(BUILD_DIR)
	find . -type d -name '__pycache__' -exec rm -r {} +

# Format code with Black
format:
	@echo "Formatting code with Black..."
	$(BLACK) $(SOURCE_DIR)

# Build the package
build:
	@echo "Building the package..."
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "Build artifacts are in $(BUILD_DIR)"

# Upload the package to PyPI
upload:
	@echo "Uploading the package to PyPI..."
	$(TWINE) upload dist/*
