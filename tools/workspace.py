from pathlib import Path


WORKSPACES_ROOT = Path("workspaces").resolve()

class WorkspaceViolationError(Exception):
    """Raised when a path escapes the project workspace."""


def get_workspace(project_id: str) -> Path:
    if not project_id or not project_id.strip():
        raise ValueError("Project ID cannot be empty.")

    workspace = (WORKSPACES_ROOT / project_id).resolve()

    if not workspace.is_relative_to(WORKSPACES_ROOT):
        raise WorkspaceViolationError(
            f"Invalid project ID: {project_id}"
        )

    workspace.mkdir(parents=True, exist_ok=True)

    return workspace


def resolve_workspace_path(project_id: str, requested_path: str) -> Path:
    if not requested_path or not requested_path.strip():
        raise ValueError("File path cannot be empty.")

    workspace = get_workspace(project_id)
    requested = Path(requested_path)

    if requested.is_absolute():
        raise WorkspaceViolationError(
            "Absolute paths are not allowed."
        )

    resolved = (workspace / requested).resolve()

    if not resolved.is_relative_to(workspace):
        raise WorkspaceViolationError(
            f"Path escapes workspace: {requested_path}"
        )

    return resolved