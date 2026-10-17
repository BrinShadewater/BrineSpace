from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-land-water-runtime-east-v1'
v=json.loads((O/'validation.json').read_text());data=json.loads((O/'records.json').read_text());assert v['passed'] and data['failures']==0
e=json.loads((P/'review.json').read_text());e['sameTickGuardProbes']=[x for x in data['records'] if x['name'].endswith('-same-tick-guards')];e['eventHashMeaning']='SHA256 of RGBA bytes encoded as hex string, not decoded RGBA digest; exact sourceRegistration keys use actual decoded RGBA SHA256.'
e['sourceCapturesUnchangedAfterGuardFix']=all(Image.open(f).convert('RGBA').tobytes()==Image.open(O/'first-clock-cache-interval'/f.name).convert('RGBA').tobytes() for f in O.glob('*-source.png'))
e['nativeCapturesUnchangedAfterGuardFix']=all(Image.open(f).convert('RGBA').tobytes()==Image.open(O/'first-clock-cache-interval'/f.name).convert('RGBA').tobytes() for f in O.glob('*-room.png'))
e['visualReview']='All190source/native presentations inspected in4boards. Authored pose progression replaces direct walk/prone jump; dynamic first/last endpoint phases present and walking advances after release. Water material still visibly changes at upright/wet classifications; full source/contact/continuous motion acceptance incomplete.'
inputs=json.loads((P/'fixture-inputs.json').read_text());e['originalMainStillMatchesPreparedCopy']=hashlib.sha256((R/'scripts/main.gd').read_bytes()).hexdigest()==inputs['originalMainSHA256'];e['normalGridStillMatchesPreparedInput']=hashlib.sha256((R/'scripts/grid_canvas.gd').read_bytes()).hexdigest()==inputs['gridSHA256']
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note=f'''## Bill East moving land/water source bridge exercised — October 2, 2026

Unselected grid.gd extends normal grid renderer; generated fixture main differs
only in GridCanvasScript preload. Actual normal Bill actor/navigation/needs/
oxygen/safety and room renderer retained. Prescribed actual clear East/West path/
ten-second water history; bare+helmet, two native East boundary windows every
60Hz tick. Dynamic exact prior-tick outgoing source and actual incoming gait
source replace study endpoints. Six-pose entry/seven-pose independent exit,
500ms each; target grid/player phase rebind at completion preserves exact incoming
endpoint and future walking progression. Combined exact source alpha/pivot/H148
envelope checked through existing segment/swim clearance at admission and each
display update. No teleport, pose rescale/body repaint or normal selection.

First2165nativechecks0fail/120.43s interval retained separately. Code review found
same-time cached output could bypass takeover guards; cache removed. Added eight
synthetic same-clock gear/facing/death/stage probes across both gears, restoring
fixture-only actor/player/bridge state afterward. Final{data['checks']}checks0fail/
{v['seconds']}s/engine0;2931owner non-log files unchanged/scratch APPDATA. Four
entry/exit admissions and exact endpoint completions; both actors continue actual
route. Same-clock guards return authoritative normal source, not cached pose.
Not natural interruption/death completion/refuge/gear gesture or Continue proof.

190advancing native/source boundary presentations/380original paired files
retained; all inspected in four full boards.8lossless APNGs verify380decoded
capture intervals with16/17ms absolute-rounded60Hz timelines (750ms entrance
window/833ms exit window), not just500ms source holds. All190source captures
unchanged after guard fix. Source panes registered from exact loaded normal or
candidate hashes/H148/pivot, no per-pose normalization. EventSHA fields hash
hex-encoded RGBA strings; review sourceRegistration keys are decoded RGBA hashes.

Visual motion/contact/master acceptance remains incomplete: source pose progression
replaces abrupt upright/prone jump, but water shading visibly changes across
upright/wet textures. Entry study all-wet flags and exit default swim prefix remain
provisional; dynamic original endpoints carry their normal metadata. Need deliberate
pose-aware surface/material/contact classification before admission. No continuous
unpaused gameplay, natural hydrology/jobs/full station, other directions or paired
checkpoint/Title Continue proof. Initial review requested image before packaging
process completed; waited same live handle, no restart, then inspected final files.

Lesson: bind actual outgoing and destination gait clocks (bare grid versus helmet
player), union visible source bounds, and recheck takeovers even at same render
time. Timing/collision green does not prove consistent water shading or physical
support. Next material/contact continuity, actual priorities/gear/death/Continue,
all cardinal bridges and normal guarded admission; cargo lifecycle and full Bill
master/cross-family polish remain. Goal active/incomplete. No commit/export.
Review: character/bill-land-water-runtime-east-v1/index.html.

'''
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 f=R/rel;f.write_text(note+f.read_text(encoding='utf-8'),encoding='utf-8')
for rel in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=R/rel;f.write_text(f.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');f.write_text(f.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill staged East land/water runtime

## Objective and acceptance
Full master-consistent Bill set, then cross-family polish. This staged native
interval does not complete water material/contact or full-set acceptance.

## Accepted decisions and constraints
Exact original source phases, original actor/world movement and safety, actual
source envelopes, no per-pose fitting/repaint/teleport. Scratch APPDATA and strict
owner-profile protection. Preserve other actors/concurrent source work.

## Current state
grid.gd+UID staged source adapter; generated fixture_main.gd+UID/scene with one
preload substitution, prepare.py, native test+UID and scratch validation runner.
Dynamic prior-tick outgoing/incoming source,500ms clock and target gait rebind;
combined bounds admission/update guard and same-tick gear/facing/death/stage cancel.
build_review.py/190captures/8APNG/4boards/review.json. First clock-cache native
interval preserved separately. Pipeline/bible/status/skills updated.

## Verification
Final2183native checks0fail/125.13s/engine0;2931owner non-log files unchanged.
Both gears enter/exit complete on exact incoming phase; post-exit walking advances.
Eight synthetic same-clock takeover probes pass; not natural priority completion.
190source/native pairs inspected,380APNG intervals decode exact. Actual60Hz
fixed-step capture in prescribed route/water windows, not unpaused gameplay.
All190source images unchanged after cache removal. No normal production changes.

## Next action
Water shading still changes at upright/wet classification. Fix pose-aware surface/
material/contact before normal admission. Actual priority/gear/death/Continue,
cardinal expansion, natural route/hydrology and full source/master/motion polish
remain. Generated fixture is a reproducible isolated copy, not a main refactor.
Current bridge banks are source studies, not accepted checkpoint bindings.
Cargo lifecycle/full set incomplete; no commit/export.
''',encoding='utf-8')
print('Native bridge milestone recorded; water material/contact and full goal still incomplete.')
