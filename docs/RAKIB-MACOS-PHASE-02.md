# Rakib Download Manager — macOS Phase 02

## Implemented on this branch

- The main window title now reads **Rakib Download Manager**.
- The menu-bar item's primary action now reads **Open Rakib Download Manager**.
- The macOS app bundle display name, Finder app name, DMG volume name, and DMG filename use Rakib Download Manager.
- New macOS settings enable login launch by default. The LaunchAgent starts the app using the existing session-start argument, so the Dashboard stays hidden while the menu-bar app remains available.
- A saved opt-out is respected: disabling login launch in Options removes the LaunchAgent and the next manual launch does not silently re-enable it.
- The existing Dashboard layout, tray event loop, download engine, and independent per-download progress view are preserved.

## Existing behaviour reused rather than duplicated

The upstream app already provides:
- A macOS menu-bar icon and menu.
- Closing the Dashboard hides it to the menu bar when the tray is available and the setting is enabled.
- Downloads continue in the app process while the Dashboard is hidden.
- The menu contains a Downloads in progress submenu; selecting an entry opens that download's own progress window.
- The progress window is a separate egui viewport, not a panel embedded in the Dashboard.

## Deliberately not changed yet

- The original app artwork is still used by the macOS installer. A new Rakib icon must be added as a real high-resolution asset before changing the installer input path.
- The internal bundle identifier, LaunchAgent label, executable names, browser native-messaging identifiers, update identity, and data directory are unchanged. These are coupled; changing only the visible bundle identifier would risk duplicate startup entries, broken browser integration, lost access to existing download history/settings, or broken updates.
- No release DMG is claimed as built or tested yet.

## Validation status

- The source edits are committed to the feature branch and not to `main`.
- GitHub currently reports zero Actions workflow runs for this repository. Enable GitHub Actions in the repository settings to let the PR's CI execute.
- Even after CI passes, the actual menu-bar lifecycle and Intel GPU/window behaviour must be smoke-tested on the target Mac before calling the macOS build release-ready.
