#!/usr/bin/env python3
"""Validate the shared skill collection and local Markdown resource links."""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []
names = set()
skills = sorted((ROOT / "skills").iterdir())
if not skills:
    errors.append("No skills found")
for folder in skills:
    manifest = folder / "SKILL.md"
    if not folder.is_dir() or not manifest.is_file():
        errors.append(f"{folder.name}: missing SKILL.md")
        continue
    text = manifest.read_text()
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not match:
        errors.append(f"{folder.name}: invalid frontmatter")
        continue
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"{folder.name}: invalid YAML: {exc}")
        continue
    if not isinstance(metadata, dict):
        errors.append(f"{folder.name}: frontmatter must be a mapping")
        continue
    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append(f"{folder.name}: invalid skill name")
    elif name != folder.name or name in names:
        errors.append(f"{folder.name}: folder/name mismatch or duplicate name")
    else:
        names.add(name)
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append(f"{folder.name}: description must be nonempty and at most 1024 characters")
    for path in folder.rglob("*"):
        if path.is_symlink():
            errors.append(f"{path.relative_to(ROOT)}: symlinks are not part of this collection")
        if not path.is_file() or path.suffix not in {".md", ".yaml"}:
            continue
        content = path.read_text()
        if "\u2014" in content or "/Users/" in content:
            errors.append(f"{path.relative_to(ROOT)}: em dash or personal absolute path")
        if path.suffix == ".yaml":
            try:
                yaml.safe_load(content)
            except yaml.YAMLError as exc:
                errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                local = target.split("#", 1)[0]
                if local and not (path.parent / local).exists():
                    errors.append(f"{path.relative_to(ROOT)}: missing resource {local}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Validated {len(skills)} canonical skills and their local Markdown links.")
