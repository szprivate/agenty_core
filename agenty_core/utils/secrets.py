"""
Centralised secret access for agentY.

Reads secrets directly from the .env file using ``dotenv_values`` so they
are never injected into ``os.environ`` (and therefore not visible to child
processes, logging frameworks, or environment dumps).

Usage::

    from agenty_core.utils.secrets import get_secret

    api_key = get_secret("COMFYUI_API_KEY")

Known secrets
-------------
    COMFYUI_API_KEY     – ComfyUI / Comfy.org API key
    HF_TOKEN            – Hugging Face access token
    COMFYUI_MODELS_DIR  – Local ComfyUI models directory override
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import dotenv_values

from agenty_core.paths import project_root


def _env_file() -> Path:
    """Path to the consuming app's ``.env`` (resolved lazily, post-startup)."""
    return project_root() / ".env"


@lru_cache(maxsize=1)
def _load() -> dict[str, Optional[str]]:
    """Load the .env file exactly once and cache the result."""
    env_file = _env_file()
    if env_file.exists():
        return dotenv_values(env_file)
    return {}


def get_secret(key: str, default: str = "") -> str:
    """Return the value of *key* from the environment or the .env file.

    Resolution order: ``os.environ`` first (so an MCP host / .mcpb bundle can
    inject secrets via env vars), then the ``.env`` file, then *default*.

    Args:
        key:     The name of the secret (e.g. ``"HF_TOKEN"``).
        default: Value to return when the key is absent or empty.

    Returns:
        The secret string, or *default* if not found.
    """
    env_value = os.environ.get(key)
    if env_value:
        return env_value
    value = _load().get(key)
    if value is None or value == "":
        return default
    return value
