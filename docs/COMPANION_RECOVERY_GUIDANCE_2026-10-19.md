# Companion recovery guidance — October 19, 2026

Owner approved a visible recovery checklist and next connected surveyed target links in the inspector and Journal, while retaining the8-Metal cost. Implemented locally; no release export or publication.

## What changed

The companion inspector now keeps a four-step checklist outside the room-details disclosure: connect a matching door; pay8 Metal and repair; open the shipping crate/trash container or start the pet-pod thaw; then supply8 powered seconds. DONE/NOW/LATER and live percentages show progress. Context explains the exact Metal shortfall, retained payment, worker travel/welding, busy rig, station door/Power blocks, room suspension, next operating cycle and a blocked emergence spot. Margot uses thaw language. Recovery remains temporary unless bought in Meta Progression; owned companions retain their future-selection wording.

After recovery, **Next connected recovery** links to another surveyed, unrecovered companion site with a matching door. Existing opened/paid work is preferred before another expense; ties are deterministic. The label says door connected, rather than promising an unobstructed crew route. No unknown map cells, recipes or discoveries are revealed. When none qualifies, the interface says to extend connected rooms and survey lights.

The Journal's actual visible Crew cards show the next target and current step/blocker, with real Inspect buttons. Surveyed companion rows also provide an Inspect action. The hidden text mirror stays consistent for search/accessibility. Clicking a link can focus an unbuilt surveyed recovery site and closes the Journal through its normal flow; unsurveyed/stale links do not reveal a site. Normal installed-room navigation remains in place.

An existing inspector filter hid the operation row for unbuilt recovery sites. It now permits surveyed companion sites, so **REPAIR & CONNECT //8 METAL** is actually visible before the found room is installed. Other unbuilt wreck controls were not broadened.

## Implementation

- `scripts/companions.gd`: read-only guidance and surveyed/connected target projections.
- `scripts/companion_recovery_panel.gd` and paired UID: scene-owned visible checklist and next-target link.
- `scripts/main.gd`: panel refresh, narrow operation-row visibility, guarded recovery navigation and Journal text mirror.
- `scripts/journal_widgets.gd`: actual visible next-target card and known-site Inspect actions.
- Two paired-UID tests and `tests/index.json`: headless logic and explicit native presentation lane.

Original companion payment, room connection, boot status/advance, snapshot, validation and restore method bodies compare equal to the before files. Cost8 Metal,18s crew welding,8 powered seconds, room economies, discovery rules, saves, art and accepted visual filters remain unchanged. There are no new checkpoint fields or permanent unlock grants. Guidance performs no crew route search or gameplay action.

## Verification

**Five focused headless tests pass:** new guidance (25 checks), existing companions/recovery, physical ward repair, inspector refresh and Journal crew roster. The final native fixture passes **28 checks** at1600×900 and1280×720, covering actual action visibility, one eight-Metal payment, repair/open/Power/restart/recovered states, next-target navigation, unknown-site rejection, real Journal buttons, blueprint-preview reset, partial repair restore, disk Continue and earlier-checkpoint rollback. Render refresh leaves resources/wrecks/RNG unchanged. Unit tests cover busy rig versus shortfall priority, suspension, retained progress, emergence clearance, owned/unowned future availability, Margot language and target filtering.

Ten native captures are retained; normal/compact checklist and Journal screens were visually reviewed. The action/current-step/next-target content stays visible; long room details and lower roster use the existing scroll areas. Tests supplied connector rooms and explicitly used clock-driven welding to isolate reward/UI states; these are **not** normal-cost opening pacing or physical-crew-route acceptance. The separate earlier paid background opening report remains the pacing evidence. No new FPS/memory, endurance, human-fun or Apple/release acceptance.

Initial attempts are retained. The first unit harness needed dynamic script introspection before it could fail on missing guidance. A native setup placed fixture rooms before surveying and obscured the Core lamps; surveying the open Core first corrected that setup. With corrected visibility, the native test isolated the hidden repair action in normal/compact views, then passed after the narrow filter fix. Visual review caught the Journal's visible-widget layer diverging from its text mirror; a failing real-control test preceded its fix. The initial source-method comparison included a neighboring new comment; method-body-only extraction confirms unchanged mechanics. Final gameplay/UI processes have no script/engine errors; the native fixture retains shutdown warnings for1 CanvasItem RID and2 ObjectDB instances, so no leak-clearance claim is made.

All Godot runs used guarded scratch APPDATA. All2,971 real player files,49 other protected source/art/test inputs and signed ZIP size/mtime match their before receipts. Earlier local work was retained through file snapshots and a task-only patch. No real-player save reset/restoration, test-profile copying into player data, art generation/import batch, build, signing, upload, Git commit/push/integration or cleanup.

## Next

Owner can review the retained native screens or try the source build. Keep8 Metal pending real first-time-player feedback on whether the steps/next target are now legible. A saving policy without discretionary rerolls remains a separate pacing experiment. River/Margot route breadth and fire-heavy openings are not covered by this interface pass.

Evidence: `output/companion-recovery-guidance-20261019/` contains original-file snapshots, task patch, RED/GREEN logs, native captures/results, regression console paths, mechanics comparison, visual review, preservation receipt, `FINAL.json` and handoff.
