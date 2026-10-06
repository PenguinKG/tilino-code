import os

import config

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the contents of a file up to 10000 characters, indicating if its truncated",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to read from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str):
    try:
        working_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_abs, file_path))
        valid_target = working_abs == os.path.commonpath([working_abs, target_file])


        if not valid_target:
            return f'Error: Cannot read {file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file) as readfile:
            content = readfile.read(config.MAX_CHARACTERS)
            if readfile.read(1):
                content += f'[...File "{file_path}" truncated at {config.MAX_CHARACTERS} characters]'
        return content

    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"
