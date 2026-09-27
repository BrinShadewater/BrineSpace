# BrineSpace asset pipeline and working workflow

## Matching portrait workflow — September 27, 2026

The seven accepted profile masters are installed in `character/portraits-brine-style-v1/`;
BRINE V14 remains the style reference. Follow the maintained
[portrait workflow](../skills/brinespace-character-pipeline/references/comms-portraits.md)
for identity/style references, prompt constraints, versioned masters and isolated
native verification. See [portrait session closeout](PORTRAIT_SESSION_CLOSEOUT_2026-09-27.md).

## September 27 asset selection and approval closeout

Start with [the latest closeout](ART_SESSION_CLOSEOUT_2026-09-27.md). The 323 existing Desktop clean exports are installed, including colored airlock suits and final furniture repairs; 43 cards and four-direction airlock captures were refreshed. The follow-up audit found the selected additional props, architecture and drone components already present. Robot rescue `occupied-3` is owner-approved. Human crew candidates remain unfinished and packages remain older snapshots.

Before repainting a reported mismatch, locate the owner's existing selected export, compare its ID/dimensions/hash and trace the actual runtime consumer. Review Candidates and source masters are not automatic replacement selections. Keep source, animation components, native visual evidence, owner acceptance and package identity separate. Both room and character skills now carry this procedure in `references/selected-art-audit.md`.

## September 26 room/animation closeout — current continuation

Read [the session handoff](ROOM_ART_SESSION_CLOSEOUT_2026-09-26.md). Native drone pilots, directional motion, runtime installation and matching frozen Windows/Mac packages are completed; the earlier “Next task” below is historical. New graphical enhancements remain a deferred backlog. Before a later pilot, inspect current consumers and effects, use a bounded representative room, and review at gameplay zoom with the locked references. Verify pause/power transitions and rendering cost where relevant. Preserve source selection, installation, agent visual review, owner acceptance and exact release evidence as separate states.

## Accepted drone handoff — September 26, 2026

The owner accepted v10 drone art and launch/recovery previews. Start with
[session closeout](DRONE_ART_SESSION_CLOSEOUT_2026-09-26.md) and the selected
`drone-animation-bases/approved-v10/` bundle in the Desktop export folder.
The bundle separates sources, 30 native components, previews, review, provenance
and tools. Original loose files remain as compatibility/history, not competing
current selections. The room and character skills now route through
`references/drone-animation.md` for shared lessons.

Next task: native room/NPC scale pilot, then articulated directional drone motion.
Do not regenerate accepted identities or mistake the launch study for a complete
NPC animation pack. No game files or owner layouts were installed/changed here.


## Current visual specification — September 26, 2026

Read [the art and theme bible](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md) before
production. It is the single current style specification, with fixed references
in [the reference lock](BRINESPACE_ART_REFERENCE_LOCK_2026-09-26.json).
The accepted clean exports remain a separate visual reference family, not an
installed replacement. Historical workflow notes and installed skill snapshots
must not override this newer visual direction.

Updated September 24, 2026. This is the maintained routing guide for asset work;
the detailed procedures remain in the two repository skills. Start with
[current status](CURRENT_STATUS.md) and [the Claude handoff](CLAUDE_HANDOFF_2026-09-24.md).

## Select the work, then the evidence

| Work | Maintained procedure | Evidence needed |
|---|---|---|
| Crew identity, motion, equipment, furniture contact | [Character skill](../skills/brinespace-character-pipeline/SKILL.md) | Selected source and rebuild, continuous native action/joins, real controller travel where relevant |
| Station props (v2), Studio, layouts, room cards | [Station props v2](STATION_PROPS_V2_2026-09-25.md) (`tools/room_props_v2/`); [Codex re-export brief](CODEX_BRIEF_MAGENTA_PROPS.md) | Catalog/`test_layout_keys`, owner layout backup, live/Studio views at four rotations, crew reachability |
| Bought props (pre-v2: BRINE Core, corridors, seabed scenery) | [Room skill](../skills/brinespace-room-pipeline/SKILL.md) and its tileset reference | Registry integrity, protected-key comparison, live/Studio views and relevant door approaches |
| Seabed, scenery, terrain, wrecks | [Environment contract](ENVIRONMENT_PRODUCTION_CONTRACT.md) | Source provenance, powered/surveyed native view, unchanged occupancy unless deliberately changed |
| Playable package | [Release workflow](RELEASE_WORKFLOW.md) | Frozen dependencies, exact PCK audit, actual release journey; native Mac evidence separately |
| Session closeout | [Claude handoff](CLAUDE_HANDOFF_2026-09-24.md) | Current decisions, local state, evidence limits, concrete unresolved work and saved task inventory |

Keep source generation, selected art, derived exports, runtime bindings, native
review, owner acceptance and packaged verification separate. None implies the next.
Do not run a full asset batch or export for documentation changes.

## Preserve the inputs before editing

The repository skills are authoritative over installed snapshots. Start from the
current bindings, not the newest filename or an old handoff's TODO. Inspect the
actual consumer and the source dimensions before choosing a repair.

Back up affected owner layout keys, recovery files and library marks before a
write. Record their before hashes and compare unrelated keys after the operation.
Owner layouts are in `%APPDATA%/Godot/app_userdata/BrineSpace/room_layouts.json`;
the repository's `rooms/full-wall-v1/default-layouts.json` is a separate input.
Preserve `favourites.json`, `retired.json`, `names.json` and `categories.json` in
`rooms/tileset-library/`. A dirty tracked file may be newer owner work. Closeout
does not require a commit and never authorizes resetting those files from Git.

The current layout protection rules live in CURRENT_STATUS and station props v2.
All 43 redesigned rooms were subsequently hand-adjusted by the owner; preserve
their saved Studio layouts. The older 27-room list and deliberately cleared
rotations describe pre-v2 history, not current authoring instructions.

## Bought-art path

*Since September 25 the bought tileset art dresses only BRINE Core, the corridor
pieces and seabed scenery; 240 unused sheets were moved to the owner's Desktop
(`rooms/tileset-library/retired-sheets.json`). Station rooms use station props v2.*

`vendor-art/` contains licensed original packs and is gitignored. Preserve it;
a clone will not recreate it. Converted sheets live under `assets/new-tilesets/`.
Tools under `tools/tileset_library/` handle conversion, scanning, registration,
merging, tone, titles, intake, sweep, refit, cutting, isolation, holes and variants.
Use only the stages required by a demonstrated defect, inspecting their help and
preview/dry-run behavior first. Do not rerun the entire chain on a mature library.

Stable IDs, aliases and removals preserve placed art. `pieces` use absolute sheet
coordinates; `region` is trimmed visual extent; `footprint` is floor occupancy.
Do not conflate them or reuse an old ID. Scene cutouts must not go through refit
that grows their bounds into neighboring art. Inspect cutouts against magenta.
Automatic key-hole repair is detection-only; source-supported manual choices win.

Typical verification after registry changes:

```powershell
python tools/tileset_library/register.py --validate
python tools/run_tests.py --only test_tileset_registry
```

Select native Studio cases from `tests/index.json` when layout interaction or
rendering changed. The September 20 library count is historical, not an invariant.
Studio-only exterior scenery filtering must preserve existing placed instances.

## Composition and presentation

Follow the [visual bible](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md). Compose believable
work areas with large/medium equipment, physical supports, useful operator space
and circulation derived from actual ports. Do not fill floor with accessories or
shrink equipment unnaturally to satisfy a geometry check. Visual overlap can form
an intentional assembly; distinguish it from clipping or an inaccessible station.

Review effective live props before adding furniture: an old functional host may
remain underneath. Studio shows some dressing/common decorations that live rooms
filter. Free placement is its default; `issues()` is intentionally quiet until
that toggle is off. Wall decorations remain paused by their production flag.
Do not change these decisions just to make an older test pass.

Inspect source pixels, actual gameplay scale and relevant production rotations.
Compare underwater scenery under powered, surveyed lighting before diagnosing
missing art. Fog-hidden diagnostic captures do not approve brighter exterior art.
Bake affected cards only after the final visual change; bind reviews to current
hashes. A later card change invalidates an earlier card-specific visual decision.

The owner's Graveyard Keeper reference is a pending direction discussion at this
handoff. A screenshot/reference request alone does not select a camera conversion.
Recover the session's unavailable detail before treating any proposal as accepted.

## Crew and animated machinery

Preserve exact source provenance and canonical builders. Rebuild into a separate
candidate location and compare before promotion. Missing originals are a blocker
to a reproducibility claim, not permission to generate replacements. Local
deterministic pixel repair is authorized; Higgsfield needs a fresh explicit request.

Judge whole sequences: approach, pickup, action, return, locomotion and interruption.
Pivots, matching endpoints and test counts cannot prove natural gait or identity.
Keep body regions connected; preserve equipment, near/far limb order, tool grip,
cargo and intentional hull occlusion. Verify the actual controller/renderer path:
standalone sprite playback missed Marsh pickup timing and exterior turn suppression.
Test pause, power loss, death precedence and disk restore for affected transitions.

## Tests, reports and checkpoints

Use `python tools/run_tests.py --list` and `tests/index.json` to choose the changed
subsystem; render-bound tests need the native lane on a real display. Read logs as
well as exit codes. Wait for observable startup and checkpoint restoration, not a
fixed number of frames. An unexplained failure merits a small state probe before
changing expectations. Isolate both profile files and loaded MetaState memory.

Preserve a frozen save and load a disposable copy. `RunSave.read` supplies `_path`;
Continue adopts it, and Conclude Expedition can delete the loaded file. Assert a
nonempty disk read and the expected seed, cycle, rooms, resources and crew so a
fresh loop cannot masquerade as successful restoration. Check visible framing
separately from state equality. Continue currently focuses BRINE intentionally.

Normal-play evidence retains paid costs, resource failure rules, dealt hands and
finite deposits. Label supplied fixtures and checkpoint chains explicitly. Exclude
intermediate conclusion awards from copied profiles. Automated paid play does not
establish human pacing, listening or continuous motion acceptance.

For performance, compare the same input, active phase, viewport and workload.
GPU readback capture is not a clean timing baseline; simulation CPU time excludes
rendering. Record tail spikes as well as means. Faster is not equivalent to smooth.
F7/F8 and the existing soak/report tools are the first diagnostic route.

## Release and closeout

For companion/container interactions, follow the maintained
[rescue workflow](../skills/brinespace-character-pipeline/references/companion-rescue.md).
Review closed, partial reveal, reboot, rollout and empty terminal states together.
Use existing body art behind explicit aperture masks, fixed chassis registration,
and the same saved clock/navigation exit as production. Apply encounter clearance
after saved layouts load; verify visual occlusion and navigation. Refresh preview
module, manifest and image revisions together before judging a repair.

Required side effects must stay outside assertions that release builds can remove.
Freeze code, configuration, runtime bindings and the dependency closure together.
Keep dynamic/JSON-relative/raw-PNG consumers. Audit an isolated package, then run
its executable: an editor pass or an asset inventory cannot prove release behavior.
Do not attribute newer source fixes to older packages.

At a milestone, update CURRENT_STATUS and a dated handoff, retaining superseded
evidence as history. Sync only changed maintained skill files to installed copies
after checking for divergent edits. Run structural skill validation and compare
the mirrors; this is not a behavioral trial. Record exact files, checks and open
acceptance. Archive a task only after its useful state is durable. Archiving means
session closure, not that every historical feature or review request is complete.
