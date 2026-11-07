# Marsh bedside motion

The preserved built-in-generated source and prompt feed `tools/build_marsh_berth.py`.
No generation service is called during rebuild. The canonical Marsh rebuild invokes
this builder before deriving clearance. Runtime output is the supplemental
`character/marsh-v2/supplemental/berth-east` pack.

Scope: Marsh only, the unmirrored legacy bed/cabinet with an unobstructed bedside
notch. Other beds, bought bunks and other crew keep their existing clips. Direction
east describes the entry; the final body lies vertically with its head north.
Standing endpoint is exact canonical idle-east; rising reverses the authored poses
and timing. Transitions take 1.6 seconds with a seated hold before the leg swing.
The controller owns contact movement and caches local anchors for stable restores.

See `docs/MARSH_BERTH_CONTACT_2026-09-21.md` for native evidence and remaining work.
