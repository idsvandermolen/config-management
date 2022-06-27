help:  ## Show help messages for make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

all: logstash kibana ## Build all targets
.PHONY: all

logstash: ## Build logstash
	@rm -rf manifests/*/logstash
	@bin/generate.py logstash
.PHONY: logstash

kibana: ## Build kibana
	@rm -rf manifests/*/kibana
	@bin/generate.py kibana
.PHONY: kibana

validate: ## Validate manifests
	@kubeconform --verbose manifests
.PHONY: validate
