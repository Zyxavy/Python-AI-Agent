import os
from functions.get_files_info import get_files_info

results = [
    get_files_info("calculator", ".") or "",
    get_files_info("calculator", "pkg") or "",
    get_files_info("calculator", "/bin") or "",
    get_files_info("calculator", "../") or ""
]


for result in results:
    print(result)