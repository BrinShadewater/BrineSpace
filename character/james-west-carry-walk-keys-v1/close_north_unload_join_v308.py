from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-join-review-v308';audit=p/'north-unload-join-audit-v307';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((audit/'inputs.json').read_bytes());assert all(sha(r/x['file'])==x['sha256'] for x in d['sources']);selection=json.loads((o/'selection.json').read_bytes())
for gear in ('bare','helmet'):
 q=o/gear;v=json.loads((q/'native_probe-validation.json').read_bytes());n=json.loads((q/'native-evidence.json').read_bytes());f=json.loads((q/'native-inputs.json').read_bytes());assert (n['checks'],n['failures'],n['captures'])==(65,0,6);assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta'];assert all(sha(r/x)==h for x,h in f['preLaunchSha256'].items())
 s=next(x for x in selection['gears'] if x['gear']==gear);assert sha(r/s['originalManifest'])==s['originalManifestSha256'];m=json.loads((o/f'{gear}-review-manifest.json').read_bytes());original=m['states'][0];candidate=m['states'][1];turn=m['states'][2];assert candidate['frameFiles'][0]==turn['frameFiles'][0];assert candidate['frameFiles'][1:]==original['frameFiles'][1:];assert candidate['frameDurationsMs']==original['frameDurationsMs'] and sum(candidate['frameDurationsMs'])==520
 decoded=Image.open(o/f'{gear}-unload-study.apng');assert decoded.n_frames==6
 for i,src in enumerate(candidate['frameFiles']):decoded.seek(i);assert np.array_equal(np.asarray(decoded.convert('RGBA')),np.asarray(Image.open(r/src[6:]).convert('RGBA')))
# Preserve full new bare turn chronology plus candidate unloading, merging only an
# identical adjacent hold for APNG packaging. The two native banks retain12slots.
turn=json.loads((p/'arrival-turn-chronology-v306/bare-review-manifest.json').read_bytes())['states'][1];unload=json.loads((o/'bare-review-manifest.json').read_bytes())['states'][1];files=turn['frameFiles']+unload['frameFiles'];clocks=turn['frameDurationsMs']+unload['frameDurationsMs'];merged=[];dur=[]
for src,clock in zip(files,clocks):
 im=Image.open(r/src[6:]).convert('RGBA')
 if merged and np.array_equal(np.asarray(merged[-1]),np.asarray(im)):dur[-1]+=clock
 else:merged.append(im);dur.append(clock)
assert len(merged)==11 and sum(dur)==1320;merged[0].save(o/'bare-turn-unload-study.apng',save_all=True,append_images=merged[1:],duration=dur,loop=0,disposal=0,blend=0);decoded=Image.open(o/'bare-turn-unload-study.apng');assert decoded.n_frames==11
for i,im in enumerate(merged):decoded.seek(i);assert np.array_equal(np.asarray(decoded.convert('RGBA')),np.asarray(im))
joined=dict(nativeSourceSlots=12,decodedApngFramesExact=11,totalMs=1320,mergedIdenticalBoundaryHoldMs=180,sources=[dict(file=f[6:],sha256=sha(r/f[6:]),durationMs=t) for f,t in zip(files,clocks)],scope='Latest306 bare turn plus candidate308 north unload; no new full helmet turn, observed continuous motion or actual arrival integration.')
(o/'joined-bare-inputs.json').write_text(json.dumps(joined,indent=2)+'\n')
report=dict(disposition='provisional_exact_turn_end_to_unload_source_join',nativeChecks=130,nativeFailures=0,nativeCapturesReviewed=12,sourceBoardsReviewed=True,firstFramesExactTurnEnd=True,remainingFiveFramesExactOriginal=True,unloadTimingMs=520,normalChanged=False,selected=False,sourceAcceptance=False,fullGoalComplete=False,findings=['Original unload0 begins with one foot advanced; unload1 already planted wider. Exact existing turn5 reused as candidate unload0 in both gears. Native cut continuity and unchanged finite timing verified.', 'Candidate0 to1 widens feet and changes equipment/cloth/body shape; subsequent crouch/drop/return unchanged. Same cut pixels are not full motion/anatomy/grade/physical support acceptance.', 'Runtime North comparison exports1024 square are whole quarter-size nearest decoded to256 for review; initial oversized comparison fixed before native. Reference-derived North raw remains candidate, not promoted original authority.', 'Bare joined306turn+308unload keeps12source slots/1320ms; APNG coalesces identical boundary100+80ms to180ms,11decoded frames byte-exact. No continuous observed playback or actual carry-to-unload turn selection tested.', 'Normal bank unchanged; full master-matched turn/helmet, latest49carry start, arrival/controller/save lifecycle and all-family consistency remain.'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n');(audit/'review.json').write_text(json.dumps(dict(disposition='paired_existing_north_join_source_audit',sourceBoardReviewed=True,frozenSources=18,referenceProvenanceInspected=True,normalChanged=False),indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old);j['northUnloadJoinReview']=dict(version=308,file=(o/'review.json').relative_to(r).as_posix(),firstFramesExactTurnEnd=True,selected=False,sourceAcceptance=False,normalChanged=False);j['nextVisualRepair']='308 paired exact old-turn5 to new-unload0 cut at520ms, bare306turn/unload1320ms joined study. Fix next0-to1 stance/material/head/gear joins and carry-stop starting source, master fidelity/early1px drift; new full shared-helmet turn and actual arrival/controller/save/Continue/normal admission still needed. Whole-family consistency/polish remain.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James exact north turn-to-unload source join - October3,2026

V307 paired original turnend/unload0..5/runtimeNorth comparison18inputs inspected.
Old unload0 advances one foot although unload1 is already planted. V308 candidate
unload0 reuses exact existing turn5 complete PNG in each gear; old1..5 and clocks
80/100/100/90/80/70ms unchanged, total520ms. No new generation, body edits, scaling
or colour painting; deterministic existing-source selection only. Normal selectors
unchanged. Runtime North comparison exports1024 are whole quarter-size nearest to
256 for review, corrected before native; reference-derived North raw provenance
explicitly remains candidate, not a newly accepted original master.

Both native gear runs65checks0/6captures each:130/0/12four-size captures all viewed.
Exact cut pixels, retained five images, metadata/timing/finite holds verified;
scratch owner unchanged and frozen runtime/manifest/source hashes stable. Paired
unloadAPNGs6decoded exact each. Bare306turn+308unload joined12source slots/1320ms;
identical100+80ms boundary hold merges to180ms in11decoded exact APNGframes.
No new continuous observed motion, actual controller arrival or physical foot support
proved. Carry-to-unload still bypasses generic facing turn in ordinary runtime.

Visual limit: new0to1 widens stance and changes cloth/backpack/body details; other
unloading crouch/return remains original. Exact cut continuity fixes the isolated
foot-forward pop but does not certify whole master fidelity, new shared helmet turn,
latest49carry/stop, head/grade/gear/body joins or normal lifecycle/save acceptance.
Full goal active/incomplete. Handoff:
character/james-west-carry-walk-keys-v1/north-unload-join-review-v308/HANDOFF.md.

Lesson: inspect the complete destination action before authoring extra movement.
If its first pose contains an unrelated step, exact reuse of the reviewed preceding
pose can establish cut continuity without introducing a new invented source. Still
review the next pose, timing and actual selector; exact endpoint pixels alone are
not natural gameplay motion. Check reference canvas size/provenance before display.
'''
guides=record_guides(r,section,'### James early turn angles and original-master face identity')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James north unload join

## Objective and acceptance
Complete master-matched James set, normal lifecycle and full-family polish.

## Accepted decisions and constraints
Master identity/matte grade/proportions/camera; wrench remains on belt. Exact source
reuse for joins; no body fitting or procedural painting. New work stays versioned.

## Current state and changed files
307 paired source chronology/provenance audit,18frozen sources.308 bare/helmet
six-pose manifests use exact existing turn5 for unload0, old1..5/timing untouched.
Two native probes/UIDs/frozen inputs/captures/source boards/APNGs; bare306turn+308unload
joined preview/input record/reviews. Ledger and five guides updated. Normal bank
unchanged; no new generation or replacement of ordinary source selectors.

## Verification and limits
Both source boards/paired audit and all12native four-size captures viewed.
Each gear65checks0/6captures, scratch owner unchanged/frozen hashes stable. Exact
turnend-to-unload0 pixels and520ms timing; paired6decodedAPNG each. Joined bare12
native-source slots/1320ms,11APNGframes exact after identical boundary hold merge.
No continuous observed replay, moving foot contact or actual arrival selector proved.
Next0to1 stance widens and material/equipment/body changes. Raw reference-derived
North candidate is not original master authority; runtime comparison1024 quartered
whole to256. Full shared helmet/new turn/art consistency and ordinary lifecycle open.

## Next action and remaining work
Resolve0to1/full-unload stance, head/body/material/gear continuity and latest49carry
stationary-turn start. Finish shared-helmet full turn and master matching/early1px
floor/crown drift. Actual carry-arrival turn currently bypassed by state change;
verify controller selection, full normal lifecycle/checkpoint/interruptions/Continue
after sources are coherent. Full directions/actions and all-family polish remain.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as out:out.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in (audit,o,o/'bare',o/'helmet') for f in folder.iterdir() if f.suffix in ('.png','.apng')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3));print(json.dumps(dict(nativeChecks=130,failures=0,capturesReviewed=12,unloadMs=520,joinedBareMs=1320,joinedDecodedExact=11,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
