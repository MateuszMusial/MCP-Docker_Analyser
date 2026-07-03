from unittest.mock import Mock

import docker
import pytest
from pytest_mock import MockerFixture

from server.logic import (
    _get_docker_client,
    _list_containers,
    _get_container_logs,
    _system_health,
)


def _make_container(
    mocker: MockerFixture,
    *,
    short_id: str,
    name: str,
    image: str,
    status: str,
) -> Mock:
    """
    Build a fake Docker container mock.
    """
    container = mocker.Mock(
        short_id=short_id,
        attrs={"Config": {"Image": image}},
        status=status,
    )
    container.name = name
    return container


def test_get_docker_client_returns_from_env(mocker: MockerFixture) -> None:
    """_get_docker_client returns whatever docker.from_env() produces."""
    from_env = mocker.patch("server.logic.docker.from_env")

    client = _get_docker_client()

    from_env.assert_called_once_with()
    assert client is from_env.return_value


def test_list_containers_maps_fields(mocker: MockerFixture) -> None:
    """Each running container is mapped to id/name/image/status."""
    fake = _make_container(
        mocker, short_id="abc123", name="test_container",
        image="test_image", status="running",
    )
    get_client = mocker.patch("server.logic._get_docker_client")
    get_client.return_value.containers.list.return_value = [fake]

    result = _list_containers()

    get_client.return_value.containers.list.assert_called_once_with()
    assert result == [
        {
            "id": "abc123",
            "name": "test_container",
            "image": "test_image",
            "status": "running",
        }
    ]


def test_list_containers_multiple(mocker: MockerFixture) -> None:
    """Order is preserved and every container is mapped."""
    c1 = _make_container(mocker, short_id="id1", name="one", image="img1", status="running")
    c2 = _make_container(mocker, short_id="id2", name="two", image="img2", status="running")
    get_client = mocker.patch("server.logic._get_docker_client")
    get_client.return_value.containers.list.return_value = [c1, c2]

    result = _list_containers()

    assert [c["name"] for c in result] == ["one", "two"]
    assert result[1]["image"] == "img2"


def test_list_containers_empty(mocker: MockerFixture) -> None:
    """No running containers yields an empty list."""
    get_client = mocker.patch("server.logic._get_docker_client")
    get_client.return_value.containers.list.return_value = []

    assert _list_containers() == []


def test_get_container_logs_happy_path(mocker: MockerFixture) -> None:
    """Returns the container metadata plus decoded logs."""
    container = _make_container(
        mocker, short_id="abc123", name="broken_app",
        image="img", status="exited",
    )
    container.logs.return_value = b"line1\nline2\n"
    get_client = mocker.patch("server.logic._get_docker_client")
    get_client.return_value.containers.get.return_value = container

    result = _get_container_logs("broken_app", tail=50)

    get_client.return_value.containers.get.assert_called_once_with("broken_app")
    container.logs.assert_called_once_with(tail=50)
    assert result == {
        "id": "abc123",
        "name": "broken_app",
        "status": "exited",
        "tail": 50,
        "logs": "line1\nline2\n",
    }


def test_get_container_logs_default_tail(mocker: MockerFixture) -> None:
    """Tail defaults to 100 when not supplied."""
    container = _make_container(mocker, short_id="x", name="c", image="i", status="running")
    container.logs.return_value = b""
    get_client = mocker.patch("server.logic._get_docker_client")
    get_client.return_value.containers.get.return_value = container

    result = _get_container_logs("c")

    container.logs.assert_called_once_with(tail=100)
    assert result["tail"] == 100


def test_get_container_logs_decodes_invalid_utf8(mocker: MockerFixture) -> None:
    """Invalid UTF-8 bytes are replaced, not raised."""
    container = _make_container(mocker, short_id="x", name="c", image="i", status="running")
    container.logs.return_value = b"ok \xff done"
    get_client = mocker.patch("server.logic._get_docker_client")
    get_client.return_value.containers.get.return_value = container

    result = _get_container_logs("c")

    assert result["logs"] == "ok � done"


def test_system_health_shape_and_conversions(mocker: MockerFixture) -> None:
    """CPU/memory/disk are read from psutil and bytes are converted to MB/GB."""
    mocker.patch("server.logic.psutil.cpu_percent", return_value=12.5)
    mocker.patch(
        "server.logic.psutil.virtual_memory",
        return_value=mocker.Mock(
            percent=40.0,
            total=8 * 1024 ** 3,       # 8 GB -> 8192 MB
            available=2 * 1024 ** 3,   # 2 GB -> 2048 MB
        ),
    )
    mocker.patch(
        "server.logic.psutil.disk_usage",
        return_value=mocker.Mock(
            percent=55.0,
            total=100 * 1024 ** 3,     # 100 GB
            free=45 * 1024 ** 3,       # 45 GB
        ),
    )

    result = _system_health()

    assert result == {
        "cpu_percent": 12.5,
        "memory": {"percent": 40.0, "total_mb": 8192, "available_mb": 2048},
        "disk": {"percent": 55.0, "total_gb": 100.0, "free_gb": 45.0},
    }
