OUTPUT_DIR = dist
DEV_OUTPUT_DIR = $(OUTPUT_DIR)/development
PRD_OUTPUT_DIR = $(OUTPUT_DIR)/production
STACK_REGISTRY = stack-registry
DEV_REGISTRY = $(STACK_REGISTRY)/development.yaml
PRD_REGISTRY = $(STACK_REGISTRY)/production.yaml
.PHONY: help
help:  ## Show help messages for make targets
	@awk 'BEGIN {FS = ":.*?## "}; /^[^: ]+:.*?## / {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: bootstrap
bootstrap: ## Setup python .venv
	python3 -m venv .venv \
	&& .venv/bin/pip install --no-cache-dir --upgrade pip \
	&& . .venv/bin/activate \
	&& poetry install --no-cache

.PHONY: all
all: test build validate ## Test, build and validate

.PHONY: build
build: development production ## Build all targets

.PHONY: development
development:
	@./generate.py $(DEV_REGISTRY) $(DEV_OUTPUT_DIR)

.PHONY: production
production:
	@./generate.py $(PRD_REGISTRY) $(PRD_OUTPUT_DIR)

.PHONY: validate
validate: validate_dev validate_prd ## Validate manifests

.PHONY: validate_dev
validate_dev:
	@kubeconform --verbose -skip Application $(DEV_OUTPUT_DIR)

.PHONY: validate_prd
validate_prd:
	@kubeconform --verbose -skip Application $(PRD_OUTPUT_DIR)

.PHONY: test
test: ## Run test suite
	@pytest

.PHONY: clean
clean: ## Cleanup manifests
	@rm -rf ./$(OUTPUT_DIR)/*
