from fastmcp import FastMCP
import docker
import json
    

mcp = FastMCP("My MCP Server")


def get_docker_client():
    """Returns the Docker client instance."""
    try:
        client = docker.from_env()
    except RuntimeError as e:
        print(f"Error initializing Docker client: {e}")
    return client


@mcp.tool()
def list_containers() -> str:
    """Lists all running Docker containers as structured JSON."""
    client = get_docker_client()
    containers = client.containers.list()

    if not containers:
        return json.dumps({"message": "No running containers found."}, indent=2)
    
    result = [
        {
            "id": container.short_id,
            "name": container.name,
            "image": container.attrs['Config']['Image'],
            "status": container.status,
        }
        for container in containers
    ]
    return json.dumps(result, indent=2)


@mcp.tool()
def get_container_logs(container_id: str, tail: int = 100) -> str:
    """Fetches the last N log lines from a container (running or exited).

    Use this to debug why a container is misbehaving or crashing.

    Args:
        container_id: The container name or (short/full) ID.
        tail: Number of log lines to return from the end (default 100).
    """
    client = get_docker_client()

    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound:
        return json.dumps(
            {"error": f"No container found matching '{container_id}'."}, indent=2
        )

    logs = container.logs(tail=tail).decode("utf-8", errors="replace")

    result = {
        "id": container.short_id,
        "name": container.name,
        "status": container.status,
        "tail": tail,
        "logs": logs,
    }
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run()
