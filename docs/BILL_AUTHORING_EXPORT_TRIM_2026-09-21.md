# Bill authoring export selection

Updated September21,2026. Brine Space. Broad goal remains active.

## Objective and acceptance
Keep unused animation authoring sources out of playable exports while preserving
all runtime dependencies, including paths discovered dynamically.

## Decisions and constraints
No art/source deletion, runtime loader redesign, export, publication or owner-room
change. Do not exclude every sources/ directory: other actors use such files.

## Implementation
build_release_manifest.py now omits character/major-bill-v3/sources/ only when
adding files through broad dynamic or formatted-directory discovery. Exact and
formatted-file dependencies still win, including transitive JSON-relative paths.
The entire Bill revision root is scanned because CrewSpritePlayer.REVISION_ROOTS
is used for catalog, clearance and locker lookup. That conservative scan was also
selecting authoring metadata and generation sheets that those consumers do not use.
The omitted subtree remains intact for canonical rebuilds.

## Verification
Evidence: output/bill-remaining-endpoints-2026-09-21/.
- Read-only real collection before/after: exactly42files omitted,11819874bytes;
  no additions and no change outside the specific Bill authoring subtree.
-25other character files under sources/ remain selected. Their actual or conservative
  dependencies are retained; this is not a general sources-folder policy.
- Independent traversal of live Bill catalogs finds all2214frame references in
  selected assets; clearance and runtime modular geometry tool remain included.
- All7release manifest tests pass. New fixture covers broad root scanning,
  omitted authoring JSON not pulling in unrelated images, and explicit/formatted/
  transitive dependencies within the otherwise omitted subtree.
- Export plugin inspection confirms PNG/JSON files absent from its manifest are
  skipped. No new PCK was produced: these are dependency-selection results, not
  measured final archive size or packaged gameplay acceptance.

## Visual checkpoint
The current registered four-direction board includes the newly integrated south
art. East/south standing endpoints match; north is visually close; west remains
lighter. Agent static review did not select another full-set replacement. This
is not full-motion or owner acceptance. Board: all-directions.png.

## Next action
At the next release milestone, run the maintained exporter, exact PCK audit and
actual release gameplay checks. Verify the42omitted sources stay absent while
runtime assets match. Existing2601720e53d908cc exports remain the earlier checkpoint,
predating this selection policy, south art update and departure controller fix.
Continue paid movement/action review and room/performance work within the broad goal.
