import json
import os

JAIL_ROOT = os.path.realpath(os.getcwd())

CWD = {"cwd": os.getcwd()}

TOOL_REMINDER = (
    "Reminder: only perform the requested task. Never delete files. "
    "Ask the user if uncertain."
)


def _resolve(path=None):
    base = CWD["cwd"]
    if path is None or path == "":
        resolved = os.path.realpath(base)
    else:
        resolved = os.path.realpath(os.path.join(base, path))
    if not (resolved == JAIL_ROOT or resolved.startswith(JAIL_ROOT + os.sep)):
        raise PermissionError(f"path outside jail: {path}")
    return resolved


def list_dir(path=None):
    entries = sorted(os.listdir(_resolve(path)))
    if not entries:
        return "(empty directory)"
    return "\n".join(entries)


def read_file(path, offset=0, max_bytes=8000):
    with open(_resolve(path), "rb") as f:
        f.seek(offset)
        data = f.read(max_bytes + 1)
    truncated = len(data) > max_bytes
    text = data[:max_bytes].decode(errors="replace")
    if truncated:
        text += f"\n(truncated at {max_bytes} bytes; re-read with offset={offset + max_bytes} for more)"
    return text


def write_file(path, content):
    resolved = _resolve(path)
    os.makedirs(os.path.dirname(resolved), exist_ok=True)
    with open(resolved, "w") as f:
        f.write(content)
    return f"wrote {len(content)} bytes to {path}"


def cd(path):
    resolved = _resolve(path)
    if not os.path.isdir(resolved):
        return f"error: not a directory: {path}"
    CWD["cwd"] = resolved
    return f"cwd is now {resolved}"


def mkdir(path):
    os.makedirs(_resolve(path), exist_ok=True)
    return f"created directory {path}"


TOOL_IMPLS = {
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
    "cd": cd,
    "mkdir": mkdir,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List the entries of a directory (default: the current working directory).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path relative to the working directory. Optional.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file's contents, capped at 8000 bytes; use offset to continue reading.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path relative to the working directory."},
                    "offset": {
                        "type": "integer",
                        "description": "Byte offset to start reading from. Default 0.",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text content to a file, creating parent directories as needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path relative to the working directory."},
                    "content": {"type": "string", "description": "Full text content to write."},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cd",
            "description": "Change the agent's working directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory to move to."},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mkdir",
            "description": "Create a directory (and parents), like mkdir -p.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory to create."},
                },
                "required": ["path"],
            },
        },
    },
]


def dispatch(call):
    name = call.function.name
    impl = TOOL_IMPLS.get(name)
    if impl is None:
        return f"error: unknown tool {name}"
    try:
        args = json.loads(call.function.arguments or "{}")
    except json.JSONDecodeError as e:
        return f"error: invalid tool arguments: {e}"
    try:
        result = impl(**args)
    except PermissionError as e:
        return f"error: {e}"
    except Exception as e:
        return f"error: {type(e).__name__}: {e}"
    return f"{result}\n\n{TOOL_REMINDER}"
