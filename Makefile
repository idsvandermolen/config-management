.PHONY: help
help:  ## Show help messages for make targets
	@awk 'BEGIN {FS = ":.*?## "}; /^[^: ]+:.*?## / {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: build
build: prometheus grafana validate ## Build all targets

.PHONY: bootstrap
bootstrap: ## Setup python .venv
	python3 -m venv .venv \
	&& .venv/bin/pip install --no-cache-dir --upgrade pip \
	&& . .venv/bin/activate \
	&& .venv/bin/pip install --no-cache-dir poetry \
	&& .venv/bin/poetry install --no-cache

.PHONY: clean
clean: ## Cleanup manifests
	@rm -rf manifests/*

.PHONY: prometheus
prometheus: ## Build prometheus
	@rm -rf manifests/*/prometheus
	@./generate.py prometheus

.PHONY: grafana
grafana: ## Build grafana
	@rm -rf manifests/*/grafana
	@./generate.py grafana

.PHONY: validate
validate: ## Validate manifests
	@kubeconform --verbose -skip Application manifests
