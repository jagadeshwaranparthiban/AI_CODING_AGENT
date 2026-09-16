from pathlib import Path
import docker

client = docker.from_env()

def run_python(file_path):

    file_path = Path(file_path).resolve()

    if not file_path.exists():
        raise FileNotFoundError(
            f"Python file does not exist: {file_path}"
        )
    
    workspace_dir = file_path.parent
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