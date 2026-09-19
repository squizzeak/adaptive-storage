#!/usr/bin/env python3
"""Maintainer-only deterministic skill bundle builder; not a sync runtime."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('adaptive-storage', 'storage-init')


def inventory(directory: Path) -> dict[str, bytes]:
    result = {}
    if directory.is_symlink():
        raise ValueError(f'Symlink directory is not package content: {directory}')
    if not directory.exists():
        return result
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Symlink is not package content: {path}')
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = path.read_bytes()
    return result


def build(root: Path, check: bool = False) -> None:
    plugin = root / 'plugins' / 'adaptive-storage'
    # Never follow a substituted output path into user data.
    for target in (root / 'plugins', plugin, plugin / 'skills'):
        if target.is_symlink():
            raise ValueError(f'Refusing symlink output: {target}')
    expected = inventory(root / 'skills')
    if not expected or any(f'{name}/SKILL.md' not in expected for name in SKILLS):
        raise ValueError('Both canonical sibling skills are required')
    actual = inventory(plugin / 'skills')
    if check:
        if expected != actual:
            raise ValueError('Generated skills differ; run python3 scripts/build.py')
    else:
        # This directory is explicitly generated and contains no user state.
        destination = plugin / 'skills'
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(root / 'skills', destination)
    for name in ('LICENSE', 'PRIVACY.md'):
        source = root / name
        target = plugin / name
        if target.is_symlink():
            raise ValueError(f'Refusing symlink output: {target}')
        if check:
            if not target.exists() or source.read_bytes() != target.read_bytes():
                raise ValueError(f'Generated {name} differs')
        else:
            shutil.copyfile(source, target)


def archive(root: Path, output: Path) -> None:
    build(root, check=True)
    plugin = root / 'plugins' / 'adaptive-storage'
    contents = inventory(plugin)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive output avoids overwriting an existing deliverable.
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, data in sorted(contents.items()):
            info = zipfile.ZipInfo('adaptive-storage/' + name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    build(ROOT, check=args.check)
    if args.archive:
        archive(ROOT, args.archive)
    print('Bundle verified' if args.check else 'Bundle built')


if __name__ == '__main__':
    main()
