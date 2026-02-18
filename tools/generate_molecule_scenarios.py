#!/usr/bin/env python3
"""Generate Molecule scenarios from examples/{module}/ state files.

For each module directory under examples/, creates a Molecule scenario:

    extensions/molecule/{module}/
        molecule.yml      # inherits shared config
        converge.yml      # include_tasks: examples/{module}/merged.yml
        verify.yml        # include_tasks: examples/{module}/gathered.yml
        cleanup.yml       # include_tasks: examples/{module}/deleted.yml (if exists)

The converge step runs the merged example (create/update), which is
idempotent on re-run — satisfying Molecule's idempotence check.

Replaced and overridden states can be tested via additional scenarios
or by extending the converge playbook manually.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = PROJECT_ROOT / 'examples'
MOLECULE_DIR = PROJECT_ROOT / 'extensions' / 'molecule'

# Relative path from molecule scenario dir to examples
# extensions/molecule/{module}/converge.yml -> ../../../examples/{module}/merged.yml
EXAMPLES_REL = '../../../examples'


def gen_molecule_yml(module_name: str) -> str:
    return f"""---
# Molecule scenario for {module_name}
# Inherits shared config from ../config.yml
"""


def gen_converge(module_name: str, has_replaced: bool) -> str:
    lines = [f"""---
- name: "Converge — {module_name}"
  hosts: localhost
  gather_facts: false
  tasks:
    - name: "Run merged examples"
      ansible.builtin.include_tasks:
        file: "{EXAMPLES_REL}/{module_name}/merged.yml"
"""]

    if has_replaced:
        lines.append(f"""    - name: "Run replaced examples"
      ansible.builtin.include_tasks:
        file: "{EXAMPLES_REL}/{module_name}/replaced.yml"
""")

    return '\n'.join(lines)


def gen_verify(module_name: str) -> str:
    return f"""---
- name: "Verify — {module_name}"
  hosts: localhost
  gather_facts: false
  tasks:
    - name: "Run gathered examples"
      ansible.builtin.include_tasks:
        file: "{EXAMPLES_REL}/{module_name}/gathered.yml"

    - name: "Assert gathered config is not empty"
      ansible.builtin.assert:
        that:
          - gathered.config is defined
          - gathered.config | length > 0
        fail_msg: "Gathered config is empty — expected at least one resource"
"""


def gen_cleanup(module_name: str) -> str:
    return f"""---
- name: "Cleanup — {module_name}"
  hosts: localhost
  gather_facts: false
  tasks:
    - name: "Run deleted examples"
      ansible.builtin.include_tasks:
        file: "{EXAMPLES_REL}/{module_name}/deleted.yml"
"""


def gen_cleanup_no_delete(module_name: str) -> str:
    """For singletons that don't support delete, cleanup is a no-op."""
    return f"""---
- name: "Cleanup — {module_name}"
  hosts: localhost
  gather_facts: false
  tasks:
    - name: "No cleanup needed (singleton resource)"
      ansible.builtin.debug:
        msg: "{module_name} does not support delete — nothing to clean up"
"""


def gen_facts_converge() -> str:
    return f"""---
- name: "Converge — facts"
  hosts: localhost
  gather_facts: false
  tasks:
    - name: "Run gathered examples"
      ansible.builtin.include_tasks:
        file: "{EXAMPLES_REL}/facts/gathered.yml"
"""


def gen_facts_verify() -> str:
    return f"""---
- name: "Verify — facts"
  hosts: localhost
  gather_facts: false
  tasks:
    - name: "Assert facts were gathered"
      ansible.builtin.assert:
        that:
          - all_facts is defined
        fail_msg: "Facts gathering returned no data"
"""


def main():
    example_dirs = sorted(
        d for d in EXAMPLES_DIR.iterdir()
        if d.is_dir() and not d.name.startswith('.')
    )

    if not example_dirs:
        print(f'ERROR: no module directories in {EXAMPLES_DIR}')
        return 1

    created_scenarios = 0
    created_files = 0

    for ed in example_dirs:
        module_name = ed.name
        scenario_dir = MOLECULE_DIR / module_name
        scenario_dir.mkdir(parents=True, exist_ok=True)

        states = {f.stem for f in ed.glob('*.yml')}
        is_facts = module_name == 'facts'

        # molecule.yml
        (scenario_dir / 'molecule.yml').write_text(gen_molecule_yml(module_name))
        created_files += 1

        if is_facts:
            (scenario_dir / 'converge.yml').write_text(gen_facts_converge())
            (scenario_dir / 'verify.yml').write_text(gen_facts_verify())
            created_files += 2
        else:
            # converge.yml — runs merged (and optionally replaced)
            has_replaced = 'replaced' in states
            (scenario_dir / 'converge.yml').write_text(
                gen_converge(module_name, has_replaced)
            )
            created_files += 1

            # verify.yml — runs gathered + assertions
            if 'gathered' in states:
                (scenario_dir / 'verify.yml').write_text(gen_verify(module_name))
                created_files += 1

            # cleanup.yml — runs deleted or no-op
            if 'deleted' in states:
                (scenario_dir / 'cleanup.yml').write_text(gen_cleanup(module_name))
            else:
                (scenario_dir / 'cleanup.yml').write_text(gen_cleanup_no_delete(module_name))
            created_files += 1

        created_scenarios += 1
        state_list = ', '.join(sorted(states))
        print(f'  OK {module_name}/ ({state_list})')

    print(f'\n{"="*60}')
    print(f'Created: {created_scenarios} scenarios, {created_files} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
