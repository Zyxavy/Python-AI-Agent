import os
from functions.get_file_content import get_file_content

results = [
    get_file_content("calculator", "main.py") or "",
    get_file_content("calculator", "pkg/calculator.py") or "",
    get_file_content("calculator", "/bin/cat") or "",
    get_file_content("calculator", "pkg/does_not_exist.py") or ""
]


for result in results:
    print(result)