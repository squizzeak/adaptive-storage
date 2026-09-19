#!/usr/bin/env python3
"""Offline distribution checks. Does not certify host runtime behavior."""
from __future__ import annotations
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from build import ROOT, SKILLS, build, inventory


def validate_links(root: Path) -> None:
    for document in root.rglob('*.md'):
        if '.git' in document.parts:
            continue
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
            target = raw.strip('<>')
            if urlsplit(target).scheme or target.startswith('#'):
                continue
            path = unquote(target.split('#', 1)[0])
            if not path:
                continue
            resolved = (document.parent / path).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                raise ValueError(f'Broken/outside link: {document.relative_to(root)} -> {raw}')


def validate(root: Path) -> None:
    build(root, check=True)
    for name in SKILLS:
        text = (root / 'skills' / name / 'SKILL.md').read_text()
        if not text.startswith('---\n'):
            raise ValueError(f'Missing frontmatter: {name}')
        header = text.split('---\n', 2)[1]
        fields = dict(line.split(': ', 1) for line in header.splitlines() if ': ' in line)
        if fields.get('name') != name or not fields.get('description'):
            raise ValueError(f'Invalid skill metadata: {name}')
        if '[TODO' in text:
            raise ValueError(f'Unfinished skill: {name}')
    plugin = root / 'plugins/adaptive-storage'
    versions = set()
    for path in (plugin / 'plugin.json', plugin / '.codex-plugin/plugin.json', plugin / '.claude-plugin/plugin.json'):
        data = json.loads(path.read_text())
        if data['name'] != 'adaptive-storage' or not data['description']:
            raise ValueError(f'Invalid plugin identity: {path}')
        versions.add(data['version'])
        if any(field in data for field in ('mcpServers', 'apps', 'hooks')):
            raise ValueError('Skill-only package has an unexpected runtime dependency')
    if len(versions) != 1:
        raise ValueError('Plugin versions differ')
    codex = json.loads((root / '.agents/plugins/marketplace.json').read_text())
    claude = json.loads((root / '.claude-plugin/marketplace.json').read_text())
    if codex['plugins'][0]['source']['path'] != './plugins/adaptive-storage':
        raise ValueError('Invalid Codex marketplace source')
    if claude['plugins'][0]['source'] != './plugins/adaptive-storage':
        raise ValueError('Invalid Claude marketplace source')
    for path in root.rglob('*.json'):
        if '.git' not in path.parts:
            json.loads(path.read_text())
    if json.loads((root / 'package.json').read_text())['pi']['skills'] != ['./skills']:
        raise ValueError('Pi package must include both skills')
    names = inventory(plugin)
    if any(name.endswith(('.py', '.js', '.ts')) or 'mcp.json' in name for name in names):
        raise ValueError('Runtime code/server configuration found in skill-only bundle')
    validate_links(root)
    print('Validated sibling skills, package identity, generated parity, JSON, local links, and skill-only boundary')


if __name__ == '__main__':
    validate(ROOT)
