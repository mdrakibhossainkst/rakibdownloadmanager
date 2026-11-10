# Rakib Download Manager: browser integration

[← Back to docs index](README.md)

Install the Rakib browser extension to send supported browser downloads to Rakib Download Manager. The extension has its own Rakib branding, Chromium ID and Firefox add-on ID. It is not published in the Chrome Web Store or Mozilla Add-ons yet, so use the manually installed package described below. Do not install the upstream Mister Download Manager extension for this fork.

## 1. Install and open the desktop app

Install Rakib Download Manager, launch it once, and leave it running for the first connection test.

- Windows: use the installer with **Set up browser integration** enabled.
- macOS and Linux: launch the app once; it registers its native messaging host for supported browsers.
- If you built from source, build the browser packages with `./tools/extension/pack.ps1` (PowerShell 7) after installing the Python Pillow dependency. The output is in `target/extension/`.

## 2. Get the Rakib extension package

From GitHub, open the [CI workflow](https://github.com/mdrakibhossainkst/rakibdownloadmanager/actions/workflows/ci.yml), choose the latest successful run for the `rakib/phase-01-macos-audit` branch, and download the **rakib-browser-extensions** artifact. Extract it.

The artifact contains:
- `RakibDownloadManager-<version>-extension-chromium.zip` — Chrome, Edge, Brave, Opera and Vivaldi.
- `RakibDownloadManager-<version>-extension-firefox.xpi` — Firefox-compatible package (unsigned; temporary installation only).
- `RakibDownloadManager-<version>-chrome-web-store.zip` — store-upload package reserved for a future Rakib listing; it is not an installable store release.

## 3. Install in Chrome, Edge, Brave, Opera or Vivaldi

1. Extract the Chromium ZIP to a permanent folder. Do not move or delete that folder after installation.
2. Open the browser's extensions page: `chrome://extensions`, `edge://extensions`, `brave://extensions`, `opera://extensions` or `vivaldi://extensions`.
3. Turn on **Developer mode**.
4. Click **Load unpacked** and select the extracted `chromium` folder.
5. Confirm that **Rakib Download Manager** appears and is enabled.
6. Open the extension popup; it should report that the desktop app is connected.

To update the extension, download and extract the newer package to a permanent folder, remove the old unpacked extension, then load the new folder. Store-based automatic updates will be available after a Rakib listing is published.

## 4. Install in Firefox

Firefox requires a signed add-on for permanent installation. Until the Rakib add-on is listed and signed by Mozilla, use temporary installation for testing:

1. Extract the Firefox package.
2. Open `about:debugging#/runtime/this-firefox`.
3. Click **Load Temporary Add-on…**.
4. Select `manifest.json` inside the extracted `firefox` folder.
5. Confirm the add-on is enabled, then test a supported download.

Firefox removes temporary add-ons when the browser closes. A permanent signed Rakib Firefox release is a separate publishing step and is not claimed to be available yet.

## 5. Test the connection

1. Keep Rakib Download Manager open.
2. Open the extension popup and check the connection indicator.
3. Visit a direct downloadable file link (for example, a ZIP file) and click it.
4. The desktop app should receive the download and open its Download File Info window. Choose **Start Download**.

If the browser downloads the file itself, first confirm the extension is enabled and the desktop app was launched once. Then see [browser troubleshooting](browser-help.md) and [browser integration details](browser-integration.md).

## 6. Control what the extension captures

- **File types:** configure **Options → File types** in the desktop app.
- **Excluded sites:** add a site under **Options → File types** to leave its downloads in the browser.
- **Per-browser capture:** use **Options → General → Capture downloads from the following browsers**.
- **One-off download:** right-click a link and choose **Download with Rakib Download Manager**.

![Options, File types: the file types Rakib Download Manager takes from the browser, and the sites it leaves alone](images/help/catch-file-types.webp)
*1 the file types Rakib Download Manager takes, 2 the sites it leaves to the browser.*

Downloads the app does not capture remain with the browser.

## Next steps

- [Browser integration details](browser-integration.md)
- [Troubleshooting when the browser does not hand downloads over](browser-help.md)
