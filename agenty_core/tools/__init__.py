"""Shared, framework-agnostic tool functions.

These are plain callables (the ``@tool`` decorator here is a no-op). The
agentY-mcp server registers them with FastMCP; the Strands app wraps them with
``strands.tool``. Image-handling and memory tools are intentionally *not* here —
they diverge per host (return format / memory backend) and live in each repo.
"""
