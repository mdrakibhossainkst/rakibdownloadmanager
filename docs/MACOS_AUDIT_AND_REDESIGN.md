# Rakib Download Manager — macOS Audit & Redesign Plan

**Audit date:** 2026-11-12  
**Base branch:** `main`  
**Working branch:** `rakib/macos-audit-redesign`  
**Upstream:** [anefzaoui/misterdownloadmanager](https://github.com/anefzaoui/misterdownloadmanager)  
**Target test machine:** Intel MacBook Pro 2012, macOS Ventura 13.7.8, Intel HD Graphics 4000, 16 GB RAM.

## 1. Executive assessment

The repository already contains a substantial cross-platform Rust download manager and several macOS-specific integrations. The correct strategy is to preserve and harden the download engine, then build a distinct Rakib product identity and a Mac-focused experience around it. Replacing the engine or rewriting the whole application in SwiftUI at the outset would add risk without first proving a need.

The current application is an `egui/eframe` desktop app, not a native SwiftUI application. Its UI specification explicitly follows IDM 6.42's measured layout. This is a good functional baseline, but it does not yet represent the requested original Rakib visual identity.

**Important:** this is a source-code audit, not a successful runtime certification. The packaging and CI configuration have now been adjusted for Ventura, but GitHub Actions and real Intel Ventura runtime tests still need to pass before the Mac build can be called stable.

## 2. Existing macOS capability inventory

| Area | Source evidence | Audit status |
|---|---|---|
| Menu-bar/tray icon | `crates/app/src/tray.rs`; `tray-icon` is included for non-Linux targets and describes macOS as menu bar | Implemented in source; verify visibility, menu actions and relaunch behavior on Ventura |
| Keep running after closing the main window | App tray and close/minimize handling; progress windows can be hidden while downloads continue | Source support exists; test close, minimize, reopen, quit and active transfers |
| Launch at login | `crates/app/src/unix.rs` writes a LaunchAgent under `~/Library/LaunchAgents` | Implemented; test enable/disable, moved app path, login and uninstall cleanup |
| Browser native messaging | `crates/app/src/unix.rs`, native host and browser manifests | Implemented in source; test Chrome/Firefox/Chromium-family browsers on Ventura |
| Safari Web Extension | `tools/safari/build-appex.sh` and packaged `.appex` | Build target lowered to `macos13.0`; Safari 14+ web extensions are supported on macOS 11+, but the new Ventura build still needs CI and real Safari testing |
| Keychain | `crates/app/src/unix.rs` macOS keychain module uses Security framework generic-password operations | Implemented in source; test first-run prompts, locked keychain, read/write/delete and app identity changes |
| Independent download progress windows | `crates/app/src/progress.rs` | Implemented; test multi-window focus, close/hide, persistence and display scaling |
| Reveal downloaded file in Finder | `crates/app/src/unix.rs` | Implemented in source; runtime verification needed |
| System accent and appearance | `crates/app/src/native.rs` reads macOS accent; theme mode follows system light/dark | Partial native integration; test accent, appearance switching and contrast |
| Graphics renderer | `crates/app/src/renderer.rs` supports OpenGL and Metal; OpenGL is the default on macOS until real cards have clean reports | Metal is optional, not certified. Intel HD 4000 + OCLP must be tested with both renderers and fallback |
| Native macOS notifications | No verified Notification Center implementation established in this pass | Investigate separately; do not confuse the menu-bar tray with Notification Center alerts |
| Code signing/notarization | `tools/installer/build-macos.sh` defaults to ad-hoc signing; Developer ID and notarization are optional environment settings | Unsigned/ad-hoc distribution requires first-run trust steps; production release needs a signing/notarization strategy |

## 3. Compatibility risks for the target Mac

1. **Safari extension:** current build script targets `arm64-apple-macos14.0` / `x86_64-apple-macos14.0`. Ventura 13 cannot run this extension as currently built. Keep Chrome/Firefox integration available and decide whether a Ventura-compatible Safari extension target is technically possible.
2. **Graphics:** macOS builds support Metal, but the default is OpenGL because the project has not certified Metal on real Mac GPUs. Test OpenGL first, then Metal, and retain automatic fallback. OCLP does not guarantee that every graphics path will work.
3. **Build environment:** the upstream workspace currently declares Rust 1.98. The Rakib fork's root `Cargo.toml` declares Rust 1.95, while the user's installed local Rust was previously reported as 1.97.1. This metadata drift must be reconciled with the lockfile and current dependencies before promising a local build.
4. **CI confidence:** `.github/workflows/ci.yml` now treats macOS failures as real CI failures. `.github/workflows/release.yml` still labels Mac DMGs experimental until Intel and Apple Silicon runtime testing is completed.
5. **Distribution identity:** the app display name, DMG name/volume and Safari extension display/package name are now branded Rakib. The inherited bundle identifier, executable names, LaunchAgent label, browser native-messaging IDs, data directory and updater identity are intentionally unchanged for this first safe packaging pass. The installer still uses the upstream artwork until a Rakib icon asset is added.

## 4. Feature work to investigate and implement

### P0 — reliability and Mac compatibility
- Verify Intel x86_64 Ventura build, launch, renderer fallback and repeated launches.
- [x] Rebrand visible macOS installer and Safari extension labels without changing legacy runtime identifiers.
- [x] Set Safari extension deployment target to macOS 13.0 for Ventura compatibility.
- [x] Make macOS CI failures fail the workflow.
- [ ] Confirm the branch's GitHub Actions CI and full Intel DMG build.
- [ ] Replace inherited icon artwork with approved Rakib branding.
- Test segmented HTTP/HTTPS downloads, resume after quit/relaunch, pause/resume, retry, checksum, large files, disk-full and network interruption.
- Verify menu-bar icon lifecycle, close-to-background, reopen, explicit Quit and auto-start.
- Verify data/settings/history survive app updates and app moves.
- Validate browser host registration/unregistration and duplicate-install handling.
- Give the app a unique bundle identifier, data directory, LaunchAgent label and browser native-messaging identity.

### P1 — Mac-focused experience
- Design a new Rakib visual system: typography, spacing, surfaces, iconography, colors, elevation, motion and component states.
- Redesign Dashboard, Active, Queued, Completed, Failed, Categories, Queues, Scheduler, Browser Integration, Settings and About.
- Rework download rows, progress cards, context menus, toolbar, empty states, search, filters and bulk actions.
- Improve independent progress windows and menu-bar quick controls.
- Add clear macOS keyboard shortcuts, drag-and-drop, Finder reveal, file conflict handling and accessibility labels.
- Add Notification Center alerts for completion/failure only if a reliable native implementation is confirmed.

### P2 — advanced capabilities
- Download rules by file type/domain and per-browser capture preferences.
- Smart duplicate detection, download history search and restore.
- Per-download and global bandwidth controls, scheduling and queue profiles.
- Optional launch-at-login control using current macOS-supported mechanisms.
- Optional update channel and verified update/recovery flow.

## 5. UI/UX direction

The redesign should be a coherent product redesign, not a superficial theme swap.

- **Product name:** Rakib Download Manager.
- **Packaging milestone (2026-11-12):** app bundle display name, DMG filename/volume label and Safari extension name updated; Safari build target set to macOS 13.0; macOS CI made blocking. These are source changes only until CI and hardware tests pass.
- **Visual character:** premium, restrained, modern Mac desktop software; clear hierarchy and purposeful color.
- **Layout:** compact sidebar + content workspace + contextual inspector/details where useful.
- **Themes:** carefully tuned Light and Dark modes; no washed-out all-white surfaces. A new built-in **Rakib** palette now establishes the product's blue/slate visual direction and is the default for fresh installations; the original Classic theme remains available.
- **Interaction:** predictable macOS window behavior, keyboard navigation, native file dialogs and context menus where feasible.
- **Performance:** avoid heavy blur, excessive animation and expensive redraws; prioritize the Intel HD 4000 target.

Keep the Rust engine and current `egui` application architecture for the first redesign milestone. Evaluate a native SwiftUI/AppKit shell only after the engine, IPC boundary and UI requirements are documented; a full UI rewrite is a separate architectural decision.

## 6. Recommended delivery sequence

1. **Audit baseline:** inspect current platform code, packaging, app identity, renderer and workflow; record runtime test results.
2. **Identity separation:** replace inherited product metadata safely, preserve required GPL notices and upstream attribution.
3. **Mac reliability milestone:** fix only verified Ventura/Intel blockers and make the macOS CI job informative rather than silently non-blocking.
4. **Design system:** establish tokens, typography, icons, components and responsive layout rules.
5. **Screen redesign:** implement the complete application UI in coherent sections.
6. **Mac integrations:** improve menu bar, background lifecycle, notifications, browser integration and startup.
7. **Release engineering:** Intel DMG first, then Apple Silicon; validate app bundle, permissions, signing, checksums and update path.

## 7. Licensing and attribution

The upstream project is GPL-3.0-or-later. This repository also declares GPL-3.0-or-later. Keep the license and required notices, preserve third-party attribution, and publish corresponding source when distributing modified binaries. Rebranding does not remove upstream or dependency license obligations.
