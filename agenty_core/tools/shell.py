"""Cross-platform script execution for skills — one program, no shell.

The policy (which programs, which folders, and why) lives in
:mod:`agenty_core.sandbox`. This module is the tool wrapper around it.
"""

import json
import subprocess

from agenty_core._compat import tool
from agenty_core import sandbox


@tool
def run_script(command: str, timeout: int = 120) -> str:
    """Run a single program and return its stdout/stderr.

    Use this to execute skill scripts (e.g. Python scripts under skills/) and the
    media/inspection tools they rely on. Works on both Windows and Unix.

    **This runs one program directly — there is no shell.** Pipes, redirects,
    ``&&`` chains, backticks and ``$(…)`` are not available and are refused rather
    than silently mangled. Run one command per call; when you need several steps,
    write a Python script with ``write_text_file`` and run that file. To PUT a
    local file to a URL, use the dedicated ``upload_file_to_url`` tool.

    Pass a **single-line** command; a multi-line one is refused for the same
    reason it never worked on Windows.

    The set of programs is restricted (python, ffmpeg/ffprobe, git, and the usual
    listing/searching tools), and path arguments must stay inside the project,
    ComfyUI's directories, or a temp file. A refusal says exactly what was
    disallowed, so read it and adjust rather than retrying the same command.

    Args:
        command: The command to run (e.g. 'python ./skills/image-downsize/scripts/downsize.py ...').
        timeout: Maximum seconds to wait for the command to finish (default 120).
    """
    argv, why = sandbox.check_command(command)
    if argv is None:
        # An error, not an exception: the model reads this and picks another way.
        # Naming the command back makes a refusal legible in the tool-activity log,
        # where the call itself is truncated.
        return json.dumps({"error": f"run_script refused this command: {why}",
                           "command": str(command or "")[:200], "refused": True})

    # A bare "python" means the interpreter agentY runs on, not whatever is first
    # on PATH — a skill script needs the environment its dependencies live in.
    if sandbox.norm_exe(argv[0]) in ("python", "python3", "py"):
        argv = [sandbox.python_executable(), *argv[1:]]

    try:
        result = subprocess.run(
            argv,
            shell=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(sandbox.working_directory()),
        )
        output = {
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
        return json.dumps(output)
    except subprocess.TimeoutExpired:
        return json.dumps({"error": f"Command timed out after {timeout}s", "command": command})
    except FileNotFoundError:
        return json.dumps({"error": f"'{argv[0]}' is not installed or not on PATH.",
                           "command": command})
    except Exception as e:
        return json.dumps({"error": str(e)})
