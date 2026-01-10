import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not os.path.exists(target_dir):
            return f'Error: "{target_dir}" does not exist'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'

        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    except Exception as e:
        return f'Error: {str(e)}'
    
    
    items = os.listdir(target_dir)
    items.sort()

    dir_name = os.path.basename(target_dir)
    if dir_name == "":
        dir_name = os.path.basename(working_directory)

    output = [f"Result for {dir_name} directory:"]

    
    for item in items:
        item_path = os.path.join(target_dir, item)

        try:
            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                is_dir = False
            elif os.path.isdir(item_path):
                file_size = os.path.getsize(item_path)
                is_dir = True
            else:
                file_size = 0
                is_dir = False
                
            output_lines.append(f"  - {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        except Exception as e:
            output_lines.append(f"  - {item}: error={str(e)}")
        
    return "\n".join(output_lines)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                default=".",
            ),
        },
    ),
)