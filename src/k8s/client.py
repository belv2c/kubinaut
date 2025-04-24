from kubernetes import client, config
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class KubernetesClient:
    """Kubernetes client wrapper for interacting with the cluster."""

    def __init__(self):
        """Initialize the Kubernetes client using local config."""
        try:
            config.load_kube_config()
            self.core_v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
            self.custom_objects = client.CustomObjectsApi()
            logger.info("Kubernetes client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kubernetes client: {str(e)}")
            raise

    async def get_namespaces(self) -> List[Dict[str, Any]]:
        """Get all namespaces in the cluster."""
        try:
            namespaces = self.core_v1.list_namespace()
            return [
                {
                    "name": ns.metadata.name,
                    "status": ns.status.phase,
                    "creation_timestamp": ns.metadata.creation_timestamp.isoformat(),
                }
                for ns in namespaces.items
            ]
        except Exception as e:
            logger.error(f"Failed to get namespaces: {str(e)}")
            raise

    async def get_pods(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """Get all pods in the specified namespace."""
        try:
            pods = self.core_v1.list_namespaced_pod(namespace)
            return [
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "ip": pod.status.pod_ip,
                    "node": pod.spec.node_name,
                    "creation_timestamp": pod.metadata.creation_timestamp.isoformat(),
                }
                for pod in pods.items
            ]
        except Exception as e:
            logger.error(f"Failed to get pods in namespace {namespace}: {str(e)}")
            raise

    async def get_services(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """Get all services in the specified namespace."""
        try:
            services = self.core_v1.list_namespaced_service(namespace)
            return [
                {
                    "name": svc.metadata.name,
                    "namespace": svc.metadata.namespace,
                    "cluster_ip": svc.spec.cluster_ip,
                    "type": svc.spec.type,
                    "ports": (
                        [
                            {
                                "port": port.port,
                                "target_port": port.target_port,
                                "protocol": port.protocol,
                            }
                            for port in svc.spec.ports
                        ]
                        if svc.spec.ports
                        else []
                    ),
                }
                for svc in services.items
            ]
        except Exception as e:
            logger.error(f"Failed to get services in namespace {namespace}: {str(e)}")
            raise

    async def get_deployments(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """Get all deployments in the specified namespace."""
        try:
            deployments = self.apps_v1.list_namespaced_deployment(namespace)
            return [
                {
                    "name": dep.metadata.name,
                    "namespace": dep.metadata.namespace,
                    "replicas": dep.spec.replicas,
                    "available_replicas": dep.status.available_replicas,
                    "strategy": dep.spec.strategy.type,
                    "creation_timestamp": dep.metadata.creation_timestamp.isoformat(),
                }
                for dep in deployments.items
            ]
        except Exception as e:
            logger.error(
                f"Failed to get deployments in namespace {namespace}: {str(e)}"
            )
            raise

    async def execute_command(
        self, command: str, namespace: str = "default"
    ) -> Dict[str, Any]:
        """Execute a command in the cluster context."""
        # This is a placeholder for command execution logic
        # In a real implementation, you would parse the command and execute appropriate K8s API calls
        return {
            "status": "success",
            "message": f"Command '{command}' executed in namespace '{namespace}'",
            "result": None,
        }
