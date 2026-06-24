# Mousecape macOS 26 Cursor Alias Fix

A small local patch tool for Mousecape `.cape` files affected by macOS 26 / Tahoe cursor replacement changes.

On macOS 26, some older Mousecape capes may appear to apply successfully, but the main arrow cursor, I-beam cursor, or crosshair-like cursors still fall back to the system default. One practical compatibility workaround is to add newer cursor keys to the cape by duplicating the existing local cursor definitions.

This repository does **not** include, redistribute, or generate any Apple cursor artwork. It only patches a `.cape` file that you already have on your own Mac.

## What it changes

The script adds these aliases when possible:

| New compatibility key | Source key copied from |
| --- | --- |
| `com.apple.coregraphics.ArrowS` | `com.apple.coregraphics.Arrow` |
| `com.apple.coregraphics.IBeamS` | `com.apple.coregraphics.IBeam` |

It also reports whether these keys already exist:

- `com.apple.cursor.20`
- `com.apple.cursor.26`

Those keys are not created by default because they may represent different cursor families in different capes.

## Why this exists

Mousecape historically worked by replacing system cursor definitions. In macOS 26 / Tahoe, some cursor families appear to use additional keys. Older capes often only contain legacy keys, so replacement can be partial.

This tool is a local migration helper for affected capes. It is not a full Mousecape fork and does not modify Mousecape itself.

## Usage

First, find your cape file. Common Mousecape cape location:

```bash
~/Library/Application\ Support/Mousecape/capes/
```

Dry run:

```bash
python3 patch_mousecape_cape.py "~/Library/Application Support/Mousecape/capes/YOUR_FILE.cape" --dry-run
```

Patch with automatic backup:

```bash
python3 patch_mousecape_cape.py "~/Library/Application Support/Mousecape/capes/YOUR_FILE.cape"
```

The script creates a timestamped backup next to the original file, for example:

```text
YOUR_FILE.cape.bak-20260624-185852
```

After patching:

1. Open Mousecape.
2. Select your cape.
3. Choose `Cape -> Apply Cape`, or double-click the cape if that is how your setup applies it.
4. If it does not take effect immediately, quit/reopen Mousecape or log out and back in.

## Optional: auto re-apply on login

Some systems lose the applied cursor after reboot/login. The `examples/` folder includes a LaunchAgent template that starts Mousecape shortly after login, lets it re-apply the last cape, then quits it.

This is intentionally provided as an example, not installed automatically.

## Safety and licensing notes

- Do not publish patched `.cape` files that contain Apple cursor image data unless you have the right to distribute those assets.
- This project only provides code and documentation.
- Mousecape is a separate project by its original author(s). This tool is not affiliated with Apple or the Mousecape project.

## Tested scenario

This was created after testing a local left-handed Mousecape cape on macOS 26 where adding `ArrowS` and `IBeamS` restored the left-handed arrow cursor behavior.
