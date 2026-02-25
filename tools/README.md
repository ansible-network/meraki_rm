# Tools — Code Generation Pipeline

This directory contains generators that produce test scaffolding and
documentation from module source code.  The four Molecule-related tools
form a sequential pipeline; the model-test generator is independent.

## Molecule Pipeline

Run these four steps **in order** whenever module DOCUMENTATION changes,
states are added/removed, or sample data needs updating:

```
python tools/generate_examples.py            # Step 1
python tools/generate_molecule_scenarios.py  # Step 2
python tools/generate_check_scenarios.py     # Step 3
python tools/inject_examples.py              # Step 4
```

### Step 1 — `generate_examples.py`

Parses every `plugins/modules/meraki_*.py` DOCUMENTATION string and
emits one YAML task file per supported state into `examples/{module}/`.
These files are the **single source of truth** for both Molecule tests
and `ansible-doc` output.

Key configuration lives in this file:

| Constant              | Purpose                                              |
|-----------------------|------------------------------------------------------|
| `FIELD_SAMPLES`       | Realistic values for fields where `'example'` is invalid |
| `REPLACED_OVERRIDES`  | Alternate values so replaced/overridden actually change something |
| `RESPONSE_ONLY_FIELDS`| Server-computed fields excluded from expected configs |

### Step 2 — `generate_molecule_scenarios.py`

Reads the example files from Step 1 and creates full Molecule scenario
directories under `extensions/molecule/{module}/{state}/`.  Each
directory gets `molecule.yml`, `vars.yml`, `converge.yml`, `verify.yml`,
`prepare.yml`, and `cleanup.yml`.

Handles:
- Unique scope IDs for parallel-safe execution (`--workers cpus-1`)
- Seed data for overridden scenarios (two resources with distinct
  canonical keys)
- Simplified verify for modules without `gathered` support
- Automatic cleanup of stale scenario directories

### Step 3 — `generate_check_scenarios.py`

Creates a `check/` scenario alongside the state directories from Step 2.
Each check scenario validates that `check_mode: true` predicts changes
correctly **without** altering actual state.

### Step 4 — `inject_examples.py`

Reads the example files from Step 1 and writes them into the `EXAMPLES`
docstring of each module so `ansible-doc` stays in sync.  Can be wired
as a pre-commit hook (`--check` mode exits non-zero if anything is
stale).

## Independent Tool

### `generate_model_tests.py`

Generates unit tests for the data-model layer
(`plugins/plugin_utils/user_models/` and `plugins/plugin_utils/api/`).
Not part of the Molecule pipeline — run it separately when models
change.
