"""App-root resolution for the shared tool layer.

The tools and utils in ``agenty_core`` used to live inside each app's ``src/``
package and resolved paths like ``config/settings.json`` or
``output_workflows/`` relative to their own ``__file__``.  Now that they live in
a *sibling* package, ``__file__`` points at the agenty_core install, not at the
consuming app — so every config/output path has to be anchored on the
**consuming app's** root instead.

Resolution order for :func:`project_root`:

1. An explicit root set by the app at startup via :func:`set_project_root`.
2. The ``AGENTY_PROJECT_ROOT`` environment variable.
3. The current working directory (both apps launch from their repo root).

Each consumer calls ``set_project_root(<its repo root>)`` once during startup
(the agentY-mcp server in ``src/mcp_server.py``; the Strands app in its
bootstrap).  Tool/util modules call :func:`project_root` instead of computing
``Path(__file__).parent.parent`` themselves.
"""

from __future__ import annotations

import os
from pathlib import Path

_PROJECT_ROOT: Path | None = None


def set_project_root(path: str | os.PathLike) -> None:
    """Pin the consuming app's root directory.

    Call once at startup, before any tool that reads ``config/`` or writes to
    ``output_workflows/`` runs.
    """
    global _PROJECT_ROOT
    _PROJECT_ROOT = Path(path).resolve()


def project_root() -> Path:
    """Return the consuming app's root directory (see module docstring)."""
    if _PROJECT_ROOT is not None:
        return _PROJECT_ROOT
    env = os.environ.get("AGENTY_PROJECT_ROOT")
    if env:
        return Path(env).resolve()
    return Path.cwd().resolve()
