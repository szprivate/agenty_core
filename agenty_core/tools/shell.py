"""Cross-platform shell execution tool for running skill scripts."""

import json
import subprocess
import sys

from agenty_core._compat import tool


@tool
def run_script(command: str, timeout: int = 120) -> str:
    """Run a shell command and return its stdout/stderr.

    Use this to execute skill scripts (e.g. Python scripts under skills/).
    Works on both Windows and Unix.

    Pass a **single-line** command. A multi-line command — including an inline
    ``python -c "..."`` whose quoted body contains real newlines — is parsed by
    ``cmd.exe`` on Windows line-by-line and silently does nothing (exit 0, empty
    output), so never inline a multi-line script here. To run a script, write it to
    a file first and invoke ``python <file>``; to PUT a local file to a URL, use the
    dedicated ``upload_file_to_url`` tool instead of a hand-written PUT snippet.

    Args:
        command: The full command to run (e.g. 'python ./skills/image-downsize/scripts/downsize.py ...').
        timeout: Maximum seconds to wait for the command to finish (default 120).
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            executable=None,
        )
        output = {
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
        return json.dumps(output)
    except subprocess.TimeoutExpired:
        return json.dumps({"error": f"Command timed out after {timeout}s", "command": command})
    except Exception as e:
        return json.dumps({"error": str(e)})
