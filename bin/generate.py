#!/usr/bin/env python3
"""
Generate manifests for a component
"""
import sys
from pathlib import Path
import shutil
import yaml

CONFIGS = Path("configs")
COMPONENTS = Path("components")
MANIFESTS = Path("manifests")


def parse_path(path: str, delimiter: str = "."):
    "Parse path into list of strings and integers."
    out = []
    if path:
        # "".split(".") -> [""]
        for segment in path.split(delimiter):
            if segment.startswith('"') and segment.endswith('"'):
                out.append(segment[1:-1])
                continue
            try:
                out.append(int(segment))
            except ValueError as _:
                out.append(segment)
    return out


def find(data, path: list):
    "Find path in data."
    ref = data
    for segment in path[:-1]:
        ref = ref[segment]
    key = path[-1]

    return ref, key


class DataPath:
    "Access data with path spec."

    def __init__(self, data):
        "Initialise with data object."
        self.data = data

    def __getitem__(self, path):
        "Return data at path."
        ref, key = find(self.data, parse_path(path))
        return ref[key]

    def __setitem__(self, path, value):
        "Set data at path to value."
        ref, key = find(self.data, parse_path(path))
        ref[key] = value

    def __delitem__(self, path):
        ref, key = find(self.data, parse_path(path))
        del ref[key]

    def __repr__(self):
        "Return repr(self)."
        return f"DataPath({repr(self.data)})"


def generate_kibana(config, stack_name: str):
    "Generate kibana manifests."
    home = COMPONENTS / "kibana"
    output_dir = Path(MANIFESTS, stack_name, "kibana")
    output_dir.mkdir(parents=True, exist_ok=True)
    # deployment
    deployment = DataPath(
        yaml.safe_load(Path(home, "deployment.yaml").open(encoding="utf-8"))
    )
    deployment["spec.template.spec.containers.0.resources"] = config[
        f"stacks.{stack_name}.kibana.resources"
    ]
    yaml.safe_dump(
        deployment.data,
        Path(output_dir / "deployment.yaml").open("w", encoding="utf-8"),
    )
    # hpa
    hpa = DataPath(
        yaml.safe_load(Path(home, "hpa.yaml").open(encoding="utf-8"))
    )
    hpa["spec.minReplicas"] = config[f"stacks.{stack_name}.kibana.minReplicas"]
    hpa["spec.maxReplicas"] = config[f"stacks.{stack_name}.kibana.maxReplicas"]
    yaml.safe_dump(hpa.data, Path(output_dir / "hpa.yaml").open("w", encoding="utf-8"))
    # service
    shutil.copy(home / "service.yaml", output_dir / "service.yaml")
    # service-account
    shutil.copy(home / "service-account.yaml", output_dir / "service-account.yaml")


def generate_logstash(config, stack_name: str):
    "Generate logstash manifests."
    home = COMPONENTS / "logstash"
    output_dir = Path(MANIFESTS, stack_name, "logstash")
    output_dir.mkdir(parents=True, exist_ok=True)
    # deployment
    deployment = DataPath(
        yaml.safe_load(Path(home, "deployment.yaml").open(encoding="utf-8"))
    )
    deployment["spec.template.spec.containers.0.resources"] = config[
        f"stacks.{stack_name}.logstash.resources"
    ]
    yaml.safe_dump(
        deployment.data,
        Path(output_dir / "deployment.yaml").open("w", encoding="utf-8"),
    )
    # hpa
    hpa = DataPath(
        yaml.safe_load(Path(home, "hpa.yaml").open(encoding="utf-8"))
    )
    hpa["spec.minReplicas"] = config[f"stacks.{stack_name}.logstash.minReplicas"]
    hpa["spec.maxReplicas"] = config[f"stacks.{stack_name}.logstash.maxReplicas"]
    yaml.safe_dump(hpa.data, Path(output_dir / "hpa.yaml").open("w", encoding="utf-8"))
    # service-account
    shutil.copy(home / "service-account.yaml", output_dir / "service-account.yaml")


def usage():
    "Print usage message and exit."
    print(f"usage: {sys.argv[0]} <component>", file=sys.stderr)
    sys.exit(1)


def main(argv):
    "Main."
    if len(argv) != 2:
        usage()
    component = argv[1]
    for env in ("development", "production"):
        config = DataPath(
            yaml.safe_load(Path(CONFIGS / f"{env}.yaml").open(encoding="utf-8"))
        )
        for stack_name in config["stacks"]:
            if component not in config[f"stacks.{stack_name}"]:
                continue
            if component == "kibana":
                generate_kibana(config, stack_name)
            if component == "logstash":
                generate_logstash(config, stack_name)


if __name__ == "__main__":
    main(sys.argv)
