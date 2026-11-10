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
7. `crates/app/src/settings.rs` documents both `minimize_to_tray` and `close_to_tray` as enabled by default. The Rakib branch now defaults login launch on for new macOS settings and preserves an explicit saved opt-out.
8. The existing app already has a theme setting and theme-file support. Preserve the current dashboard structure; use theme assets and app identity for initial visual customization.

## macOS app bundle findings

- `tools/installer/build-macos.sh` already builds both `aarch64-apple-darwin` and `x86_64-apple-darwin` release binaries and packages separate DMGs.
- The generated app bundle now displays “Rakib Download Manager” and uses a generated Rakib icon. It intentionally retains bundle ID `io.github.anefzaoui.misterdownloadmanager` for compatibility with existing LaunchAgent, data, browser integration and updater paths; a full identity migration is a separate breaking change.
- The bundle declares `LSMinimumSystemVersion` as `11.0`, so Ventura 13.7.8 is above the declared minimum. This is not by itself proof that all dependencies or runtime behaviour work on Ventura.

## Compatibility and CI observations

- The project declares Rust 1.95 as its minimum; the build workflow uses the repository's stable toolchain file.
- The existing CI workflow labels macOS as experimental and uses `macos-latest`, an Apple Silicon runner. That does not validate an Intel x86_64 build.
- GitHub's current standard Intel macOS runner label is `macos-15-intel`; add a dedicated x86_64 compile/package check using that runner. Public repositories can use standard GitHub-hosted runners without charge, subject to GitHub's current runner policy.
- GitHub has retired the macOS 13 hosted image. A GitHub-hosted runner therefore cannot exactly reproduce Ventura 13.7.8. Use CI for Intel architecture/build checks and the user's actual Ventura Mac for final compatibility testing.
- GUI lifecycle behaviour still needs a real Mac test; a successful CI compile does not prove that closing the dashboard leaves the process and active downloads alive.

## Design constraint

Preserve the existing MDM dashboard layout and interaction model. Customization should initially be limited to Rakib branding, app identity, icon, theme assets and carefully reviewed visual details. Do not replace the UI framework or redesign the main dashboard as part of the macOS lifecycle work.

## Phase 01 conclusion

The repository already contains a tray icon, close-to-tray handling, session-start handling, independent Tokio download execution, default-on close/minimize-to-tray settings, and Intel macOS packaging. The next phase should verify startup registration, progress-window ownership, actual macOS process lifecycle and identity migration. Avoid duplicating existing functionality until those paths are tested.

This audit is historical baseline documentation. Implementation and follow-up decisions are recorded in `RAKIB-MACOS-PHASE-02.md` and `RAKIB-RELEASE-CHECKLIST.md`.
