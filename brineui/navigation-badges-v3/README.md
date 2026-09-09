# Clean navigation badges v3

Updated: 2026-09-08. Five badge icon refinements generated with the built-in image tool. Exact edit prompts retained in prompts.json.

## Objective and direction
Cleaner icons with broad smooth enamel surfaces and crisp silhouettes. Remove heavy scratches and chipped texture. Preserve the cream Codex computer, ochre Archive, jade Diagnostics, orange Journal and multicolor Menu against dark teal metal badges.

## Deliverables and verification
codex.png, archive.png, diagnostics.png, journal.png and menu.png. All five visually reviewed: substantially reduced distressing and clear icon shapes. File properties are in validation.json. Earlier versions preserved. Integrated through scripts/navigation_badge.gd.

## Remaining work

Runtime integration now uses scripts/navigation_badge.gd with per-asset octagonal UV clipping; the baked exterior is excluded during UI drawing. See docs/NAVIGATION_BADGES_2026-09-08.md. Source PNGs remain RGB; standalone alpha exports are still pending.
Owner visual review remains pending. These RGB sources are usable through the verified runtime clipping helper; background extraction remains necessary for standalone transparent exports.
