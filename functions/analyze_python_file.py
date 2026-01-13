import ast, os
from google.genai import types

def analyze_python_file(working_directory, file_path):
        
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{target_file}" as it is outside the permitted working directory'

        if not target_file.endswith(".py"):
            return f'Error: "{target_file}" is not a Python file'
                    
        if not os.path.isfile(target_file):
            return f'Error: "{target_file}" does not exist or is not a regular file'


    except Exception as e:
        return f"Error: executing Python file: {e}"

    try:

        with open(target_file, 'r') as f:
            tree = ast.parse(f.read())
        
        result = {
            "functions": [],
            "classes": [],
            "f_calls": [],
            "imports": [],
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                result["functions"].append({
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "line": node.lineno
                })

            elif isinstance(node, ast.ClassDef):
                    result["classes"].append({
                        "name": node.name,
                        "line": node.lineno
                    })
        
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].append({
                        "name": alias.name,
                        "line": node.lineno
                    })
            
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    result["f_calls"].append({
                        "name": node.func.id,
                        "line": node.lineno
                    })
            
        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_analyze_python_file = types.FunctionDeclaration(
    name="analyze_python_file", 
    description="Analyze the contents of a specific Python file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema( 
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            )
        },
        required=["file_path"], 
    ),
)