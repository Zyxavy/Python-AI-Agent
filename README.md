# Python-AI-Agent

Using a pre-trained LLM to build an agent from scratch.

## Overview

This repository contains a Python AI Agent, capable of understanding and executing tasks related to file system operations and Python script execution. It can assist with:

-  **File System Navigation:** Listing files and directories.
-   **File Operations:** Reading and writing file content.
-   **Code Execution:** Running Python scripts with specified arguments.

---

## Direction to use

To keep things secure, try not to hardcode your key directly in main.py. Instead, you can set it as an environment variable or just swap it out in the code for a quick test:

```python
 # main.py
    api_key = "your-key-here"
```
I'm using uv for package management, but regular Python works too:

```bash
    uv run main.py "Check the files in the directory and tell me what's inside"
```
Using Python (with verbose mode to see the agent's logic):

```bash
python main.py "Run the script in the calculator folder" --verbose
```

---

## Limitations

- This agent can only access the `calculator/` directory, feel free to change it to use another or various directories.

- This is a learning project, so expect some bugs while I refine the logic.

---

Learning Resources from [boot.dev](https://www.boot.dev/)

---