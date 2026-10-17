from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
package=json.loads((P/'packaging-validation.json').read_text());native=json.loads((P/'native-staged-validation.json').read_text());assert package['passed'] and native['exitCode']==0 and native['realProfileUnchanged']
def atomic(file,fn):
 before=file.read_bytes();after=fn(before);temp=file.with_name(file.name+'.james.tmp');temp.write_bytes(after)
 if file.read_bytes()!=before:temp.unlink();raise RuntimeError('Concurrent edit '+str(file))
 temp.replace(file)
note='''### James distress and recovery staging — September 30, 2026

Eight states/48refs per mode staged in character/james-air-family-v1. Four
independently authored12-body facing sources, with retained originals/prompts and
revisions. ES source density differs between water and dry rows: use one fixed
anatomical skull ruler per action row, never independent per-pose silhouette height.
E scales25/65water,25/70dry;S25/78water,25/72dry;W25/60water,25/70dry;N22/66both.
These remain anatomy auditions requiring final source consistency review.

Current selections:E water v2 unchanged, recovery v3 profile;Wv3both;Nv2both;Sv1.
East v2 compressed excessive dry legs; v3 narrowed side torso/feet but masters'
camera/stance must remain the authority. West wrench restoration put it prominently
on the near hip despite the master placing it on the farther partially occluded hip;
v3 failed to correct that, so do not promote West as equipment-consistent. A fresh
master-only recovery-row remake is the next useful route if edits keep preserving
the wrong camera/tool ownership. Preserve already successful water source crops
explicitly: generated edits do not guarantee unmentioned pixels stay unchanged.

Northv2 shortens overly long projected water legs and moves chest-reaching gloves
away from the backpack. Warm-component rear head detection selected brown boots:
manually inspect crown proxies; do not label these measured shoulder registration.
Sealed-helmet fitting reuses selected water donor4 for prone,donor1 for leaned dry,
donor0 for upright. Source/donor provenance and owned head region are recorded.

Canvas256x360,p128224,standing148 preserves physical scale with96px extra upper
registration space versus water'sp128128. Exact currently selected swim0 endpoints
close960ms distress loop; exact idle0 closes3s finite recovery. Retained per-pose
water flags/facing/depth/timing are unchanged. Boot-contact midpoint governs dry
registration, cranial anchor governs prone; no per-pose bounding-height fitting.

528 packaging and1045 standalone native player/render checks PASS, owner profile
unchanged;82px bare/helmet contacts viewed. These prove pose selection/clocks/alpha
and endpoint provenance, not anatomy acceptance or actual life-state progression.
Candidate distress life clearance derived, runtime/registry/selected live clearance
unchanged. Need actual RoomFlooding.step_crew low-air→safe-room recovery, pause and
completion checks, normal grid and clearance after source/equipment refinement.
16 live states remain retained;8 are now staged here,8death states still unauthored.
Full-set material/anatomy/timing/readability/journey consistency pass remains open.
See docs/JAMES_AIR_STAGING_HANDOFF_2026-09-30.md.
'''
headline='''## James distress and air recovery staged — September 30, 2026

Eight independently authored states in both modes, exact swimming/standing seams,
retained960ms/3s clocks.528 package and1045 standalone native checks PASS,82px
contacts reviewed; owner profile unchanged. Further side-view anatomy and West
wrench ownership refinement required before actual life-state integration.
Runtime unchanged;16 retained states,8 staged here and8 death states still to make.
Full-set consistency/polish remains. See [handoff](JAMES_AIR_STAGING_HANDOFF_2026-09-30.md).

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
for file in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 atomic(file,lambda b:b if note.encode() in b else b+b'\n\n'+note.encode())
(R/'docs/JAMES_AIR_STAGING_HANDOFF_2026-09-30.md').write_text('''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James distress/recovery candidates

## Objective and acceptance
Full James animation set then cross-family consistency/polish. This milestone stages
eight new states; runtime still has16 retained states. Full goal remains active.

## Accepted decisions and constraints
Matte neutral masters, exact anatomy/perspective/scale, wrench on original anatomical
belt hip. Prone distress loop960ms; dry recovery3s with planted feet and exact idle
completion. Do not force crouched/prone/fallen poses to standing silhouette height.

## Current state
character/james-air-family-v1 and four james-air-{direction}-v1 source folders.
8states/48refs per mode,256x360,p128224,standing148. Source/E/W/N repairs retained:
E water v2/recoveryv3,Wv3,Nv2,Sv1. Existing shared helmets fitted at fixed shell size.
Scripts/configs/provenance/endpoint hashes/review.gif/native contacts and candidate
distress clearance recorded. Pipeline,bible,continuation and skills updated.

## Verification
528package and1045 standalone native checks PASS; owner profile unchanged.
Exact swimming loop/standing completion, retained clocks/metadata, source/donor
hashes, head-owned compositing, nonclipped exports and82px both-mode contacts reviewed.
No actual low-air/recovery simulation, installed loader, routing or owner acceptance.

## Next action
Refine E/W recovery side camera/stance against actual idle. West generated wrench is
still on wrong prominent near hip despitev3 request; remake source from master only
if constrained edits keep anchoring wrong ownership/camera. Keep successful E water
v2 source explicitly. Nrear cranial proxies are manual because warm detector chose
boots. Review helmet collars/hand overlap, stance/material seams in all directions.
Then scratch native RoomFlooding.step_crew low-air/safe-room/recovery timing/pause/
completion + normal grid candidate clearance, install actual8states and revalidate.
Generate8 ground/water death states, then full-set polish/journey consistency audit.
No live generation/test jobs, commit, export or full-set completion.
''',encoding='utf-8')
(P/'selection.json').write_text(json.dumps(dict(status='staged_anatomy_equipment_review_required',runtimeInstalled=False,fullSetComplete=False,statesPerMode=8,refsPerMode=48,nativeReview='82px standalone contacts reviewed',pending=['Side recovery camera/stance consistency','West wrench anatomical hip ownership','Actual low-air/recovery progression and installed loader/clearance']),indent=2)+'\n')
for mode in ['bare','helmet']:
 def status(b):
  m=json.loads(b);m['status']='staged_anatomy_equipment_review_required';return (json.dumps(m,indent=2)+'\n').encode()
 atomic(P/(mode+'-manifest.json'),status)
print('Recorded new source/staged evidence and unresolved anatomy/equipment issues; goal active')
