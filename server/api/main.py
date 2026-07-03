import docker
from fastapi import FastAPI, HTTPException

from server.logic import _list_containers, _get_container_logs
from server.api.schemas import ContainerListResponse, ContainerLogsResponse


app = FastAPI()


@app.get("/")
def hello() -> str:
    return "Hello world!"


@app.get("/containers", response_model=list[ContainerListResponse])
def list_containers():
    return _list_containers()


@app.get("/containers/{container_id}/logs", response_model=ContainerLogsResponse)
def get_container_logs(container_id: str, tail: int = 100):
    try:
        return _get_container_logs(container_id, tail)
    except docker.errors.NotFound:
        raise HTTPException(404, f"No container found matching '{container_id}'.")
