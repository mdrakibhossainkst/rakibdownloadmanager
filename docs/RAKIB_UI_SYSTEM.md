# Rakib Download Manager — UI System

**Status:** design specification for the next UI implementation milestone  
**Reference target:** 1280 × 800 desktop window, including the Intel MacBook Pro 2012's 1280 × 800 internal display  
**Implementation:** keep the existing Rust + egui engine and behavior; replace presentation incrementally

## Product direction

Rakib should feel like a focused, premium macOS utility: quiet surfaces, confident blue accents, compact information density, clear status, and restrained motion. It must not look like a recoloured copy of IDM. The current download engine, queue logic, browser capture, progress windows and tray lifecycle are functional foundations to preserve while the interface is replaced.

## Design tokens

The built-in `Rakib` theme is the source of truth for semantic colours.

| Token | Light | Dark | Use |
|---|---|---|---|
| Window | `#f3f6fc` | `#0e1726` | Main workspace background |
| Surface | `#ffffff` | `#152238` | Cards, sidebar, inspector |
| Header | `#eaf0f9` | `#1c2d47` | Toolbars and section headers |
| Text | `#172b4d` | `#eaf2ff` | Primary text |
| Accent | `#246bfd` | `#6ba6ff` | Primary action, selected state, links |
| Selection | `#dce9ff` | `#24446d` | Selected rows and controls |
| Error | `#b42318` | `#ff8c82` | Failed state and destructive feedback |
| Warning | `#8a4b08` | `#f3c66a` | Waiting, retry and caution |
| Success | `#176b45` | `#72d6a3` | Completed and healthy state |

- Spacing scale: 4, 8, 12, 16, 20, 24 and 32 pt.
- Standard control radius: 8 pt; compact controls: 5–6 pt; cards: 10–12 pt.
- Main content padding: 20 pt; sidebar padding: 12–16 pt.
- Use semantic colours, never hard-code a light-only colour into a component.
- Text and icon contrast must remain readable in both themes; focus indicators must be visible without relying on colour alone.

## Main window layout

The redesign uses three clear zones, with the inspector optional:

1. **Navigation sidebar — 224–248 pt**
   - Brand mark and app name at the top.
   - Primary destinations: All Downloads, Active, Queued, Completed, Failed.
   - Smart categories by file type: Documents, Images, Video, Audio, Archives, Other.
   - Queue list and Scheduler shortcut.
   - Bottom utilities: Browser Integration, Settings, About.
   - Counts are quiet metadata, not oversized badges.

2. **Workspace — flexible**
   - Header with current destination title, item count and one clear primary action.
   - Search field and compact filters (status, category, date, source).
   - Download rows with filename, source/domain, progress, downloaded/total size, speed, ETA and status.
   - Row selection exposes contextual actions; avoid permanently showing every action.
   - Empty, loading, paused, retrying and failed states receive purposeful layouts.

3. **Inspector — optional 280–320 pt**
   - Opens when one download is selected; otherwise hidden.
   - Preview/file icon, filename, URL, save location, size, checksum, connection/segment details and timestamps.
   - Quick actions: Open, Reveal in Finder, Copy URL, Retry, Pause/Resume, Remove.
   - Must collapse cleanly on narrow windows and the 1280 × 800 target display.

## Core component behavior

- **Download row:** one-line filename with ellipsis; secondary domain and metadata; a thin progress track; clear status text. Completed rows should not compete visually with active work.
- **Progress track:** show percentage and transferred size; use motion only while actively downloading. Respect reduced-motion preferences.
- **Primary action:** one strong accent button per context. Destructive actions are visually separated and require confirmation only when data could be lost.
- **Toolbar:** Add URL is primary; batch/torrent actions live in a compact secondary menu. Pause/Resume and Remove are contextual.
- **Context menu:** actions follow the selected item state. Keep keyboard shortcuts visible where supported.
- **Progress window:** compact, independent, always reflects the same download model as the dashboard; closing the window must not stop the download.
- **Menu-bar quick view:** show active count and aggregate speed; provide Show Dashboard, Add URL, Pause All/Resume All and Quit.

## macOS behavior

- Main-window close hides the dashboard when active downloads exist; explicit Quit remains available.
- Download processing, queue timers and saving continue independently of the dashboard window.
- Use native file/folder pickers and Finder reveal where available.
- Support Command-based shortcuts, standard text-field behavior, drag-and-drop and accessible labels.
- Avoid heavy blur, large shadows, continuous animation and unnecessary GPU effects; the target includes Intel HD Graphics 4000 with OCLP.
- Light/Dark mode must be tested on Ventura; never allow a mode switch to produce all-white or all-black surfaces.

## Implementation order

1. Apply and verify the semantic Rakib palette (done in the current branch).
2. Extract reusable sidebar, header, search/filter, download-row and inspector components without changing download behavior.
3. Implement the new dashboard behind the Rakib theme/layout selection while retaining Classic as a fallback.
4. Port selection, sorting, filtering, keyboard navigation, drag-and-drop and context actions.
5. Redesign the independent progress window and menu-bar quick view.
6. Run regression tests for download lifecycle, queues, browser capture, persistence, accessibility and Intel rendering.

## Acceptance criteria

- No inherited IDM-style main layout remains in the Rakib experience after the dashboard milestone.
- Every existing download action remains reachable and works.
- Light and Dark modes have consistent semantic surfaces and accessible contrast.
- At 1280 × 800, the sidebar, workspace and optional inspector do not force horizontal scrolling.
- Closing the dashboard never interrupts active downloads.
- The app remains responsive on the Intel HD 4000 target without relying on blur or continuous animation.
