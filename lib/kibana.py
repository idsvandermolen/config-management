"""
Generate Kibana components
"""
from pathlib import Path
import shutil
import yaml
from .datapath import DataPath


def generate(components: Path, manifests: Path, config: DataPath, stack_name: str):
    "Generate kibana manifests."
    home = components / "kibana"
    output_dir = Path(manifests, stack_name, "kibana")
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
    hpa = DataPath(yaml.safe_load(Path(home, "hpa.yaml").open(encoding="utf-8")))
    hpa["spec.minReplicas"] = config[f"stacks.{stack_name}.kibana.minReplicas"]
    hpa["spec.maxReplicas"] = config[f"stacks.{stack_name}.kibana.maxReplicas"]
    yaml.safe_dump(hpa.data, Path(output_dir / "hpa.yaml").open("w", encoding="utf-8"))
    # service
    shutil.copy(home / "service.yaml", output_dir / "service.yaml")
    # service-account
    shutil.copy(home / "service-account.yaml", output_dir / "service-account.yaml")
