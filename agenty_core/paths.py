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
_CORPUS_ROOT: Path | None = None


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


def set_corpus_root(path: str | os.PathLike) -> None:
    """Pin the canonical corpus root (rarely needed; mainly for tests)."""
    global _CORPUS_ROOT
    _CORPUS_ROOT = Path(path).resolve()


def corpus_root() -> Path:
    """Root of the *canonical* workflow-template corpus and recipe database.

    Unlike :func:`project_root` (per-app: ``config/settings.json``, ``models.json``,
    ``output_workflows/``, ``.env``, ``batch_jobs/``), the template corpus and its
    distilled recipe DB are shared by every consuming app, so they live **once**
    in the ``agenty_core`` repo and each app reads them from here — every app
    builds workflows from the same templates. Canonical layout under this root:

        comfyui_workflow_templates_custom/   (+ templates/index.json)
        comfyui_workflow_templates_official/ (+ index.json)
        config/workflow_templates.json       (name -> description catalog)
        config/workflow_recipes*.json        (generated DB, node_knowledge, cache)

    Override with ``AGENTY_CORPUS_ROOT``; defaults to the agenty_core repo root
    (this module is ``agenty_core/agenty_core/paths.py``, so two parents up).
    """
    if _CORPUS_ROOT is not None:
        return _CORPUS_ROOT
    env = os.environ.get("AGENTY_CORPUS_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parent.parent
