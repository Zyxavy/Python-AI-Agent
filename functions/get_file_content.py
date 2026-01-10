import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not target_file.startswith(working_dir_abs):
            return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(target_file):
            return f'Error: "{file_path}" does not exist'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" is not a file'

    except Exception as e:
        return f'Error: {str(e)}'
    
    try:
        MAX_CHARS = 10000

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            extra = f.read(1)
            if extra:
                file_content_string += f'\n[...File "{target_file}" truncated at {MAX_CHARS} characters]'

    except Exception as e:
        return f'Error: {str(e)}'

    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file at a specified path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)