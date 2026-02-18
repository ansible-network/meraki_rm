"""Generate spec-compliant response bodies from schemas.

Fills required fields with type-appropriate defaults and merges
state_store data with schema defaults to ensure every response
passes spec validation.
"""

from typing import Any, Dict, List, Optional


def generate_default_from_schema(schema: Dict[str, Any]) -> Any:
    """Generate a default value conforming to a JSON schema.

    Args:
        schema: JSON schema dict

    Returns:
        A value matching the schema type
    """
    if not schema:
        return None

    # Check for example first
    if 'example' in schema:
        return schema['example']

    schema_type = schema.get('type', 'object')

    if schema_type == 'string':
        enum = schema.get('enum')
        if enum:
            return enum[0]
        return schema.get('default', '')

    if schema_type == 'integer':
        return schema.get('default', 0)

    if schema_type == 'number':
        return schema.get('default', 0.0)

    if schema_type == 'boolean':
        return schema.get('default', False)

    if schema_type == 'array':
        return []

    if schema_type == 'object':
        result = {}
        properties = schema.get('properties', {})
        required = set(schema.get('required', []))
        for prop_name, prop_schema in properties.items():
            if prop_name in required:
                result[prop_name] = generate_default_from_schema(prop_schema)
        return result

    return None


def merge_with_schema_defaults(
    data: Dict[str, Any],
    schema: Dict[str, Any],
) -> Dict[str, Any]:
    """Merge user-provided data with schema defaults.

    Fills in required fields that are missing from data,
    using type-appropriate defaults from the schema.

    Args:
        data: User-provided resource data
        schema: Response JSON schema

    Returns:
        Merged data dict with all required fields filled
    """
    if not schema or schema.get('type') != 'object':
        return data

    result = dict(data)
    properties = schema.get('properties', {})
    required = set(schema.get('required', []))

    for prop_name, prop_schema in properties.items():
        if prop_name not in result:
            # Fill required fields with defaults
            if prop_name in required:
                result[prop_name] = generate_default_from_schema(prop_schema)
            # Also fill fields that have explicit defaults
            elif 'default' in prop_schema:
                result[prop_name] = prop_schema['default']

    return result


def unwrap_array_schema(schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """If schema is an array, return the items schema.

    Args:
        schema: JSON schema dict

    Returns:
        Items schema if array, None otherwise
    """
    if schema and schema.get('type') == 'array':
        return schema.get('items')
    return None
