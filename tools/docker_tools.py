from pathlib import Path
import docker

client = docker.from_env()

def run_python(file_path):

    file_path = Path(file_path)
    container = client.containers.run(
        image="python:3.12",
        command=f"python {file_path.name}",
        volumes={
            str(file_path.parent.resolve()): {
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