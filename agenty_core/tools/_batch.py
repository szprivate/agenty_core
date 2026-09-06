"""Let a lookup tool answer for many subjects in one call.

An agent that needs ten node schemas used to spend ten round-trips on them, and
each one replays the whole conversation — system prompt, tool schemas, every
prior result — as fresh input. Measured on one workflow build: ten sequential
``get_node_schema`` calls at ~26K context each, ~215K input tokens and ~24
seconds to learn ten things that were all known before the first call.

So the read-only lookups take a list. The rules, applied by every one of them:

* **one subject in, today's answer out** — byte-identical to the un-batched
  response, so existing callers, prompts and skills keep working;
* **many subjects in, a map out**, keyed by subject, under a plural key;
* **a subject that fails does not fail the batch** — its entry carries the error
  and the rest still answer, because the alternative is an agent retrying nine
  good lookups to get the tenth.
"""

from __future__ import annotations

import json
from typing import Callable


def as_list(value) -> list:
    """One subject or many, always a list.

    Also unpacks a JSON array that arrived as a *string* (``'["a","b"]'``).
    Models emit that shape often enough that treating it as a single literal
    name — a lookup for a subject called ``["a","b"]`` — is a guaranteed miss
    where the intent was never ambiguous.
    """
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("[") and text.endswith("]"):
            try:
                parsed = json.loads(text)
            except ValueError:
                return [value]
            if isinstance(parsed, list):
                return parsed
        return [value]
    return [value]


def one_or_many(subjects: list, run_one: Callable[..., str], plural_key: str,
                key_of: Callable = str) -> str:
    """Run *run_one* per subject; return one answer, or a map of them.

    A single subject returns exactly what *run_one* returned — same string, so
    nothing downstream can tell whether it went through here. Several return
    ``{plural_key: {subject: answer}}`` with each answer parsed back from JSON
    where it is JSON, so the caller reads one object instead of nested strings.
    """
    if not subjects:
        return json.dumps({"error": "No subjects given.", plural_key: {}})
    if len(subjects) == 1:
        return run_one(subjects[0])

    out: dict = {}
    for subject in subjects:
        key = key_of(subject)
        try:
            raw = run_one(subject)
        except Exception as exc:  # noqa: BLE001 — one bad subject, not a bad batch
            out[key] = {"error": str(exc)}
            continue
        try:
            out[key] = json.loads(raw)
        except (ValueError, TypeError):
            out[key] = raw
    return json.dumps({plural_key: out, "count": len(out)})
