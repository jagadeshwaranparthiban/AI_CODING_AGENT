from pathlib import Path
import docker
from agents.exceptions import CodeExecutionError
from agents.logger import logger

def get_docker_client():
    try:
        client = docker.from_env()
        return client
    except docker.errors.DockerException as e:
        logger.exception("Failed to connect to Docker")
        raise CodeExecutionError(
            "Failed to connect to Docker. Ensure Docker is installed and running."
        ) from e


def run_python(file_path):

    file_path = Path(file_path).resolve()

    if not file_path.exists():
        raise CodeExecutionError(
            f"Python file does not exist: {file_path}"
        )
    
    client = get_docker_client()
    workspace_dir = file_path.parent

    try:
        container = client.containers.run(
            image="python:3.12",
            command=["python", f"/app/{file_path.name}"],
            volumes={
                str(workspace_dir): {
                    "bind": "/app",
                    "mode": "rw"
                }
            },
            working_dir="/app",
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