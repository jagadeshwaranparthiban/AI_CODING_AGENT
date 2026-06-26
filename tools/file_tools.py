from pathlib import Path


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