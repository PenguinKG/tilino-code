import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the specified Python file with the desired arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the Python file that's wanted to run, relative to the working directory (default is the working directory itself)",
                },
                "arg": {
                    "type": "array",
                    "items": {
                      "type": "string"
                    },
                    "description": "Optional arguments to be passed down to the run command"
                }
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, arg: list[str]| None = None):
    try:
        working_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_abs, file_path))
        valid_target = working_abs == os.path.commonpath([working_abs, target_file])


        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if arg:
            command.extend(arg)

        stringconst = ""
        completedrun = subprocess.run(command, cwd=working_abs, capture_output=True, text=True, timeout=30, check=False)

        if completedrun.returncode != 0:
            stringconst += f"Process exited with code {completedrun.returncode}\n\n"
        if not completedrun.stdout and not completedrun.stderr:
            stringconst += "No output produced"
        else:
            stringconst += f"STDOUT: {completedrun.stdout}\n\nSTDERR: {completedrun.stderr}"

        return stringconst

    except Exception as e:  # noqa: BLE001
        return f"Error: executing Python file: {e}"
