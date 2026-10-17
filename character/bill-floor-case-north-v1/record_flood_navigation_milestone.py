from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'flood-navigation-evidence.json').read_text());assert e['validation']['passed']
note='''## Bill moving water treatment verified; land/water pose join open — October 2, 2026

Actual normal Bill actor navigates graph/collision-validated prescribed in-room
East/West path with normal medium/oxygen/safety/position/source updates at60Hz.
Two ten-second room-water rise/hold/drain histories/bare and helmet; native captured
every2ticks/30Hz. Both move320.3618world units and cross dry/water/dry.4561native
checks0fail/223.27s/engine0/cleanlog;2931owner non-log files unchanged/scratch APPDATA.
670native presentations/1340original source-room captures retained; six full-root
registered boundary/overview boards viewed. Candidate treatment maintains water
readability in sampled moving views. Normal renderer/selection/art unchanged.

Visual join remains FAILED: source abruptly changes upright walk to prone East swim
at water.55, then back to walk when draining. Same148standing ruler and actual pivot
registration prove this is a pose gap, not per-frame normalization. Current wet
start/stop transitions join tread/swim; they do not supply a land/water bridge.
Need authored matched transitions and collision/medium-aware dispatch, then replay
moving native joins. No natural full evacuation/hydrology/full cardinal motion,
continuous playback visual acceptance, original-master/full-library acceptance here.

Four advancing native/source APNGs preserve all300captured intervals each and exact
ten-second timelines; decoded pixels checked against all inputs including merged
identical frames. Source panes use post-run normal-loaded exact RGBA hash/pivot/H148
metadata at common physical root, no source scaling or paint. Headless metadata
inspection1664loaded slots/14.74s is inventory, not1664assertion checks despite old
log wording. Initial source boards/animation panes used varying canvas origins and
clipped tall walking poses; corrected with original metadata, not body resizing.

First unload-anchor trial FAILED movement requirement/132.19s: observed actual
blocked swim escape, then only16units of movement while draining.337native pairs,
fixture/log/report retained in output/bill-floor-case-flood-route-v1/
first-stationary-interval. Separate headless controller probe/49.9s records exact
blocked path/no swim clearance; no fallback teleport, geometry or gameplay fix.
That probe report corrected to explicitly record no native screenshot. Separate
moving fixture seeds only initial valid route; it does not resolve blocked escape.
First moving fixture/49.06s SCRIPT ERROR called staged observe_finish on normal
actor; failed fixture/log/report retained. Optional staged hook now guarded;
normal actor/navigation/source behavior unmodified. Every owner profile unchanged.

Lesson: isolate material consistency, source pose joins and actual navigation. Do
not weaken displacement checks or call a blocked dispatch successful evacuation.
Register mixed source canvases by original texture metadata before diagnosing size
changes; preserve integer capture timelines without cumulative APNG rounding drift.
Next matched land/water pose bridge and native joins, normal water material admission,
outside-room fallback, cargo lifecycle/older-bank Continue and full Bill master/
cross-family polish. Goal active/incomplete. No commit/export. Review:
character/bill-floor-case-north-v1/flood-navigation-review.html.

'''
for filename in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 f=R/filename;s=f.read_text(encoding='utf-8')
 if note.splitlines()[0] not in s:f.write_text(note+s,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 s=f.read_text(encoding='utf-8')
 if note.splitlines()[0] not in s:f.write_text(s+'\n'+note,encoding='utf-8')
(P/'FLOOD_NAVIGATION_HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill live water joins

## Objective and acceptance
Complete full Bill set matching master identity/style/perspective/stature/proportions/
matte grade, then whole-library consistency and motion polish. Active/incomplete.

## Accepted decisions and constraints
Keep original source/registration, world collision/oxygen/safety and owner profile.
Material readability can improve independently; a sharp land/water pose change is
still unaccepted. Preserve blocked escape evidence rather than teleport or weaken checks.

## Current state
Moving normal-actor navigation fixture/runner and source-registration inventory;
rebuildable native30Hz/root-registered source review, original captures and APNGs.
Candidate water treatment unselected; no production art/controller/renderer edits.
Pipeline/bible/both skill references updated with navigation/registration lessons.

## Verification
4561native checks0fail/223.27s;two10s histories/both gear states move320.3618units.
670native presentations/1340original files; six source/native boards viewed.
Four APNGs decode all300inputs each and preserve exact10seconds.1664slot metadata
inspection supports post-run exact source registration; not1664assertion checks.
Every interval2931owner files unchanged/scratch. Two failed fixtures retained.

## Next action
Authored matched upright/prone land-water transitions and collision/medium-aware
dispatch, then actual moving joins. Guarded normal material selection; blocked
unload-position escape/outside fallback, held-case priorities/shared-room lifetime,
older-bank Continue, cargo idle join and full Bill master/library polish remain.
''',encoding='utf-8')
e['visualReview']={'sixBoardsViewed':True,'material':'Readable moving sampled sources, existing geometry/detail preserved.','join':'FAILED upright/prone medium boundary; matched source bridge required.','continuousPlaybackVisualAcceptance':False,'APNGDecode':'All300 intervals per timeline decode identically; exact10000ms.', 'normalProductionSelected':False}
(P/'flood-navigation-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('Moving evidence, failed pose-join scope and pipeline/bible/skill lessons recorded.')
