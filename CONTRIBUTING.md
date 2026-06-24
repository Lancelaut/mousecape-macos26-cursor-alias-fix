# Contributing

Thanks for considering a contribution.

## Useful reports

Please include:

- macOS version
- Mousecape version or fork
- Whether the cape is a dump cape or a custom cape
- Output from `--dry-run`
- Which cursor families still fail after patching

Please do **not** upload `.cape` files that contain Apple cursor artwork or other assets you do not have permission to redistribute.

## Development checks

```bash
python3 -m py_compile patch_mousecape_cape.py
python3 patch_mousecape_cape.py --help
plutil -lint examples/com.example.mousecape.autoreapply.plist
```

If you have a local test cape, test against a copy, not the original.
