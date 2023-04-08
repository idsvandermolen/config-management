#!/usr/bin/env python3
"""
Load Stack Registry
"""
from pathlib import Path
from ruamel.yaml import YAML


def get_registry(path: str):
    "Load Stack Registry from path."
    yaml = YAML()
    registry = {}
    for filename in Path(path).glob("*.yaml"):
        registry[filename.stem] = yaml.load(filename.open(encoding="utf-8"))

    return registry
