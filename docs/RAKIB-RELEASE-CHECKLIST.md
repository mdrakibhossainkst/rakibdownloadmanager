# Rakib Download Manager — Release Readiness Checklist

This checklist distinguishes repository work from checks that require a real macOS installation or repository-level secret configuration.

## Implemented on the feature branch

- [x] Rakib app title, menu-bar primary action and Finder/DMG display names
- [x] Original SVG icon source, About/runtime icon and macOS ICNS generation
- [x] Rakib product-name mapping across app translations while retaining upstream browser-extension identity
- [x] Runtime-generated app/menu-bar icon
- [x] Help, issue-report and latest-release API links point to the Rakib repository
- [x] New macOS settings default to login launch; saved opt-out is respected
- [x] macOS agent bundle stays out of the Dock while keeping the menu-bar entry
- [x] Intel macOS CI matrix entry and manual workflow dispatch
- [x] Existing Dashboard, download engine and independent progress windows retained

## Required before a public release

- [ ] Enable GitHub Actions for this repository if GitHub has them disabled
- [ ] Enable the repository Issues feature so the in-app bug-report link can create reports in this fork
- [ ] Run CI and fix all blocking failures; record Intel macOS build/test result
- [ ] Run the Release workflow manually and inspect both DMG artifacts
- [ ] Test the Intel DMG on macOS Ventura: first launch, menu-bar visibility, dashboard open/close, active downloads, progress windows, pause/resume, history, restart/login launch, and clean uninstall/reinstall
- [ ] Verify the app bundle's custom icon, Gatekeeper behavior, and Safari/browser integration
- [ ] Configure a fork-owned OpenPGP release key: the public key is pinned in `crates/tools/keys/rakib-release.asc` (fingerprint `FB1E9144C6FC782CC6CE61DFE6852D874F11BDFB`); add the matching private key as the GitHub Actions secret `RAKIB_RELEASE_KEY`. The release workflow and CI fingerprint check now use this exact identity.
- [ ] Publish a signed release tag only after the signing key and artifacts are verified

## Security and compatibility notes

- Do not remove checksum-signature verification to make unsigned releases install. The app intentionally refuses an update list that is not signed by its trusted publisher key.
- Until the fork-owned key is configured, GitHub Releases can still carry manually downloadable DMGs, but the in-app self-updater will not trust unsigned release manifests.
- The existing bundle identifier and internal executable/helper names remain unchanged to preserve current app data, LaunchAgent and browser integration. A future identifier migration must include a tested migration path.
- macOS 13.7.8 is not available as a hosted GitHub runner image. CI is architecture/build coverage, not a substitute for the user's actual Ventura test.
