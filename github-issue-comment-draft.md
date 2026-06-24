I ran into this with an older left-handed `.cape` on macOS 26 as well. In my case, the cape contained the legacy keys:

- `com.apple.coregraphics.Arrow`
- `com.apple.coregraphics.IBeam`

but did not contain:

- `com.apple.coregraphics.ArrowS`
- `com.apple.coregraphics.IBeamS`

Duplicating the existing Arrow and IBeam cursor dictionaries to those `*S` compatibility keys restored the arrow/I-beam behavior for that cape.

I put together a small local patch script that does this without redistributing any cursor artwork or patched cape files:

<REPO URL HERE>

It only edits a cape file already present on the user's machine, creates a timestamped backup, and validates the result with `plutil` on macOS.
