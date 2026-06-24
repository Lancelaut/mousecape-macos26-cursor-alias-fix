# Mousecape macOS 26 Cursor Alias Fix

A small local migration tool for Mousecape `.cape` files affected by macOS 26 / Tahoe cursor replacement changes.

On macOS 26, some older Mousecape capes may appear to apply successfully, while the main arrow cursor, I-beam cursor, or related cursor families still fall back to the system default. A practical compatibility workaround is to add the newer cursor keys to the cape by duplicating the existing local cursor definitions.

This repository does **not** include, redistribute, or generate any Apple cursor artwork. It only patches a `.cape` file that you already have on your own Mac.

## Quick start

```bash
# 1. Clone this repository
git clone https://github.com/Lancelaut/mousecape-macos26-cursor-alias-fix.git
cd mousecape-macos26-cursor-alias-fix

# 2. Preview changes first
python3 patch_mousecape_cape.py "~/Library/Application Support/Mousecape/capes/YOUR_FILE.cape" --dry-run

# 3. Patch with automatic timestamped backup
python3 patch_mousecape_cape.py "~/Library/Application Support/Mousecape/capes/YOUR_FILE.cape"
```

Then open Mousecape and re-apply the cape:

1. Open Mousecape.
2. Select the patched cape.
3. Choose `Cape -> Apply Cape`, or double-click the cape if that is how your setup applies it.
4. If it does not take effect immediately, quit/reopen Mousecape or log out and back in.

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

This tool is a local cape migration helper. It is not a Mousecape fork and does not modify Mousecape itself.

## Finding your cape file

Common Mousecape cape location:

```bash
~/Library/Application\ Support/Mousecape/capes/
```

You can list local capes with:

```bash
find ~/Library/Application\ Support/Mousecape/capes -name '*.cape' -maxdepth 1
```

## Example output

```text
Cape: Left_Cursors
Identifier: com.alexzielenski.mousecape.dump
Cursor count before: 50
ADDED: com.apple.coregraphics.ArrowS from com.apple.coregraphics.Arrow
ADDED: com.apple.coregraphics.IBeamS from com.apple.coregraphics.IBeam
OK: com.apple.cursor.20 exists
OK: com.apple.cursor.26 exists
Backup: /path/to/YOUR_FILE.cape.bak-20260624-185852
Cursor count after: 52
Validation: /path/to/YOUR_FILE.cape: OK
```

## Recovery

By default, the script creates a timestamped backup next to the original file:

```text
YOUR_FILE.cape.bak-YYYYMMDD-HHMMSS
```

To revert manually, quit Mousecape and copy the backup over the patched file.

## Optional: auto re-apply on login

Some systems lose the applied cursor after reboot/login. The `examples/` folder includes a LaunchAgent template that starts Mousecape shortly after login, lets it re-apply the last cape, then quits it.

This is intentionally provided as an example, not installed automatically.

## Safety and licensing notes

- Do not publish patched `.cape` files that contain Apple cursor image data unless you have the right to distribute those assets.
- This project only provides code and documentation.
- Mousecape is a separate project by its original author(s).
- This project is not affiliated with Apple or the Mousecape project.

## Tested scenario

This was created after testing a local left-handed Mousecape cape on macOS 26 where adding `ArrowS` and `IBeamS` restored the left-handed arrow cursor behavior.

## License

MIT. See `LICENSE`.
