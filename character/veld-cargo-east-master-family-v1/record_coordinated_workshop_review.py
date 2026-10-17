from pathlib import Path
import json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'veld-workshop-coordinated-joins-v2-review'
s=json.loads((D/'summary.json').read_text());s['visualReview']={'reviewedPages':[f'staged-{gear}-{page}.png' for gear in ['bare','helmet'] for page in [1,2,3]],'sourceNativePairsReviewed':76,'fullNativeFramesReviewed':['staged-helmet-0032-native.png','staged-helmet-0400-native.png'],'all316CapturesReviewed':False,'observations':['Exact whole held East join precedes master half-turn.','Master turn shells/body stay compact through East-West and West-North.','New West gait matches master material/head more closely than prior selected source.','Turn ends into first gait pose abruptly; whole authored first-step/stop remains.','Older North unload crouch and final idle broaden body and alter detail/grade; whole North action repair remains.'],'scope':'Sampled source/native poses, not uninterrupted motion or natural lifecycle/Continue acceptance.'};(D/'summary.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
block='''## Veld coordinated workshop cargo review — October 2, 2026

Fixture-only Veld subclass holds travel through master East-West680ms and
West-North800ms turns. Exact canonical held East precedes first turn; real route
and original waypoint/speed/room contact retained. Staged East action/carry,
West master carry and original-master turn families override preview sources;
North unload/idle remain older selected sources. No normal controller/admission.

Actual main-scene/default powered workshop four comparisons both gears:5053checks,
0failures,2102ticks/316source-native captures/102.67s.189targeted frozen inputs
include main/shared CrewLife/actor/grid/player/manifests/frames; allunchanged.
Scratch APPDATA/all2931owner non-log files unchanged. Candidate displayed turns
41/48ticks travel0 vs baseline half-turn41ticks/30.659world-unit travel. Source-row
membership exact. Sixboards/76first-unique candidate source/native pairs plus2full
native helmet scenes inspected. Two89frame native snapshot comparison APNGs,
9983ms previewloops,178decoded RGBframes exact; these hold recorded pose clocks,
not uninterrupted native cadence. First failing interval2assertions retained:
arrival's last translation was incorrectly counted before the turn was displayed.
Corrected assertion checks consecutive actual displayed turn records; older
playback motion dictionary can remain stale during frame_at_elapsed actions.

Visual limits remain: North unload interiors/idle widen body/change grade and
detail; turn-to-open-gait first-step and arrival stop need authored whole motion.
Prototype arrival hold skips normal update: no interruption/needs/safety/Continue
or cargo ownership acceptance. Next whole master North action repair and genuine
first-step/stop, then guarded coordinated-controller lifecycle and remaining
South/cardinal/furniture/full-library consistency. Full goal active/incomplete.
Lesson: source identity alone cannot fix travel/turn coordination. Attribute
travel to displayed source intervals, not a controller flag first set at arrival
or stale playback metadata during independently clocked actions.
Handoff: character/veld-cargo-east-master-family-v1/WORKSHOP_JOIN_HANDOFF.md.

'''
refs=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for p in refs:
    st=p.stat();tmp=p.with_name(p.name+'.veld-coordinated.tmp')
    with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode());shutil.copyfileobj(src,dst,1024*1024)
    now=p.stat();assert (now.st_size,now.st_mtime_ns)==(st.st_size,st.st_mtime_ns),str(p)
    for attempt in range(5):
        try:os.replace(tmp,p);break
        except PermissionError:
            if attempt==4:raise
            time.sleep(.2)
(P/'WORKSHOP_JOIN_HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld coordinated cargo

## Objective and acceptance
Full master-matched Veld set, followed by cross-library polish. Full goal active.

## Accepted decisions and constraints
Original identity/anatomy/proportions/matte grade; preserve room geometry and
normal selections until visual/world lifecycle acceptance. Scratch APPDATA only.

## Current state
workshop_motion_preview.gd + UID is fixture-only Veld subclass. Holds real route
through master East-West and West-North turns, aliases exact held East before
first turn, delays unload until arrival turn completes. Original speed/waypoints.
New test_veld_workshop_coordinated_joins_v1.gd + UID, matching tools runner,
review_coordinated_workshop.py, build_workshop_motion_review.py and review folder.
Normal production actor/manifests unchanged. Arrival hold bypasses normal update;
it is authoring evidence, not a safe/restore-compatible runtime controller.

## Verification
Output coordinated-joins-v1 retains first2assertion failures with exact scripts;
v2:5053checks0failures,2102ticks316captures,189frozen inputs stable,2931owner files
unchanged,102.67s. Shared CrewLife/main included. Candidate turns41/48shown ticks
with0physical travel, baselinehalfturn30.659units. Sixboards76unique pairs and2
nativefull scenes inspected. Two89frame/9983ms APNG snapshot comparisons exact
decoded178frames; not uninterrupted motion or all316visual capture acceptance.

## Next action
Author whole master-matched North unload/pickup interiors to canonical North held
turn endpoint and original master idle, without body strips/per-pose fitting.
Inspect North old final idle versus true original master before endpoint choice.
Author real first-step/stop joins; do not force held legs into walking frames.
Then safely coordinate controller travel/arrival turns with service loss, safety,
medium, equipment, death and fresh Continue checkpoints before normal adoption.
South/cardinal remaining master actions, dormant furniture sources and full-library
consistency remain. Existing normal lifecycle and cargo ownership not certified
by this authoring-only subclass. Stale player.motion during finite actions is
not the displayed source; use actual row membership/clock for interval evidence.
''',encoding='utf-8')
print('Recorded coordinated preview, scoped native/visual evidence and five maintained references; full goal remains active.')
