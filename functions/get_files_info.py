import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        working_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_abs, directory))
        valid_target = working_abs == os.path.commonpath([working_abs, target_dir])


        if not valid_target:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        fileinfo = ""
        for file in os.listdir(target_dir):
            fileinfo += f"- {file}: file_size={os.path.getsize(os.path.join(target_dir, file))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, file))}\n"
        return fileinfo
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"
