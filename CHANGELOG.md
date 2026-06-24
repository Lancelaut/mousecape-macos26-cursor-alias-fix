# Changelog

## 0.1.0 - 2026-06-24

Initial public release.

- Add `patch_mousecape_cape.py`.
- Add compatibility aliases:
  - `com.apple.coregraphics.ArrowS` from `com.apple.coregraphics.Arrow`
  - `com.apple.coregraphics.IBeamS` from `com.apple.coregraphics.IBeam`
- Create timestamped backups by default.
- Validate patched cape files with `plutil` when available.
- Include a sample LaunchAgent for re-applying Mousecape after login.
- Document licensing/safety boundary: no cursor artwork or patched cape files are redistributed.
