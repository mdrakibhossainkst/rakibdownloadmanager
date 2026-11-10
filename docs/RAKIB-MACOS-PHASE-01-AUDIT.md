# Rakib Download Manager — macOS Phase 01 Audit

Date: 2026-11-10

## Repository baseline

- Repository: `mdrakibhossainkst/rakibdownloadmanager`
- Upstream: `anefzaoui/misterdownloadmanager`
- Default branch at audit: `main`
- Workspace version: `0.5.2`
- License: `GPL-3.0-or-later`
- Rust edition: `2024`
- Minimum Rust version declared by the workspace: `1.95`
- Desktop UI: `egui/eframe`
- Existing macOS tray dependency: `tray-icon`
- macOS graphics backend includes Metal; OpenGL remains the default renderer.

## Existing behaviour found in source

1. `crates/app/src/tray.rs` already creates a tray/menu-bar icon using `TrayIconBuilder`.
2. The tray left-click sends `TrayCmd::Show`; the menu exposes download actions, active downloads, Options and Exit.
3. `crates/app/src/main.rs` has a `Start::Session` path for login-started launches. It intends to start hidden and remain in the notification area when the tray icon is available.
4. `crates/app/src/app.rs` handles a close request by cancelling the close and hiding to tray when the tray is available and `settings.close_to_tray` is enabled. If no visible tray is detected on macOS, it falls back to minimizing rather than hiding an unreachable window.
5. The app's downloads run on a Tokio runtime; the UI reads snapshots. This is a useful separation, but it is not yet proof that all shutdown/termination paths preserve downloads.
6. Active downloads are represented in the tray menu and can reopen their progress window.

## Compatibility and build observations

- The project declares Rust 1.95 as its minimum; the build workflow uses the repository's stable toolchain file.
- The existing CI workflow labels macOS as experimental and uses `macos-latest`, which currently means Apple Silicon. That does not validate an Intel x86_64 build.
- For this Intel Mac target, add a dedicated x86_64 macOS CI job (for example, `macos-15-intel`) and explicitly test the minimum macOS deployment target before treating the build as compatible with Ventura 13.7.8.
- GitHub-hosted macOS runners are suitable for automated compile checks, but GUI lifecycle behaviour still needs a real Mac test.

## Design constraint

Preserve the existing MDM dashboard layout and interaction model. Customization should initially be limited to Rakib branding, app identity, icon, theme assets and carefully reviewed visual details. Do not replace the UI framework or redesign the main dashboard as part of the macOS lifecycle work.

## Phase 01 conclusion

The repository already contains a tray icon, close-to-tray handling, session-start handling and independent Tokio download execution. The next phase should be a targeted audit of settings defaults, startup registration, progress-window ownership, macOS app-bundle behaviour and process-exit paths. Avoid duplicating existing functionality until those paths are verified.

No application source code has been changed in this audit phase.
