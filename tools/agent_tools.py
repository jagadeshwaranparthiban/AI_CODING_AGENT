from langchain_core.tools import tool
from tools.file_tools import *


@tool
def read_file_tool(project_id: str, file_path: str) -> str:
    """Read the contents of a file."""
    return read_file(project_id, file_path)


@tool
def write_file_tool(project_id: str, file_path: str,content: str) -> str:
    """Write content to a file."""
    return write_file(project_id, file_path, content)


@tool
def list_files_tool(project_id: str, directory: str) -> list[str]:
    """List files in a directory."""
    return list_files(project_id, directory)