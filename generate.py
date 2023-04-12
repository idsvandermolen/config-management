#!/usr/bin/env python3
"""
Generate manifests for a component
"""
import sys
from pathlib import Path
from ruamel.yaml import YAML
from datapath import DataPath
from lib.grafana import generate as generate_grafana
from lib.prometheus import generate as generate_prometheus


def usage():
    "Print usage message and exit."
    print(
        f"usage: {sys.argv[0]} <stack registry filename> <output dir>", file=sys.stderr
    )
    sys.exit(1)


def main(argv):
    "Main."
    if len(argv) != 3:
        usage()
    yaml = YAML()
    with Path(argv[1]).open(encoding="utf-8") as fp:
        stack_registry = DataPath(yaml.load(fp))
        generate_grafana(stack_registry, argv[2])
        generate_prometheus(stack_registry, argv[2])


if __name__ == "__main__":
    main(sys.argv)
