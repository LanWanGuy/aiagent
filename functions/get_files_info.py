import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            if directory == ".":
                print ("Result for current directory:")
                results = ""
                for file in os.listdir(target_dir):
                    results = results + (f"  - {file}: file_size={os.path.getsize(os.path.join(target_dir, file))} bytes is_dir={os.path.isdir(os.path.join(target_dir, file))}\n")
                return results
            else:
                print (f"Result for '{directory}' directory:")
                results = ""
                for file in os.listdir(target_dir):
                    results = results + (f"  - {file}: file_size={os.path.getsize(os.path.join(target_dir, file))} bytes is_dir={os.path.isdir(os.path.join(target_dir, file))}\n")
                return results
    except Exception as e:
        return f'Error: {str(e)}'
