from pathlib import Path
import docker
from agents.exceptions import CodeExecutionError
from agents.logger import logger
from .workspace import get_workspace, resolve_workspace_path


def get_docker_client():
    try:
        client = docker.from_env()
        return client
    except docker.errors.DockerException as e:
        logger.exception("Failed to connect to Docker")
        raise CodeExecutionError(
            "Failed to connect to Docker. Ensure Docker is installed and running."
        ) from e


def run_python(project_id: str, file_path: str):

    workspace = get_workspace(project_id)
    file_path = resolve_workspace_path(project_id, file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Python file does not exist: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )
    
    if file_path.suffix != ".py":
        raise ValueError(
            "run_python only supports Python files."
        )

    relative_path = file_path.relative_to(workspace)
    container_relative_path = relative_path.as_posix()
    container_file_path = f"/workspace/{container_relative_path}"
    
    client = get_docker_client()
    container = None

    try:
        container = client.containers.run(
            image="python:3.12",
            command=["python", str(container_file_path)],
            volumes={
                str(workspace): {
                    "bind": "/workspace",
                    "mode": "rw"
                }
            },
            working_dir="/workspace",
            detach=True,
            remove=False,
            network_disabled=True
        )

        result = container.wait()
        logs = container.logs().decode()
        container.remove()
        return result, logs
    
    except docker.errors.ContainerError as e:
        logger.exception("Error executing Python code in Docker")
        raise CodeExecutionError(
            f"Error executing Python code in Docker: {e.stderr.decode()}"
        ) from e
    
    finally:
        if container:
            try:
                container.remove(force=True)
            except Exception as e:
                logger.warning("Failed to remove Docker container: %s", e)