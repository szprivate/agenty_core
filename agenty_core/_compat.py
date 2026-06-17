"""A no-op ``tool`` decorator so shared tool functions stay plain callables.

The tool functions in ``agenty_core.tools`` are framework-agnostic: the
agentY-mcp server registers them with FastMCP centrally, and the Strands app
wraps them with ``strands.tool`` at registration time.  Neither needs the
decorator to do anything, so it returns the function untouched.  It accepts both
the bare ``@tool`` and parametrised ``@tool(...)`` forms.
"""

from __future__ import annotations

from typing import Any, Callable


def tool(func: Callable | None = None, *_args: Any, **_kwargs: Any):
    """No-op replacement for ``strands.tool`` — returns the function unchanged."""
    if func is not None and callable(func):
        return func

    def _wrap(f: Callable) -> Callable:
        return f

    return _wrap
