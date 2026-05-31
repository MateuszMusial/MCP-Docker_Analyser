from fastmcp import FastMCP
import docker
import json
    

client = docker.from_env()
mcp = FastMCP("My MCP Server")


@mcp.tool()
def list_containers() -> str:
    """Lists all running Docker containers as structured JSON."""
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
