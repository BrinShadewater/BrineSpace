from pathlib import Path
import json,hashlib,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
def atomic(p,b):
 t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(b);os.replace(t,p)
def write(p,v):atomic(p,(json.dumps(v,indent=2)+'\n').encode())
before=read(P/'source-inputs-before.json');after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before};assert before==after;write(P/'source-inputs-after.json',after)
e=read(P/'pose-evidence.json');motion=[r for r in e['records'] if not r['key'].startswith('idle-')];assert len(motion)==108 and len(e['joins'])==10 and all(j['registeredRGBAExact'] for j in e['joins'])
review={'status':'source_motion_review_material_mismatch_open','motionReferencesReviewed':108,'clipsPerGear':9,'allPoseBoardsReviewed':9,'mastersCompared':'North and West selected idle frame0, same declared148 ruler; displayed separately from water anchor','browserObservations':[{'key':'death-water-west','timeSeconds':[.02,3.87],'poses':[0,5]},{'key':'swim-north','timeSeconds':[.02,.52],'poses':[0,3]},{'key':'swim-west','timeSeconds':[.02],'poses':[0]}],'browserScope':'Observed selected source replay advancing beside masters at148/82 ruler. All nine clips available; not every clip continuously watched, no native-motion proof.','findings':['North/West tread/start/swim/stop pose sequences retain compact legs and boots.','All10 tested registered start/swim/stop/West death-entry pairs exactly match. Tests bind swim frame0, not every arbitrary active swim phase.','West death interiors1-5 visibly have brighter slightly pink knee/boot hardware and fuller lit limb patches than swim entry. Material polish remains open despite repaired compact leg projection.'],'diagnostic':'material-diagnostic.json broad rear-body ROI: pooled per-pose P90 RGB swim[100.2,91.9,89.8],death[112.4,102.3,102.3]; neutral mean>100 fraction .077 vs .118. Not semantic or physical lighting measurement.','productionInputsUnchanged':len(before),'artOrProductionChanges':False,'engineRun':False,'ownerAcceptance':'pending','fullSetComplete':False}
write(P/'selection-review.json',review)
note='''## James North/West water motion comparison — October 1, 2026

All108 selected North/West tread/start/swim/stop and West water-death source slots
reviewed across nine paired boards, both gears, original durations and declared148
ruler/pivots. Interactive source replay displays separate same-scale standing masters
and82-ruler samples. Browser observed West death entry/terminal and North swim0/3;
West swim entry also rendered. All10 tested registered action joins exact, binding
swim frame0 rather than arbitrary live phase.405 source/manifest/loader inputs
unchanged.396 loaded references include288idle slots; only idle0 shown as master,
not396 visually reviewed poses. No native engine or owner profile access.

Remaining visible defect: West water-death interiors1-5 have brighter, slightly pink
knee/boot highlights and fuller lit limb patches than selected swim entry. Compact
leg projection is retained from the installed September30 repair, but material
continuity is not accepted. Broad fixed rear ROI corroborates brighter values:
P90 RGB swim100.2/91.9/89.8 vs death112.4/102.3/102.3; mean>100 fraction.077 vs.118.
This mask includes pose-dependent boots/hardware, not semantic matte certification.

Evidence/HANDOFF:character/james-water-motion-review-2026-10-01. Source replay only,
not native travel/depth/mortality/cadence. No source/art/timing/production changes.
Next address West water-death material interiors while retaining exact entry,
compact anatomy, shared helmet, source provenance and original clock. Then remaining
furniture/exterior journeys and full-set cross-family polish. Full goal remains open.

'''
p=R/'docs/CURRENT_STATUS.md';atomic(p,note.encode()+p.read_bytes())
lesson='''
## James water endpoint versus interior material review — October 1, 2026

Exact cross-family endpoint joins and a repaired limb silhouette do not establish
whole-clip matte continuity. Review every selected source pose at the authored
water anchor, original durations and same148 physical ruler; place standing masters
separately rather than fitting prone silhouettes to standing height. North/West
water review inspected108motion slots/nine paired boards,10exact frame0-bound joins.
West death1-5 still shows brighter slightly pink knee/boot hardware than swim entry.
Broad fixed rear-body ROI supports this visible difference, but includes changing
pose coverage and hardware; do not call it a semantic matte or lighting test.

Source playback observed West death entry/terminal and North swim changing0->3
beside selected masters at148/82 ruler. This is not every clip continuously watched
or actual world-route/mortality evidence.396loaded refs include288idle poses;
108motion poses and idle0masters were visually reviewed.405input hashes unchanged,
no source/timing/production edits or native/profile access. Evidence:
character/james-water-motion-review-2026-10-01. Correct material interiors without
undoing compact leg projection or exact entry, then recheck the entire finite clip.
Full James goal and owner acceptance remain open.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:atomic(p,p.read_bytes()+lesson.encode())
handoff='''# Project handoff

Updated: October1,2026 · Project:Brine Space · Task:James water source motion/material

## Objective and acceptance
Full James set/master/style/size/perspective/proportions/grade, then family polish.
Previous goal turn was progress:18disk locker checkpoints passed and recorded.
Current progress finds material mismatch requiring repair; full goal remains open.

## Accepted decisions and constraints
Matte graphite/ochre, compact projected legs, canonical helmet, independent facings,
148ruler, original pivots/durations, exact swim entry. No per-pose height fitting.

## Current state
New reproducible review builder,9paired pose boards,108motion preview PNGs,
interactive index.html/playback.json, pose/hash reports, broad material diagnostic,
selection review and recorder. Five maintained guides updated atomically.
Live loopback preview server execsession90906 port8796; browser tab1 retained.
No source/art/manifest/timing/production edits; no engine/profile access.

## Verification
All108motion slots/nine boards inspected, separate North/West idle0masters.
Browser source clock observed death0->5,Northswim0->3,Westswim0. Every clip playable,
not every clip continuously watched.10normalized fullRGBA joins exact; swimframe0
only, not arbitrary active phase.405source/manifest/loader hashes unchanged;
396loaded refs include288idle slots, not all396 visually reviewed.
West death1-5 visibly brighter/pinker knee/boot hardware/full lit patches than swim;
rearROI P90RGB100.2/91.9/89.8 swim vs112.4/102.3/102.3 death supports concern.
Material polish OPEN, not native cadence/world mortality proof or full-set acceptance.

## Next action
Repair selected West water-death material interiors while preserving exact entry,
compact anatomy, canonical helmet/provenance/finite timing. Recheck all6paired
poses and playback. Continue remaining full furniture/exterior journeys and polish.
'''
atomic(P/'HANDOFF.md',handoff.encode())
print(json.dumps({'motionReviewed':108,'joinsExact':10,'inputsUnchanged':len(before),'materialMismatchOpen':True}))
