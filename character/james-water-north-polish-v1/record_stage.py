from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
v=json.loads((P/'native-staged-validation.json').read_text());assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged']
assert json.loads((P/'package-verification.json').read_text())['checks']==209
selection=dict(status='staged_not_installed',runtimeInstalled=False,fullSetComplete=False,
               statesPerMode=3,refsPerMode=18,packageChecks=209,nativePlayerChecks=427,
               realProfileUnchanged=True,source='../james-water-north-v1/source-polish-v6.png',
               visualReview='Paired source/native82px complete pose boards and old/new comparison midpoint',
               pending=['Early arm raise is too abrupt: author a bent-elbow intermediate before overhead reach',
                        'Actual North water-route motion and effective clearance',
                        'Live runtime installation and final native regression','Owner/full-set acceptance'])
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
def atomic(path,fn):
    before=path.read_bytes() if path.exists() else b'';after=fn(before)
    if before==after:return
    tmp=path.with_name(path.name+'.north-water.tmp');tmp.write_bytes(after)
    if (path.read_bytes() if path.exists() else b'')!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
    tmp.replace(path)
note='''### James North water anatomy audition — September 30,2026

Old-atlas motion references can overpower a small accepted master and reproduce
chunky boots/short legs. North water polish v5 did so and added diagonal yaw/roll;
retain rejection evidence. Master-only nearest-neighbor enlarged reference v6
restored slim calves/boots and a straight rear lean. A skull-only22/66 ruler gave
159px neutral vs148px master; whole-body density comparison supports one fixed
148/478 scale for the complete independently drawn source. Never resize each
pose to identical height. Preserve foreshortening and exact selected swim join.

Staged paired tread/start/stop:209 package and427 native player checks PASS;
owner profile unchanged. Native82px all-pose board reviewed. These checks prove
loading, clocks and phase joins, not smooth arms: the first lean reaches overhead
too abruptly. Author a bent-elbow lead-in before route testing/promotion. Shared
helmet edits remain confined to cranial ownership. Base library fixture loads
must append overrides; replacement clears the swim destination. Failed fixture
retained, corrected rerun PASS. Runtime still uses earlier selected water art.
See docs/JAMES_NORTH_WATER_POLISH_HANDOFF_2026-09-30.md; full James goal active.
'''
for path in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(path,lambda b:b if note.encode() in b else b+b'\n\n'+note.encode())
headline='''## James North water anatomy polish staged — September30,2026

Master-only v6 source improves slim boots/calves and straight rear lean. Paired
tread/start/stop staged:209 package/427 native playback checks PASS; profile
unchanged. Native82px pose board reviewed. Early overhead arm raise still needs
a bent-elbow lead-in, then actual route/clearance and installation proof. Runtime
water art unchanged. [Handoff](JAMES_NORTH_WATER_POLISH_HANDOFF_2026-09-30.md).
Full James goal active.

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
handoff='''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James North water anatomy polish

## Objective and acceptance
Complete James set, master matching and cross-family polish. Candidate stage
improves proportions; live installation and full motion acceptance pending.

## Accepted decisions and constraints
Neutral matte graphite/gold, slim master calves/boots, no enlarged soles or
backpack, straight rear camera through lean, belt wrench persists. Independent
source art and single fixed density; no per-pose body resizing or limb splicing.

## Current state
character/james-water-north-polish-v1 has paired3-state36-reference candidate,
builder/209-check verifier/427-check native playback fixture/comparison media.
Source-polish-v6 and exact prompt/origin retained in james-water-north-v1.
V5 rejected for inherited bulk and diagonal lean; its audition/origin retained.
V6 one fixed148/478 scale. Existing clocks and exact selected swim endpoint
retained; shared helmet donors reuse fixed shell scale and owned head edit.
Runtime/registry unchanged. Pipeline,bible,continuation and both skill copies updated.

## Verification
209 package PASS,427 staged native loader/clock/transition checks PASS,zero
failures/timeouts/profile delta. Native82px48-pose board reviewed including
unchanged swim. Old/new paired comparison midpoint reviewed. Fixture initially
replaced base library and lacked swim; exact confirmed process terminated,
failed logs retained, append correction rerun passed. No engine changes.
Visual issue: first lean raises both arms overhead immediately; package/phase
checks cannot certify smooth limb motion. No actual route proof this revision.

## Next action
Author an independent bent-elbow lead-in pose between neutral and overhead reach,
using v6/master proportions, preserve whole-body source and fixed material curve.
Review full transition, then stage actual North water routes/clearance before
promotion. West water death limb seam, workstation facing turns and full
furniture/meal/equipment/exterior journeys remain. No processes running;goal active.
'''
atomic(R/'docs/JAMES_NORTH_WATER_POLISH_HANDOFF_2026-09-30.md',lambda b:handoff.encode())
print('Staged North water milestone recorded; early arm lead-in pending; runtime unchanged')
