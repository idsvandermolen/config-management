help:  ## Show help messages for make targets
	@grep -E '^[a-zA-Z0-9_-][^:]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

all: prometheus grafana ## Build all targets
.PHONY: all

prometheus: ## Build prometheus
	@rm -rf manifests/*/prometheus
	@./generate.py prometheus
.PHONY: prometheus

grafana: ## Build grafana
	@rm -rf manifests/*/grafana
	@./generate.py grafana
.PHONY: grafana

validate: ## Validate manifests
	@kubeconform --verbose manifests
.PHONY: validate
