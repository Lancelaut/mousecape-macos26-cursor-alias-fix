# FAQ

## Does this replace Mousecape?

No. This is only a local migration helper for existing Mousecape `.cape` files. You still need Mousecape to apply the cape.

## Does this include Apple cursor files?

No. The repository intentionally does not include any cursor artwork, patched `.cape` files, or Apple assets.

The script only edits a cape file already present on your own Mac.

## What problem does it try to fix?

On macOS 26 / Tahoe, some older Mousecape capes may be marked as applied, while the arrow cursor or I-beam cursor still falls back to the system default.

In tested cases, adding these compatibility aliases helped:

- `com.apple.coregraphics.ArrowS` copied from `com.apple.coregraphics.Arrow`
- `com.apple.coregraphics.IBeamS` copied from `com.apple.coregraphics.IBeam`

## Is this guaranteed to fix every cape?

No. It is a best-effort compatibility patch for one known class of cape files. Different capes may use different cursor keys, and macOS cursor internals can change again.

Always run `--dry-run` first and keep the automatic backup.

## Will it overwrite my cape?

Yes, when not using `--dry-run`, it writes the patched cape back to the same path. By default it first creates a timestamped backup next to the original file:

```text
YOUR_FILE.cape.bak-YYYYMMDD-HHMMSS
```

## How do I restore the backup?

Quit Mousecape, then copy the backup over the patched cape file. For example:

```bash
cp "YOUR_FILE.cape.bak-YYYYMMDD-HHMMSS" "YOUR_FILE.cape"
```

Then reopen Mousecape and apply the restored cape.

## Why not create `com.apple.cursor.20` or `com.apple.cursor.26` automatically?

Those keys may refer to different cursor families depending on the cape and macOS version. The script reports whether they exist but does not synthesize them by default.

## Can I use this for left-handed cursors?

Yes, if your left-handed cape already has a working `com.apple.coregraphics.Arrow` definition but macOS 26 is ignoring the arrow after applying it. The tested case was a left-handed cape where adding `ArrowS` restored the right-upward arrow cursor.

## Can this run on non-macOS systems?

The Python plist editing logic is cross-platform, but `plutil` validation is macOS-specific. On non-macOS systems, the script will skip `plutil` validation if `plutil` is not available.
