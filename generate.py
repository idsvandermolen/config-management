#!/usr/bin/env python3
"""
Generate manifests for a component
"""
import sys
from pathlib import Path
import yaml
from lib.datapath import DataPath
from lib.kibana import generate as generate_kibana
from lib.logstash import generate as generate_logstash

CONFIGS = Path("configs")
COMPONENTS = Path("components")
MANIFESTS = Path("manifests")
GENERATORS = {
    "kibana": generate_kibana,
    "logstash": generate_logstash,
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
    for env in ("development", "production"):
        config = DataPath(
            yaml.safe_load(Path(CONFIGS / f"{env}.yaml").open(encoding="utf-8"))
        )
        for stack_name in config["stacks"]:
            if component_name not in config[f"stacks.{stack_name}"]:
                continue
            generate(COMPONENTS, MANIFESTS, config, stack_name)


if __name__ == "__main__":
    main(sys.argv)
