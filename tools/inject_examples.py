#!/usr/bin/env python3
"""Inject examples/{module}/*.yml into module EXAMPLES strings.

Reads per-state YAML task files from examples/{module}/ subdirectories,
concatenates them in a canonical order, and writes the combined content
into the EXAMPLES block of the corresponding plugins/modules/meraki_*.py.

This keeps ansible-doc output in sync with the example files that also
serve as Molecule test input.

Usage:
    python tools/inject_examples.py          # inject all
    python tools/inject_examples.py --check  # dry-run, exit 1 if stale
    python tools/inject_examples.py --diff   # show what would change

Pre-commit hook:
    - repo: local
      hooks:
        - id: inject-examples
          name: Sync examples into module EXAMPLES
          entry: python tools/inject_examples.py --check
          language: python
          pass_filenames: false
"""

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = PROJECT_ROOT / 'examples'
MODULES_DIR = PROJECT_ROOT / 'plugins' / 'modules'

EXAMPLES_RE = re.compile(
    r"(EXAMPLES\s*=\s*r?''').*?(''')",
    re.DOTALL,
)

STATE_ORDER = ['merged', 'replaced', 'overridden', 'gathered', 'deleted']


def collect_example_content(example_dir: Path) -> str:
    """Concatenate per-state YAML files in canonical order."""
    parts = []
    for state in STATE_ORDER:
        state_file = example_dir / f'{state}.yml'
        if state_file.exists():
            content = state_file.read_text().rstrip('\n')
            # Strip the leading `---` from non-first files to avoid multiple doc starts
            if parts and content.startswith('---'):
                content = content[3:].lstrip('\n')
            parts.append(content)

    return '\n\n'.join(parts)


def inject_one(example_dir: Path, dry_run=False, show_diff=False) -> bool:
    """Inject concatenated examples into a module file. Returns True if changed."""
    module_name = f'meraki_{example_dir.name}'
    module_path = MODULES_DIR / f'{module_name}.py'

    if not module_path.exists():
        print(f'  SKIP {example_dir.name}/: no module {module_path.name}')
        return False

    combined = collect_example_content(example_dir)
    if not combined:
        print(f'  SKIP {example_dir.name}/: no state files found')
        return False

    module_content = module_path.read_text()
    new_block = f"EXAMPLES = r'''\n{combined}\n'''"

    m = EXAMPLES_RE.search(module_content)
    if not m:
        print(f'  SKIP {module_path.name}: no EXAMPLES block found')
        return False

    old_block = m.group(0)
    if old_block == new_block:
        return False

    if show_diff:
        old_lines = old_block.split('\n')
        new_lines = new_block.split('\n')
        print(f'\n--- {module_path.name} ({len(old_lines)} lines)')
        for line in old_lines[:3]:
            print(f'  - {line}')
        print(f'  ... ({len(old_lines)} lines total)')
        print(f'+++ {module_path.name} ({len(new_lines)} lines)')
        for line in new_lines[:3]:
            print(f'  + {line}')
        print(f'  ... ({len(new_lines)} lines total)')

    if not dry_run:
        updated = module_content[:m.start()] + new_block + module_content[m.end():]
        module_path.write_text(updated)

    return True


def main():
    parser = argparse.ArgumentParser(description='Inject examples into module EXAMPLES strings')
    parser.add_argument('--check', action='store_true', help='Exit 1 if any module is stale')
    parser.add_argument('--diff', action='store_true', help='Show diffs without writing')
    args = parser.parse_args()

    dry_run = args.check or args.diff

    if not EXAMPLES_DIR.exists():
        print(f'ERROR: {EXAMPLES_DIR} not found')
        return 1

    example_dirs = sorted(
        d for d in EXAMPLES_DIR.iterdir()
        if d.is_dir() and not d.name.startswith('.')
    )

    if not example_dirs:
        print(f'WARNING: no module directories in {EXAMPLES_DIR}')
        return 0

    changed = 0
    up_to_date = 0

    for ed in example_dirs:
        result = inject_one(ed, dry_run=dry_run, show_diff=args.diff)
        if result:
            changed += 1
            action = 'STALE' if dry_run else 'UPDATED'
            state_files = [f.stem for f in sorted(ed.glob('*.yml'))]
            print(f'  {action} meraki_{ed.name}.py <- {ed.name}/ ({", ".join(state_files)})')
        else:
            up_to_date += 1

    total = changed + up_to_date
    print(f'\n{"="*60}')
    if dry_run:
        print(f'Check: {changed} stale, {up_to_date} up-to-date (of {total})')
    else:
        print(f'Injected: {changed} updated, {up_to_date} unchanged (of {total})')

    if args.check and changed > 0:
        print('Run `python tools/inject_examples.py` to update.')
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
