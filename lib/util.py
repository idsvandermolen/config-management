"""
Various utility functions
"""
import typing
import kubernetes.client as k


def mk_deployment(name: str, containers: typing.List[k.V1Container]) -> k.V1Deployment:
    "Generate Deployment."
    return k.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=k.V1ObjectMeta(name=name),
        spec=k.V1DeploymentSpec(
            selector={"matchLabels": {"name": name}},
            template=k.V1PodTemplateSpec(
                metadata=k.V1ObjectMeta(labels={"name": name}),
                spec=k.V1PodSpec(containers=containers),
            ),
        ),
    )


def mk_hpa(
    name: str,
    min_replicas: int,
    max_replicas: int,
    scale_target_ref: k.V1CrossVersionObjectReference,
    target_cpu_utilization_percentage: int = 80,
) -> k.V1HorizontalPodAutoscaler:
    "Generate HorizontalPodAutoscaler."
    return k.V1HorizontalPodAutoscaler(
        api_version="autoscaling/v1",
        kind="HorizontalPodAutoscaler",
        metadata=k.V1ObjectMeta(name=name),
        spec=k.V1HorizontalPodAutoscalerSpec(
            min_replicas=min_replicas,
            max_replicas=max_replicas,
            scale_target_ref=scale_target_ref,
            target_cpu_utilization_percentage=target_cpu_utilization_percentage,
        ),
    )


def mk_service(name: str, port: int, port_name: str, service_type=None) -> k.V1Service:
    "Generate service"
    return k.V1Service(
        api_version="v1",
        kind="Service",
        metadata=k.V1ObjectMeta(name=name, labels={"name": name}),
        spec=k.V1ServiceSpec(
            ports=[k.V1ServicePort(name=port_name, port=port, target_port=port)],
            selector={"name": name},
            type=service_type,
        ),
    )


def mk_service_account(name: str, automount_token: bool = None) -> k.V1ServiceAccount:
    "Generate service account"
    return k.V1ServiceAccount(
        api_version="v1",
        kind="ServiceAccount",
        metadata=k.V1ObjectMeta(name=name),
        automount_service_account_token=automount_token,
    )
