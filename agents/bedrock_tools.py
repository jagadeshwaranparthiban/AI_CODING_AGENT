from tools.file_tools import (
    read_file,
    write_file,
    list_files,
)
from agents.exceptions import ToolNotFoundError

TOOLS = [
    {
        "toolSpec": {
            "name": "read_file",
            "description": (
                "Read a file from the current project workspace. "
                "IMPORTANT: file_path MUST be a relative path such as "
                "'agent_test.py' or 'src/main.py'. "
                "NEVER use an absolute path such as 'C:/...' or "
                "'D:/...'. The project workspace is automatically provided "
                "by the application."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path of the file to read."
                        }
                    },
                    "required": ["file_path"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "write_file",
            "description": (
                "Write content to a file inside the current project workspace. "
                "IMPORTANT: file_path MUST be a relative path such as "
                "'agent_test.py' or 'src/main.py'. "
                "NEVER use an absolute path. "
                "The project workspace is automatically provided "
                "by the application."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path of the file to write."
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write into the file."
                        }
                    },
                    "required": [
                        "file_path",
                        "content"
                    ]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "list_files",
            "description": (
                "List files inside the current project workspace. "
                "Use a relative directory such as '.' or 'src'. "
                "Do not use absolute paths. "
                "Use '.' for the project root."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "Directory whose files should be listed."
                        }
                    },
                    "required": ["directory"]
                }
            }
        }
    }
]

TOOL_FUNCTIONS = {
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
}

def execute_tool(project_id: str, tool_name: str, tool_input: dict):
    if tool_name not in TOOL_FUNCTIONS:
        raise ToolNotFoundError(
            f"Unknown tool requested: {tool_name}"
        )

    tool = TOOL_FUNCTIONS[tool_name]
    return tool(project_id=project_id, **tool_input)