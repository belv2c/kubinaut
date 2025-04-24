from typing import Dict, Any
import json
import logging
from ..k8s.client import KubernetesClient

logger = logging.getLogger(__name__)


class MCPHandler:
    """Handler for Model Context Protocol messages."""

    def __init__(self, k8s_client: KubernetesClient):
        """Initialize the MCP handler with a Kubernetes client."""
        self.k8s_client = k8s_client

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP messages."""
        try:
            # Validate message format
            if not isinstance(message, dict) or "type" not in message:
                return self._error_response("Invalid message format")

            # Handle different message types
            handlers = {
                "get_namespaces": self._handle_get_namespaces,
                "get_pods": self._handle_get_pods,
                "get_services": self._handle_get_services,
                "get_deployments": self._handle_get_deployments,
                "execute_command": self._handle_execute_command,
            }

            handler = handlers.get(message["type"])
            if not handler:
                return self._error_response(f"Unknown message type: {message['type']}")

            return await handler(message)

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            return self._error_response(str(e))

    async def _handle_get_namespaces(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_namespaces message."""
        try:
            namespaces = await self.k8s_client.get_namespaces()
            return {
                "status": "success",
                "type": "namespaces_response",
                "data": namespaces,
            }
        except Exception as e:
            return self._error_response(str(e))

    async def _handle_get_pods(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_pods message."""
        try:
            namespace = message.get("namespace", "default")
            pods = await self.k8s_client.get_pods(namespace)
            return {"status": "success", "type": "pods_response", "data": pods}
        except Exception as e:
            return self._error_response(str(e))

    async def _handle_get_services(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_services message."""
        try:
            namespace = message.get("namespace", "default")
            services = await self.k8s_client.get_services(namespace)
            return {"status": "success", "type": "services_response", "data": services}
        except Exception as e:
            return self._error_response(str(e))

    async def _handle_get_deployments(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_deployments message."""
        try:
            namespace = message.get("namespace", "default")
            deployments = await self.k8s_client.get_deployments(namespace)
            return {
                "status": "success",
                "type": "deployments_response",
                "data": deployments,
            }
        except Exception as e:
            return self._error_response(str(e))

    async def _handle_execute_command(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle execute_command message."""
        try:
            if "command" not in message:
                return self._error_response("Command not specified")

            namespace = message.get("namespace", "default")
            result = await self.k8s_client.execute_command(
                message["command"], namespace
            )
            return {"status": "success", "type": "command_response", "data": result}
        except Exception as e:
            return self._error_response(str(e))

    def _error_response(self, message: str) -> Dict[str, Any]:
        """Create an error response."""
        return {"status": "error", "type": "error_response", "message": message}
