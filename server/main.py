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


if __name__ == "__main__":
    mcp.run()
