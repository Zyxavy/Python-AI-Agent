import os

def get_files_info(working_directory, directory="."):

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    
        if not valid_target_dir:
            print(f'Error: "{directory}" is not a directory')
            return 

        if not os.path.exists(target_dir):
            return f'Error: "{target_dir}" does not exist'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'

        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    except Exception as e:
        return f'Error: {str(e)}'
    
    
    items = os.listdir(target_dir)
    output = f"Result for {os.path.basename(target_dir)} directory:"

    items.sort()
    
    for item in items:
        item_path = os.path.join(target_dir, item)

        try:
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            string = f"\n- {item}: file_size={file_size}, is_dir={is_dir}"
            output += string
        except Exception as e:
            string = f"\n - {item}: error={str(e)}"
            output += string
        
    return output.rstrip()

    