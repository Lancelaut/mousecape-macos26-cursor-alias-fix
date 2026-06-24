I ran into the same macOS 26/Tahoe cursor replacement issue with an older left-handed `.cape`.

For that cape, the legacy keys existed:

- `com.apple.coregraphics.Arrow`
- `com.apple.coregraphics.IBeam`

but these compatibility keys were missing:

- `com.apple.coregraphics.ArrowS`
- `com.apple.coregraphics.IBeamS`

Duplicating the existing Arrow/IBeam cursor dictionaries to `ArrowS` and `IBeamS` restored the arrow and I-beam behavior for me.

I published a small local patch script here:

https://github.com/Lancelaut/mousecape-macos26-cursor-alias-fix

It does not redistribute any cursor artwork or patched `.cape` files. It only patches a cape already present on the user's Mac, creates a timestamped backup, and validates the result with `plutil`.
