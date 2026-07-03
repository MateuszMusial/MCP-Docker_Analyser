from fastmcp import FastMCP
import docker
import json

from logic import _list_containers, _get_container_logs, _system_health
    

mcp = FastMCP("My MCP Server")



@mcp.tool()
def list_containers() -> str:
    """
    Lists all running Docker containers as structured JSON.
    Use this to see what containers are currently running on the host.
    """
    containers = _list_containers()

    if not containers:
        return json.dumps({"message": "No running containers found."}, indent=2)
    return json.dumps(containers, indent=2)


@mcp.tool()
def get_container_logs(container_id: str, tail: int = 100) -> str:
    """
    Fetches the last N log lines from a container (running or exited).
    Use this to debug why a container is misbehaving or crashing.

    Args:
        container_id: The container name or (short/full) ID.
        tail: Number of log lines to return from the end (default 100).
    """
    try:
        logs = _get_container_logs(container_id, tail)
    except docker.errors.NotFound:
        return json.dumps({"error": f"No container found matching '{container_id}'."}, indent=2)
    return json.dumps(logs, indent=2)


@mcp.tool()
def get_system_health() -> str:
    """
    Returns the current CPU, memory, and disk usage of the host machine.
    Use this to monitor the health of the system running the Docker containers.
    """
    health = _system_health()
    return json.dumps(health, indent=2)


if __name__ == "__main__":
    mcp.run()
