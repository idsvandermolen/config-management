"""
Generate Logstash components
"""
from pathlib import Path
import shutil
import yaml
from .datapath import DataPath


def generate(src: Path, dst: Path, config: DataPath, stack_name: str):
    "Generate logstash manifests."
    home = src / "logstash"
    output_dir = Path(dst, stack_name, "logstash")
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
    hpa = DataPath(yaml.safe_load(Path(home, "hpa.yaml").open(encoding="utf-8")))
    hpa["spec.minReplicas"] = config[f"stacks.{stack_name}.logstash.minReplicas"]
    hpa["spec.maxReplicas"] = config[f"stacks.{stack_name}.logstash.maxReplicas"]
    yaml.safe_dump(hpa.data, Path(output_dir / "hpa.yaml").open("w", encoding="utf-8"))
    # service-account
    shutil.copy(home / "service-account.yaml", output_dir / "service-account.yaml")
