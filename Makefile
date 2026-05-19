PREFIX ?= $(HOME)/.local
BINDIR ?= $(PREFIX)/bin
TARGET ?= ztypy
INSTALL_PATH := $(BINDIR)/$(TARGET)
PROJECT_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3

.PHONY: install uninstall

install:
	@mkdir -p "$(BINDIR)"
	@printf '%s\n' '#!/usr/bin/env bash' > "$(INSTALL_PATH)"
	@printf '%s\n' '$(PYTHON) "$(PROJECT_ROOT)/main.py" "$$@"' >> "$(INSTALL_PATH)"
	@chmod +x "$(INSTALL_PATH)"
	@echo "Installed $(TARGET) to $(INSTALL_PATH)"

uninstall:
	@rm -f "$(INSTALL_PATH)"
	@echo "Removed $(INSTALL_PATH)"
