# In-game workspace refinement

- Inspector content now follows explicit room/site/order/card selection. Crossing
  rooms or cards with the pointer changes hover visuals, not the selected content.
- Refreshing the same selection retains the inspector's scroll offset. Selecting
  a different object starts at the top. Inspector wheel events stop at that panel;
  the sidebar does not forward scrolling to the world.
- Construction access moved from the floating map panel to the sidebar, below
  Diagnostics. Journal / Construction still provides order details and links.
- Removed the floating operations panel and persistent event-log panel. Patterns,
  priorities and full event history remain in their Journal pages.
- Inspector header/image are smaller; body text is larger. Blueprint cards show
  larger names, primary output and purchase cost. Detailed input and known-link
  information remains in the selected inspector. Zoom and placement diagnostics
  are available under View & Placement Details; pause/speed/cycle remain visible.
- The textured seabed already covers the 40-by-40 valid gameplay grid. The blank
  outer area came from zooming the content below the viewport's dimensions. The
  minimum zoom now derives from the viewport, preventing that empty overscroll.
  Existing map coordinates, rooms, deposits and saves are preserved. Window resize
  updates the zoom limit and restores the camera's relative center.

Verification: tests/test_ui_workspace.gd checks clicked-room stability across
world/card hover, independent scroll handling, scroll retention, sidebar queue
placement, minimum zoom, and near/far camera boundaries. Native 1280x720 captures
are output/ui-workspace-1280.png and output/ui-workspace-map.png. Save/Continue
and native shared-menu regression results are recorded beside these captures.

## Pause menu nesting

The pause root now has five actions: Resume, Save, Settings, Station & Archives,
and End or Leave Loop. Station & Archives contains Codex, progression, recenter,
guide replay and debug-only admin view. End or Leave Loop contains save/title,
save/quit, restart and conclude/bank research. Each submenu has Back; Escape
returns to root first, restoring the opener's focus. Reopening starts at root.
The shared settings/archive Back flow retains its originating pause page.

Native workspace tests verify page visibility, five-action root, Back/Escape,
focus restoration, accessible conclusion, save feedback and pause preservation.
The complete native shared-menu regression passes, including settings changes,
save, title return and enlarged text. One boolean type annotation was repaired
in concurrently changed cryo room code to make this validation run load cleanly.

## Placement openings

Placement ghosts now configure all authored, rotated doorway apertures as open,
including sockets facing empty cells. Narrow corridor previews omit their end
caps. The lighter tint keeps wall gaps visible. Blue aperture brackets/arrows
mark available doors; cyan marks matching neighbors, amber crosses mismatches.
These markers appear on the placement ghost in normal view. Installed-room
animation and connection rules are unchanged. Preview door configuration checks
pass across 140 room/rotation cases; native four-rotation captures inspect wall
gaps and alignment. This is a rendering change, not permission to connect walls
that have no matching doors.

Placement indicators toggle with V by default (rebindable Placement guides action).
Settings / Accessibility exposes the same saved choice. The toggle hides aperture
markers and neighbor matching lines, preserving physical open wall sockets and
corridor ends. It is blocked while a modal menu is open and redraws immediately
while paused. Native preview tests verify hotkey, persistence, modal gating and
140 rotated aperture configurations, including an indicators-off capture.
