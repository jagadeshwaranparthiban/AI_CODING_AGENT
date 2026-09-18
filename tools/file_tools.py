from pathlib import Path
from .workspace import resolve_workspace_path

def save_code(project_id, code):

    workspace = Path(
        f"workspaces/{project_id}"
    )

    workspace.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = workspace / "main.py"
    file_path.write_text(code)
    return str(file_path)

def read_file(project_id: str, file_path: str) -> str:

    path = resolve_workspace_path(project_id, file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )

    return path.read_text(encoding="utf-8")


def write_file(project_id: str, file_path: str, content: str) -> str:

    path = resolve_workspace_path(project_id, file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        content,
        encoding="utf-8"
    )

    return str(path.resolve())


def list_files(project_id: str, directory: str) -> list[str]:

    path = resolve_workspace_path(project_id, directory)

    if not path.exists():
        raise FileNotFoundError(
            f"Directory not found: {directory}"
        )

    if not path.is_dir():
        raise ValueError(
            f"Path is not a directory: {directory}"
        )

    return [
        str(file.resolve())
        for file in path.rglob("*")
        if file.is_file()
    ]

def check_directory_exists(directory: str) -> bool:
    path = Path(directory)
    return path.exists() and path.is_dir()