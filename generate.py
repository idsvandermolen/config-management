#!/usr/bin/env python3
"""
Generate manifests for a component
"""
import sys
from pathlib import Path
import shutil
import yaml
from datapath import DataPath

CONFIGS = Path("configs")
COMPONENTS = Path("components")
MANIFESTS = Path("manifests")


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
