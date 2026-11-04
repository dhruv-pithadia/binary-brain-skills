#!/usr/bin/env python3
"""Read-only tool and machine check; no downloads or provider calls."""
import argparse
import json
import platform
import shutil
import subprocess
from pathlib import Path


def probe(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    args = parser.parse_args()
    disk_path = args.project.expanduser().resolve()
    while not disk_path.exists():
        disk_path = disk_path.parent
    if disk_path.is_file():
        disk_path = disk_path.parent
    tools = {name: shutil.which(name) for name in ('node', 'npx', 'ffmpeg', 'ffprobe')}
    blender = shutil.which('blender')
    if not blender and platform.system() == 'Darwin':
        candidate = Path('/Applications/Blender.app/Contents/MacOS/Blender')
        blender = str(candidate) if candidate.is_file() else None
    raw_ram = probe(['sysctl', '-n', 'hw.memsize']) if platform.system() == 'Darwin' else None
    ram = int(raw_ram) if raw_ram and raw_ram.isdigit() else None
    cpu = probe(['sysctl', '-n', 'machdep.cpu.brand_string']) if platform.system() == 'Darwin' else None
    missing = [name for name, path in tools.items() if not path]
    print(json.dumps({
        'status': 'missing-tools' if missing else 'base-tools-found',
        'system': platform.system(), 'architecture': platform.machine(), 'cpu': cpu,
        'total_ram_bytes': ram, 'total_ram_gib': ram / 2**30 if ram else None,
        'available_ram_bytes': None,
        'available_ram_note': 'Check current memory pressure before heavy stages; total RAM is not free RAM.',
        'disk_checked_at': str(disk_path), 'free_disk_gib': round(shutil.disk_usage(disk_path).free / 2**30, 2),
        'tools': tools, 'missing_required_tools': missing, 'optional_blender': blender,
        'defaults': {'engine': 'HTML/SVG', 'draft_width': 540, 'draft_height': 960,
                     'fps': 30, 'heavy_processes': 1, 'install_blender': False},
        'note': 'Base CLI availability is not a render benchmark. HyperFrames and voice/alignment providers still need validation. No model, renderer or Blender was installed or launched.'
    }, indent=2))
    return 1 if missing else 0


if __name__ == '__main__':
    raise SystemExit(main())
