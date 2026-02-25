#!/usr/bin/env python3
"""Generate data-model unit tests (standalone — not part of the Molecule pipeline).

Introspects each user model's ``_field_mapping`` and paired API model to
emit sibling ``*_test.py`` files that verify:

  - Forward transform  (User → API)
  - Reverse transform  (API → User)
  - Roundtrip          (User → API → User)
  - Scope param exclusion
  - Endpoint operations validity  (``api/v1/`` only)
  - Generated dataclass field existence  (``api/v1/generated/`` only)

This tool is independent of the Molecule example/scenario pipeline; it
targets the ``plugins/plugin_utils/`` model layer.

Usage::

    python tools/generate_model_tests.py            # write all *_test.py
    python tools/generate_model_tests.py --check     # dry-run
"""

import argparse
import importlib
import inspect
import json
import re
import sys
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).parent.parent
PLUGINS_DIR = PROJECT_ROOT / "plugins" / "plugin_utils"
USER_MODELS_DIR = PLUGINS_DIR / "user_models"
API_V1_DIR = PLUGINS_DIR / "api" / "v1"
GENERATED_DIR = API_V1_DIR / "generated"
SPEC_PATH = PROJECT_ROOT / "spec3.json"

# Ensure project root is importable
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Sample value generation
# ---------------------------------------------------------------------------

def _sample_value(type_hint: str, field_name: str) -> str:
    """Return a Python literal string for a sample value based on type hint."""
    if "bool" in type_hint.lower():
        return "True"
    if "int" in type_hint.lower():
        return "24"
    if "float" in type_hint.lower():
        return "1.5"
    if "List[Dict" in type_hint:
        return "[{'key': 'value'}]"
    if "Dict[str, Dict" in type_hint:
        return "{'k1': {'ip': '10.0.0.1', 'name': 'host'}}"
    if "Dict" in type_hint:
        return "{'enabled': True}"
    if "List[str]" in type_hint:
        return "['item1', 'item2']"
    if "List" in type_hint:
        return "['a', 'b']"
    return f"'{field_name}_val'"


def _type_hint_str(f) -> str:
    """Get a string representation of a dataclass field's type."""
    hint = f.type
    if isinstance(hint, str):
        return hint
    return getattr(hint, "__name__", str(hint))


# ---------------------------------------------------------------------------
# Model introspection
# ---------------------------------------------------------------------------

def _load_module(dotted_path: str):
    """Import a module by dotted path."""
    return importlib.import_module(dotted_path)


def _find_user_model_class(mod):
    """Find the User* dataclass in a module."""
    for name, obj in inspect.getmembers(mod, inspect.isclass):
        if name.startswith("User") and is_dataclass(obj):
            return name, obj
    return None, None


def _find_api_class(mod):
    """Find the API*_v1 dataclass in a module."""
    for name, obj in inspect.getmembers(mod, inspect.isclass):
        if name.startswith("API") and is_dataclass(obj) and "_v1" in name:
            return name, obj
    return None, None


def _find_generated_class(mod):
    """Find the generated dataclass in a module."""
    for name, obj in inspect.getmembers(mod, inspect.isclass):
        if is_dataclass(obj) and not name.startswith("API") and not name.startswith("User"):
            return name, obj
    return None, None


def _get_field_mapping(cls) -> Optional[Dict[str, str]]:
    """Extract _field_mapping from a class (if it has one)."""
    mapping = getattr(cls, "_field_mapping", None)
    if mapping and isinstance(mapping, dict):
        return dict(mapping)
    return None


def _get_scope_fields(cls) -> List[str]:
    """Identify scope fields (present on dataclass but absent from _field_mapping)."""
    if not is_dataclass(cls):
        return []
    mapping = _get_field_mapping(cls) or {}
    dc_fields = {f.name for f in fields(cls)}
    mapped = set(mapping.keys())
    return sorted(dc_fields - mapped - {"_field_mapping"})


def _get_endpoint_operations(api_cls) -> Optional[Dict]:
    """Get endpoint operations if the class has them."""
    method = getattr(api_cls, "get_endpoint_operations", None)
    if method and callable(method):
        try:
            ops = method()
            if ops:
                return ops
        except Exception:
            pass
    return None


# ---------------------------------------------------------------------------
# Tier 1: user_models/{name}_test.py
# ---------------------------------------------------------------------------

def _generate_user_model_test(
    module_name: str,
    user_cls_name: str,
    user_cls,
    mapping: Dict[str, str],
    scope_fields: List[str],
) -> str:
    """Generate test content for a user model."""
    dc_fields = {f.name: f for f in fields(user_cls)}
    lines = [
        f'"""Colocated tests for {user_cls_name} — forward transform & scope exclusion."""',
        "",
        "from dataclasses import fields as dc_fields",
        f"from . import {module_name}",
        "",
        "",
        "def _ctx():",
        "    return {'manager': None, 'cache': {}}",
        "",
        "",
        f"class TestInstantiation:",
        f'    """Verify {user_cls_name} can be constructed with all fields."""',
        "",
        "    def test_defaults(self):",
        f"        obj = {module_name}.{user_cls_name}()",
        "        for f in dc_fields(obj):",
        "            if f.name.startswith('_'):",
        "                continue",
        "            assert getattr(obj, f.name) is None",
        "",
    ]

    # Forward transform test
    sample_kwargs = {}
    for user_field, api_field in mapping.items():
        if user_field in dc_fields:
            hint = _type_hint_str(dc_fields[user_field])
            sample_kwargs[user_field] = _sample_value(hint, user_field)

    if sample_kwargs:
        lines.append("")
        lines.append(f"class TestForwardTransform:")
        lines.append(f'    """{user_cls_name} -> API (to_api) field mapping."""')
        lines.append("")
        lines.append("    def test_mapped_fields(self):")
        lines.append(f"        user = {module_name}.{user_cls_name}(")
        for k, v in sample_kwargs.items():
            lines.append(f"            {k}={v},")
        lines.append("        )")
        lines.append("        api = user.to_api(_ctx())")
        lines.append("")
        for user_field, api_field in mapping.items():
            if user_field in sample_kwargs:
                lines.append(f"        assert api.{api_field} == user.{user_field}")
        lines.append("")

        lines.append("    def test_none_fields_omitted(self):")
        first_field = next(iter(mapping))
        first_val = sample_kwargs.get(first_field, "'x'")
        lines.append(f"        user = {module_name}.{user_cls_name}({first_field}={first_val})")
        lines.append("        api = user.to_api(_ctx())")
        lines.append(f"        assert api.{mapping[first_field]} == user.{first_field}")
        # Pick a field that should be None
        other_fields = [f for f in mapping if f != first_field]
        if other_fields:
            of = other_fields[0]
            lines.append(f"        assert getattr(api, '{mapping[of]}', None) is None")
        lines.append("")

    # Scope exclusion test
    if scope_fields:
        lines.append("")
        lines.append(f"class TestScopeExclusion:")
        lines.append(f'    """Scope params must not appear in API output."""')
        lines.append("")
        lines.append("    def test_scope_not_in_api(self):")
        scope_kwargs = ", ".join(f"{s}='{s}_val'" for s in scope_fields)
        first_mapped = next(iter(mapping))
        first_val = sample_kwargs.get(first_mapped, "'x'")
        lines.append(f"        user = {module_name}.{user_cls_name}({scope_kwargs}, {first_mapped}={first_val})")
        lines.append("        api = user.to_api(_ctx())")
        lines.append("        api_field_names = {f.name for f in dc_fields(api)}")
        for s in scope_fields:
            lines.append(f"        assert '{s}' not in api_field_names or getattr(api, '{s}', None) is None")
        lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Tier 2: api/v1/{name}_test.py
# ---------------------------------------------------------------------------

def _generate_api_model_test(
    module_name: str,
    api_cls_name: str,
    api_cls,
    user_module_name: str,
    user_cls_name: str,
    user_cls,
    mapping: Dict[str, str],
    scope_fields: List[str],
) -> str:
    """Generate test content for an API model."""
    api_dc_fields = {f.name: f for f in fields(api_cls)}
    user_dc_fields = {f.name: f for f in fields(user_cls)}

    api_alias = f"{module_name}_api"
    user_alias = f"{module_name}_user"

    lines = [
        f'"""Colocated tests for {api_cls_name} — reverse transform, roundtrip & endpoints."""',
        "",
        "from dataclasses import fields as dc_fields",
        f"from . import {module_name} as {api_alias}",
        f"from ...user_models import {user_module_name} as {user_alias}",
        "",
        "",
        "def _ctx():",
        "    return {'manager': None, 'cache': {}}",
        "",
    ]

    # Reverse transform test
    reverse_kwargs = {}
    for user_field, api_field in mapping.items():
        if api_field in api_dc_fields:
            hint = _type_hint_str(api_dc_fields[api_field])
            reverse_kwargs[api_field] = _sample_value(hint, api_field)

    if reverse_kwargs:
        lines.append("")
        lines.append(f"class TestReverseTransform:")
        lines.append(f'    """API -> User (to_ansible) field mapping."""')
        lines.append("")
        lines.append("    def test_mapped_fields(self):")
        lines.append(f"        api = {api_alias}.{api_cls_name}(")
        for k, v in reverse_kwargs.items():
            lines.append(f"            {k}={v},")
        lines.append("        )")
        lines.append("        user = api.to_ansible(_ctx())")
        lines.append("")
        for user_field, api_field in mapping.items():
            if api_field in reverse_kwargs:
                lines.append(f"        assert user.{user_field} == api.{api_field}")
        lines.append("")

    # Roundtrip test
    if mapping:
        lines.append("")
        lines.append(f"class TestRoundtrip:")
        lines.append(f'    """User -> API -> User preserves all mapped fields."""')
        lines.append("")
        lines.append("    def test_roundtrip(self):")

        # Build user kwargs from mapping
        user_sample = {}
        for user_field in mapping:
            if user_field in user_dc_fields:
                hint = _type_hint_str(user_dc_fields[user_field])
                user_sample[user_field] = _sample_value(hint, user_field)

        lines.append(f"        original = {user_alias}.{user_cls_name}(")
        for k, v in user_sample.items():
            lines.append(f"            {k}={v},")
        lines.append("        )")
        lines.append("        ctx = _ctx()")
        lines.append("        api = original.to_api(ctx)")
        lines.append("        roundtripped = api.to_ansible(ctx)")
        lines.append("")
        for user_field in user_sample:
            lines.append(f"        assert roundtripped.{user_field} == original.{user_field}")
        lines.append("")

    # Endpoint operations test
    ops = _get_endpoint_operations(api_cls)
    if ops:
        lines.append("")
        lines.append(f"class TestEndpointOperations:")
        lines.append(f'    """Validate endpoint operations are well-formed."""')
        lines.append("")
        lines.append("    def test_operations_exist(self):")
        lines.append(f"        ops = {api_alias}.{api_cls_name}.get_endpoint_operations()")
        lines.append(f"        assert len(ops) > 0")
        lines.append("")
        lines.append("    def test_operations_have_required_fields(self):")
        lines.append(f"        ops = {api_alias}.{api_cls_name}.get_endpoint_operations()")
        lines.append("        for name, op in ops.items():")
        lines.append("            assert op.path, f'{name} missing path'")
        lines.append("            assert op.method, f'{name} missing method'")
        lines.append("            assert op.path_params is not None, f'{name} missing path_params'")
        lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Tier 3: api/v1/generated/{name}_test.py (drift detection)
# ---------------------------------------------------------------------------

_SPEC_CACHE: Optional[Dict] = None


def _load_spec() -> Dict:
    """Load spec3.json (cached)."""
    global _SPEC_CACHE
    if _SPEC_CACHE is None:
        with open(SPEC_PATH) as f:
            _SPEC_CACHE = json.load(f)
    return _SPEC_CACHE


def _extract_source_paths(gen_path: Path) -> List[str]:
    """Parse 'Source paths:' section from the generated file's docstring."""
    paths = []
    in_source = False
    with open(gen_path) as f:
        for line in f:
            if "Source paths:" in line:
                in_source = True
                continue
            if in_source:
                stripped = line.strip()
                if stripped.startswith("/"):
                    paths.append(stripped)
                elif stripped.startswith('"""') or stripped == "":
                    if paths:
                        break
                else:
                    break
    return paths


def _extract_spec_fields_for_paths(spec: Dict, source_paths: List[str]) -> set:
    """Extract all property names from request and response schemas for the given API paths."""
    all_fields: set = set()
    spec_paths = spec.get("paths", {})

    def _collect_from_schema(schema: dict):
        if schema.get("type") == "array":
            schema = schema.get("items", {})
        props = schema.get("properties", {})
        all_fields.update(props.keys())

    for api_path in source_paths:
        path_obj = spec_paths.get(api_path, {})
        for method_name, method_obj in path_obj.items():
            if method_name in ("parameters", "servers", "summary", "description"):
                continue
            # Response schemas
            responses = method_obj.get("responses", {})
            for status, resp_obj in responses.items():
                if not status.startswith("2"):
                    continue
                content = resp_obj.get("content", {})
                for media, media_obj in content.items():
                    _collect_from_schema(media_obj.get("schema", {}))
            # Request body schemas
            req_body = method_obj.get("requestBody", {})
            req_content = req_body.get("content", {})
            for media, media_obj in req_content.items():
                _collect_from_schema(media_obj.get("schema", {}))

    return all_fields


def _generate_generated_test(
    module_name: str,
    gen_cls_name: str,
    gen_cls,
    gen_path: Path,
) -> str:
    """Generate drift-detection test for a generated dataclass."""
    dc_field_names = sorted(f.name for f in fields(gen_cls))

    # Try to extract spec-derived fields for a drift comparison
    source_paths = _extract_source_paths(gen_path)
    spec_fields: Optional[set] = None
    if source_paths:
        spec = _load_spec()
        spec_fields = _extract_spec_fields_for_paths(spec, source_paths)

    lines = [
        f'"""Drift-detection tests for generated {gen_cls_name} dataclass."""',
        "",
        "from dataclasses import fields as dc_fields, is_dataclass",
        f"from . import {module_name}",
        "",
        "",
        f"class TestSchema:",
        f'    """{gen_cls_name} field inventory — catches regeneration drift."""',
        "",
        "    def test_is_dataclass(self):",
        f"        assert is_dataclass({module_name}.{gen_cls_name})",
        "",
        "    def test_expected_fields_exist(self):",
        f"        field_names = {{f.name for f in dc_fields({module_name}.{gen_cls_name}())}}",
        f"        expected = {set(dc_field_names)!r}",
        "        assert expected.issubset(field_names), f'Missing fields: {expected - field_names}'",
        "",
        "    def test_all_fields_optional(self):",
        f'        """Every generated field should default to None (all Optional)."""',
        f"        obj = {module_name}.{gen_cls_name}()",
        "        for f in dc_fields(obj):",
        "            assert getattr(obj, f.name) is None, f'{f.name} is not None by default'",
        "",
        f"    def test_field_count(self):",
        f'        """Guard against silent field additions or removals."""',
        f"        assert len(dc_fields({module_name}.{gen_cls_name}())) == {len(dc_field_names)}",
        "",
    ]

    # Add spec drift test if we found spec fields
    if spec_fields:
        lines.append("")
        lines.append(f"class TestSpecDrift:")
        lines.append(f'    """Cross-reference dataclass fields against spec3.json response schemas."""')
        lines.append("")
        lines.append(f"    SPEC_FIELDS = {sorted(spec_fields)!r}")
        lines.append("")
        lines.append("    def test_dataclass_covers_spec(self):")
        lines.append(f'        """Every spec response property should have a dataclass field."""')
        lines.append(f"        dc_names = {{f.name for f in dc_fields({module_name}.{gen_cls_name}())}}")
        lines.append(f"        spec_set = set(self.SPEC_FIELDS)")
        lines.append(f"        missing = spec_set - dc_names")
        lines.append(f"        assert not missing, f'Spec fields missing from dataclass: {{missing}}'")
        lines.append("")
        lines.append("    def test_dataclass_no_extra_fields(self):")
        lines.append(f'        """Warn if the dataclass has fields not in the spec (may indicate stale fields)."""')
        lines.append(f"        dc_names = {{f.name for f in dc_fields({module_name}.{gen_cls_name}())}}")
        lines.append(f"        spec_set = set(self.SPEC_FIELDS)")
        lines.append(f"        extras = dc_names - spec_set")
        lines.append(f"        assert not extras, (")
        lines.append(f"            f'Dataclass has fields not in spec responses: {{extras}}. '")
        lines.append(f"            f'These may be stale or from request-only schemas.'")
        lines.append(f"        )")
        lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def _discover_model_pairs() -> List[Tuple[str, Path, Path]]:
    """Find all (module_name, user_model_path, api_v1_path) triples."""
    pairs = []
    for user_path in sorted(USER_MODELS_DIR.glob("*.py")):
        name = user_path.stem
        if name.startswith("_") or name.endswith("_test"):
            continue
        api_path = API_V1_DIR / f"{name}.py"
        if api_path.exists():
            pairs.append((name, user_path, api_path))
    return pairs


def _discover_generated() -> List[Tuple[str, Path]]:
    """Find all (module_name, generated_path) pairs."""
    results = []
    for p in sorted(GENERATED_DIR.glob("*.py")):
        name = p.stem
        if name.startswith("_") or name.endswith("_test"):
            continue
        results.append((name, p))
    return results


def generate_all(check_only: bool = False) -> Tuple[int, int, int]:
    """Generate all test files. Returns (created, skipped, errors)."""
    created = skipped = errors = 0

    # Tier 1 & 2: user_models + api/v1
    for name, user_path, api_path in _discover_model_pairs():
        try:
            user_mod = _load_module(f"plugins.plugin_utils.user_models.{name}")
            api_mod = _load_module(f"plugins.plugin_utils.api.v1.{name}")
        except Exception as e:
            print(f"  SKIP {name}: import error: {e}")
            skipped += 1
            continue

        user_cls_name, user_cls = _find_user_model_class(user_mod)
        api_cls_name, api_cls = _find_api_class(api_mod)

        if not user_cls or not api_cls:
            print(f"  SKIP {name}: missing User or API class")
            skipped += 1
            continue

        mapping = _get_field_mapping(user_cls)
        if not mapping:
            print(f"  SKIP {name}: no _field_mapping (special model)")
            skipped += 1
            continue

        scope_fields = _get_scope_fields(user_cls)

        # Tier 1
        user_test_path = user_path.with_name(f"{name}_test.py")
        user_test_content = _generate_user_model_test(
            name, user_cls_name, user_cls, mapping, scope_fields,
        )
        if not check_only:
            user_test_path.write_text(user_test_content)
        print(f"  {'CHECK' if check_only else 'OK'} user_models/{name}_test.py")
        created += 1

        # Tier 2
        api_test_path = api_path.with_name(f"{name}_test.py")
        api_test_content = _generate_api_model_test(
            name, api_cls_name, api_cls,
            name, user_cls_name, user_cls,
            mapping, scope_fields,
        )
        if not check_only:
            api_test_path.write_text(api_test_content)
        print(f"  {'CHECK' if check_only else 'OK'} api/v1/{name}_test.py")
        created += 1

    # Tier 3: generated
    for name, gen_path in _discover_generated():
        try:
            gen_mod = _load_module(f"plugins.plugin_utils.api.v1.generated.{name}")
        except Exception as e:
            print(f"  SKIP generated/{name}: import error: {e}")
            skipped += 1
            continue

        gen_cls_name, gen_cls = _find_generated_class(gen_mod)
        if not gen_cls:
            print(f"  SKIP generated/{name}: no dataclass found")
            skipped += 1
            continue

        gen_test_path = gen_path.with_name(f"{name}_test.py")
        gen_test_content = _generate_generated_test(name, gen_cls_name, gen_cls, gen_path)
        if not check_only:
            gen_test_path.write_text(gen_test_content)
        print(f"  {'CHECK' if check_only else 'OK'} api/v1/generated/{name}_test.py")
        created += 1

    return created, skipped, errors


def main():
    parser = argparse.ArgumentParser(description="Generate colocated *_test.py files")
    parser.add_argument("--check", action="store_true", help="Dry run")
    args = parser.parse_args()

    print("Generating colocated unit tests...")
    created, skipped, errors = generate_all(check_only=args.check)
    print(f"\n{'Would create' if args.check else 'Created'}: {created} | Skipped: {skipped} | Errors: {errors}")


if __name__ == "__main__":
    main()
