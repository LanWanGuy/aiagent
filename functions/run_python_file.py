import os, subprocess
from socket import timeout

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return f'Process exited with code {result.returncode}'
        elif not result.stdout and not result.stderr:
            return 'No output produced'
        else:
            return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'
    except Exception as e:
        return f'Error: executing Python file:{str(e)}'
