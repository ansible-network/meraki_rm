"""Convert Python dataclass fields and type hints to JSON Schema.

Used by the MCP server to generate tool input schemas from User Model
dataclasses. Reads field types, defaults, and metadata descriptions
directly from the dataclass -- no external files needed.
"""

from __future__ import annotations

import dataclasses
import typing
from typing import Any, Dict, get_type_hints


_ORIGIN_MAP = {
    list: "array",
    dict: "object",
}


def _unwrap_optional(tp: Any) -> tuple[Any, bool]:
    """Unwrap Optional[T] -> (T, True) or return (tp, False)."""
    origin = getattr(tp, "__origin__", None)
    if origin is typing.Union:
        args = tp.__args__
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return non_none[0], True
    return tp, False


def _python_type_to_json_schema(tp: Any) -> Dict[str, Any]:
    """Map a Python type annotation to a JSON Schema fragment."""
    inner, _ = _unwrap_optional(tp)

    if inner is str:
        return {"type": "string"}
    if inner is int:
        return {"type": "integer"}
    if inner is float:
        return {"type": "number"}
    if inner is bool:
        return {"type": "boolean"}

    origin = getattr(inner, "__origin__", None)

    if origin in (list, typing.List):
        args = getattr(inner, "__args__", ())
        if args:
            items = _python_type_to_json_schema(args[0])
        else:
            items = {}
        return {"type": "array", "items": items}

    if origin in (dict, typing.Dict):
        return {"type": "object"}

    return {"type": "string"}


def dataclass_to_json_schema(cls: type, exclude_fields: set[str] | None = None) -> Dict[str, Any]:
    """Convert a dataclass to a JSON Schema object.

    Reads ``dataclasses.fields()`` for names and defaults, ``get_type_hints()``
    for types, and ``field.metadata["description"]`` for descriptions.

    Args:
        cls: A dataclass type (User Model).
        exclude_fields: Field names to omit (e.g. scope fields handled separately).

    Returns:
        JSON Schema dict with ``type``, ``properties``, and ``required``.
    """
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f"{cls} is not a dataclass")

    exclude = exclude_fields or set()
    hints = get_type_hints(cls)
    properties: Dict[str, Any] = {}
    required: list[str] = []

    for f in dataclasses.fields(cls):
        if f.name.startswith("_") or f.name in exclude:
            continue

        tp = hints.get(f.name, str)
        prop = _python_type_to_json_schema(tp)

        desc = f.metadata.get("description") if f.metadata else None
        if desc:
            prop["description"] = desc

        _, is_optional = _unwrap_optional(tp)
        if not is_optional and f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING:
            required.append(f.name)

        properties[f.name] = prop

    schema: Dict[str, Any] = {
        "type": "object",
        "properties": properties,
    }
    if required:
        schema["required"] = required

    return schema
