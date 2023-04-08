#!/usr/bin/env python3
"""
Generate manifests for a component
"""
import sys
import os
from pathlib import Path
from datapath import DataPath
from lib.grafana import generate as generate_grafana
from lib.prometheus import generate as generate_prometheus
from lib.stack_registry import get_registry

CONFIGS = Path(os.environ.get("CONFIGS"))
MANIFESTS = Path(os.environ.get("OUTPUT_DIR"))
COMPONENTS = Path(os.environ.get("COMPONENTS"))
GENERATORS = {
    "grafana": generate_grafana,
    "prometheus": generate_prometheus,
}


def usage():
    "Print usage message and exit."
    print(f"usage: {sys.argv[0]} [{','.join(GENERATORS.keys())}]", file=sys.stderr)
    sys.exit(1)


def main(argv):
    "Main."
    if len(argv) != 2:
        usage()
    component_name = argv[1]
    if component_name not in GENERATORS:
        usage()
    generate = GENERATORS[component_name]
    stack_registry = DataPath(get_registry(CONFIGS))
    for env in stack_registry:
        for stack_name in stack_registry[f"{env}.stacks"]:
            if component_name not in stack_registry[f"{env}.stacks.{stack_name}"]:
                continue
            generate(MANIFESTS, COMPONENTS, DataPath(stack_registry[f"{env}.stacks"]), stack_name)


if __name__ == "__main__":
    main(sys.argv)
