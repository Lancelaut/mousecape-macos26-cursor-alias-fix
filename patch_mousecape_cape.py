#!/usr/bin/env python3
"""
Patch a Mousecape .cape file for macOS 26 / Tahoe cursor compatibility.

This tool does not include or distribute any cursor artwork. It only edits a
local .cape file that the user already has by adding compatibility aliases such
as ArrowS and IBeamS when the source cursor definitions exist.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import plistlib
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ALIASES: dict[str, str] = {
    "com.apple.coregraphics.ArrowS": "com.apple.coregraphics.Arrow",
    "com.apple.coregraphics.IBeamS": "com.apple.coregraphics.IBeam",
}

OPTIONAL_KEYS = (
    "com.apple.cursor.20",
    "com.apple.cursor.26",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_plist(path: Path) -> dict[str, Any]:
    try:
        data = plistlib.loads(path.read_bytes())
    except Exception as exc:  # noqa: BLE001 - CLI should show a concise error
        raise SystemExit(f"ERROR: failed to read plist/cape: {path}\n{exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: expected plist dictionary in {path}")
    return data


def run_plutil(path: Path) -> tuple[bool, str]:
    plutil = shutil.which("plutil")
    if not plutil:
        return True, "plutil not found; skipped platform plist validation"
    proc = subprocess.run(
        [plutil, "-lint", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode == 0, proc.stdout.strip()


def patch_cape(path: Path, *, dry_run: bool = False, no_backup: bool = False) -> int:
    if not path.exists():
        raise SystemExit(f"ERROR: file not found: {path}")
    if path.suffix.lower() != ".cape":
        print(f"WARNING: file does not end with .cape: {path}", file=sys.stderr)

    before_hash = sha256(path)
    data = load_plist(path)
    cursors = data.get("Cursors")
    if not isinstance(cursors, dict):
        raise SystemExit("ERROR: cape has no Cursors dictionary")

    cape_name = data.get("CapeName", "(unknown)")
    identifier = data.get("Identifier", "(unknown)")
    print(f"Cape: {cape_name}")
    print(f"Identifier: {identifier}")
    print(f"Cursor count before: {len(cursors)}")

    changed = False
    for dst, src in ALIASES.items():
        if dst in cursors:
            print(f"OK: {dst} already exists")
            continue
        if src not in cursors:
            print(f"SKIP: cannot add {dst}; source {src} is missing")
            continue
        if dry_run:
            print(f"WOULD ADD: {dst} from {src}")
        else:
            cursors[dst] = copy.deepcopy(cursors[src])
            print(f"ADDED: {dst} from {src}")
        changed = True

    for key in OPTIONAL_KEYS:
        print(f"{'OK' if key in cursors else 'NOTE'}: {key} {'exists' if key in cursors else 'is not present'}")

    if dry_run:
        print("Dry run only; no file written.")
        return 0

    if not changed:
        print("No changes needed.")
        return 0

    backup_path = None
    if not no_backup:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = path.with_name(path.name + f".bak-{timestamp}")
        shutil.copy2(path, backup_path)
        print(f"Backup: {backup_path}")

    path.write_bytes(plistlib.dumps(data, fmt=plistlib.FMT_XML, sort_keys=False))
    ok, lint_output = run_plutil(path)
    if not ok:
        if backup_path:
            shutil.copy2(backup_path, path)
            print(f"ERROR: plist validation failed; restored backup: {backup_path}", file=sys.stderr)
        raise SystemExit(lint_output or "ERROR: plist validation failed")

    after_data = load_plist(path)
    after_cursors = after_data.get("Cursors", {})
    print(f"Cursor count after: {len(after_cursors)}")
    print(f"SHA256 before: {before_hash}")
    print(f"SHA256 after:  {sha256(path)}")
    print(f"Validation: {lint_output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Patch a local Mousecape .cape file with macOS 26/Tahoe compatibility cursor aliases.",
    )
    parser.add_argument("cape", type=Path, help="Path to the .cape file to patch")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--no-backup", action="store_true", help="Do not create a timestamped .bak backup")
    args = parser.parse_args(argv)
    return patch_cape(args.cape.expanduser(), dry_run=args.dry_run, no_backup=args.no_backup)


if __name__ == "__main__":
    raise SystemExit(main())
