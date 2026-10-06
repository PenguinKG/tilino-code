import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites the desired contents to a file and creates the file and necessary parent directories if it doesn't exist.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write to or create, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Contents to be written in the specified file."
                }
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_abs, file_path))
        valid_target = working_abs == os.path.commonpath([working_abs, target_file])


        if not valid_target:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, mode='w') as arch:
            arch.write(content)
        return f"Successfully wrote to {file_path} ({len(content)} characters written)"
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"
