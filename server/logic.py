import docker


def _get_docker_client():
    """Returns the Docker client instance."""
    client = docker.from_env()
    return client


def _list_containers() -> list[dict]:
    """Lists all running Docker containers as structured JSON."""
    client = _get_docker_client()
    containers = client.containers.list()

    result = [
        {
            "id": container.short_id,
            "name": container.name,
            "image": container.attrs['Config']['Image'],
            "status": container.status,
        }
        for container in containers
    ]
    return result

def _get_container_logs(container_id: str, tail: int = 100) -> dict:
    """Fetches the last N log lines from a container (running or exited)"""
    client = _get_docker_client()
    container = client.containers.get(container_id)
    logs = container.logs(tail=tail).decode("utf-8", errors="replace")

    result = {
        "id": container.short_id,
        "name": container.name,
        "status": container.status,
        "tail": tail,
        "logs": logs,
    }
    return result
