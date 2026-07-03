from pydantic import BaseModel, Field


class ContainerListResponse(BaseModel):
    id: str = Field(..., description="The unique identifier for the Docker container.")
    name: str = Field(..., description="The name of the Docker container.")
    image: str = Field(..., description="The image used to create the Docker container.")
    status: str = Field(..., description="The current status of the Docker container.")


class ContainerLogsResponse(BaseModel):
    id: str = Field(..., description="The unique identifier for the Docker container.")
    name: str = Field(..., description="The name of the Docker container.")
    status: str = Field(..., description="The current status of the Docker container.")
    tail: int = Field(100, description="The number of log lines returned from the end of the logs.")
    logs: str = Field(..., description="The log output from the Docker container.")


class SystemHealthResponse(BaseModel):
    cpu_percent: float = Field(..., description="The current CPU usage percentage of the host machine.")
    memory: dict = Field(..., description="Memory usage details of the host machine.")
    disk: dict = Field(..., description="Disk usage details of the host machine.")
