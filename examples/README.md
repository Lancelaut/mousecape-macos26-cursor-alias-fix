# Examples

## `com.example.mousecape.autoreapply.plist`

A sample macOS LaunchAgent that starts Mousecape shortly after login, waits a few seconds for Mousecape to re-apply the last selected cape, then quits Mousecape.

This is useful on systems where the cursor resets after reboot/login.

Install manually only if you understand what it does:

```bash
cp examples/com.example.mousecape.autoreapply.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.example.mousecape.autoreapply.plist
launchctl enable gui/$(id -u)/com.example.mousecape.autoreapply
```

Uninstall:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.example.mousecape.autoreapply.plist
rm ~/Library/LaunchAgents/com.example.mousecape.autoreapply.plist
```

You may want to change the label from `com.example.mousecape.autoreapply` to your own reverse-DNS identifier.
