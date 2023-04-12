"""
Generate Grafana components
"""
from pathlib import Path
import kubernetes.client as k
from ruamel.yaml import YAML
from datapath import DataPath
from . import util


def generate_stack(dest: Path, stack_registry: DataPath, stack_name: str):
    "Generate stack manifests configured in stack_registry into dest."
    output_dir = Path(dest, stack_name, "grafana")
    output_dir.mkdir(parents=True, exist_ok=True)
    client = k.ApiClient()
    name = stack_registry.get(f"stacks.{stack_name}.grafana.name", "grafana")
    port = stack_registry.get(f"stacks.{stack_name}.grafana.port", 3000)
    port_name = "ui"
    # deployment
    image = stack_registry.get(
        f"stacks.{stack_name}.grafana.image", "grafana/grafana:latest"
    )
    requests = stack_registry.get(
        f"stacks.{stack_name}.grafana.resources.requests",
        {"cpu": "1", "memory": "1G"},
    )
    limits = stack_registry.get(
        f"stacks.{stack_name}.grafana.resources.limits",
        {"cpu": "1", "memory": "1G"},
    )
    deployment = util.mk_deployment(
        name,
        [
            k.V1Container(
                name=name,
                image=image,
                ports=[
                    k.V1ContainerPort(
                        name=port_name,
                        container_port=port,
                    )
                ],
                resources=k.V1ResourceRequirements(
                    requests=requests,
                    limits=limits,
                ),
            )
        ],
    )
    yaml = YAML()
    yaml.dump(
        client.sanitize_for_serialization(deployment),
        Path(output_dir / "deployment.yaml").open("w", encoding="utf-8"),
    )
    # hpa
    yaml.dump(
        client.sanitize_for_serialization(
            util.mk_hpa(
                name,
                min_replicas=stack_registry.get(
                    f"stacks.{stack_name}.grafana.minReplicas", 1
                ),
                max_replicas=stack_registry.get(
                    f"stacks.{stack_name}.grafana.maxReplicas", 1
                ),
                scale_target_ref=k.V1CrossVersionObjectReference(
                    api_version=deployment.api_version,
                    kind=deployment.kind,
                    name=deployment.metadata.name,
                ),
            )
        ),
        Path(output_dir / "hpa.yaml").open("w", encoding="utf-8"),
    )
    # service
    yaml.dump(
        client.sanitize_for_serialization(
            util.mk_service(
                name, port=port, port_name=port_name, service_type="NodePort"
            )
        ),
        Path(output_dir / "service.yaml").open("w", encoding="utf-8"),
    )
    # service-account
    yaml.dump(
        client.sanitize_for_serialization(
            util.mk_service_account(name, automount_token=False)
        ),
        Path(output_dir / "service-account.yaml").open("w", encoding="utf-8"),
    )
    # ArgoCD app
    app = DataPath(
        yaml.load(Path("components", "argocd", "grafana.yaml").open(encoding="utf-8"))
    )
    app["spec.source.path"] = str(output_dir)
    yaml.dump(
        app.data, Path(output_dir, "application.yaml").open("w", encoding="utf-8")
    )


def generate(stack_registry: DataPath, dest: Path):
    "Generate grafana manifests."
    for stack_name in stack_registry["stacks"]:
        if "grafana" not in stack_registry[f"stacks.{stack_name}"]:
            continue
        generate_stack(dest, stack_registry, stack_name)
