from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
entry='''## James paired water clips staged - 2026-09-30

All four tread/swim/start/stop sets packaged,16 states/96 references per mode.
Common256x276 canvas/pivot128,128; fixed source scale, preserved960ms loops and
520ms transitions, exact shared endpoints and reversed stops. Fixed master gold
gain/matte curve with protected source heads. North four-interior v4 removes the
invented medical marking and is staged at a separate fixed source-density scale.
Four independently authored shared-helmet pitch sheets fitted at master shell
widths35/39/35/33 E/S/W/N. Corrected south stroke3 head anchor571 to544 sourceY
after enlarged seam audit exposed goggles outside helmet; source body unchanged.
695 bare+548 helmet packaging checks and2054 paired native loader/clock/transition
checks PASS, zero failures; scratch profiles unchanged. Four native82px contacts
reviewed. These are staged candidates: actual water routing, selected-pixel
clearance, continuous route rendering and installation remain. Current installed
inventory still68 retained bare; full-set/polish goal remains active.
See docs/JAMES_WATER_HANDOFF_2026-09-30.md and family/station-review.gif.

'''
lesson='''

### James registered water/helmet staging - 2026-09-30

Build water reviews with the actual common world pivot, not bottom-aligned source
auditions. Reuse exact tread/swim endpoint pixels and reverse the authored start
for stop while retaining existing timings/water metadata. A new sheet may have
different source density: calibrate one anatomical scale for that whole sheet,
record the cranial ruler, and inspect torso/neck/limbs separately. James north
interiors use22/106, main sheet22/47; neither is per-pose height normalization.
Shared-shell donor calibration excludes the collar below the cranium. Independently
author forward swimming pitch; dry lying head donors can lean the wrong way.
An anchor that includes the chin can leave original goggles/hair above the shell:
inspect enlarged source cranial regions before expanding an erase mask. James
south stroke3 source headY571 was27 pixels too low; correcting it to544 fixed both
registration and protected-head grading. Do not conceal such defects by deleting
extra torso pixels. Reject yawed rear helmet donors and retain source overhead
glove pixels where they cross the upper head region. Pixel/clock/native contact
checks establish those scopes; real water routing and continuous renderer contact
remain necessary before installation. Evidence: JAMES_WATER_HANDOFF_2026-09-30.md.
'''
for rel,text,prepend in [('docs/CURRENT_STATUS.md',entry,True),('docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',entry,False),('docs/ASSET_PIPELINE_AND_WORKFLOW.md',lesson,False),('docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',lesson,False),('skills/brinespace-character-pipeline/references/crew-consistency.md',lesson,False)]:
 path=R/rel;marker=text.strip().splitlines()[0].encode()
 if marker not in path.read_bytes():atomic(path,lambda b,t=text.encode(),p=prepend:t+b if p else b+t)
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if lesson.strip().splitlines()[0].encode() not in path.read_bytes():atomic(path,lambda b:b+lesson.encode())
def selection(b):
 m=json.loads(b);m.update(status='paired_packaged_native_loader_verified_staged',runtimeInstalled=False,helmetPaired=True,northStartInteriors='../james-water-north-v1/source-start-interiors-v4.png',northStartInteriorsStatus='Staged source-density correction; unsupported cross removed; real continuous water-route review pending',pending=['Selected-pixel clearance including transition reach','Actual water routing and continuous runtime rendering','Route-level anatomical/helmet continuity review','Paired runtime installation','Full-set consistency and polish']);m['verification']={'barePackagingChecks':695,'helmetPackagingChecks':548,'pairedNativeChecks':2054,'failures':0,'realProfileUnchanged':True};return (json.dumps(m,indent=2)+'\n').encode()
atomic(P/'selection.json',selection)
handoff='''# Project handoff

Updated: 2026-09-30 · Project: C:/Users/Alex/Documents/Brine Space · Task: James water family

## Objective and acceptance
Continue James's full master-matched set, then cross-animation consistency/polish.
This milestone packages tread/swim/start/stop all four directions, bare/helmet.
Staged candidates; no runtime installation or owner acceptance.

## Accepted decisions and constraints
Matte graphite/silver/muted gold, source identity/department/asymmetric belt wrench
retained; independently authored facings. Old grayscale water clips guide stroke
only, not physical proportions. Fixed anatomical scale per sheet; never normalize
bent knees or prone silhouettes to standing height. Reversible work authorized.

## Current state
character/james-water-{east,south,west,north}-v1 contain sources/prompts, retained
contracts, extraction/auditions, registered-ungraded poses,96 bare+96 equipped
references, manifests/hashes, explicit head anchors and independent helmet donors.
Family build.py/fit_helmets.py reproduce from local source. Main anatomical scales
E.5/S.480769/W.471698/N.468085; north four-interior v4 fixed22/106 source-density
scale. v4 removes unsupported cross; v3 and original yawed row preserved.
Common256x276/pivot128128/standing148. Loop960ms, start/stop520ms. Exact loop
seams/shared transition endpoints, reversed stop. Fixed master-class gold gain
and matte body curve; original cranial pixels protected. Shared helmet shell rulers
35/39/35/33 E/S/W/N; one calibrated source scale per direction. Rear donors2/3
rejected for sideways tilt; original overhead glove pixels retained. South stroke3
headY corrected571->544 after enlarged seam audit, avoiding larger torso erasure.
Origins/provenance in source-origins/helmet-source-origins and north v4 origin.
station-review.gif displays registered paired clips at82px; native-*-contact.png
are fresh Godot filtered82px contacts. Runtime installed inventory remains68
retained bare states. No edits to runtime loaders, NPC behavior or clearances.

## Verification
695 bare packaging checks,548 helmet composition/contracts checks PASS.2054 paired
native loader/simulation-clock/pause/start-stop handoff checks PASS, zero failures;
96 slots/mode matched disk pixels. Scratch APPDATA helper records real profile
unchanged. Four fresh native contact images visually reviewed; initial bare1026
native checks preserve earlier scope. This is not proof of selected runtime packs,
actual path clearance, uninterrupted flood/exterior routes or owner acceptance.

## Next action
Derive clearance envelopes from selected alpha/pivots for both modes, including
diagonal transition reach. Exercise actual James water routing/pose-clearance and
continuous grid rendering in scratch profiles, review full launches/loops/stops,
then install literal manifest paths and paired registry selection if sound.
Revisit north torso/neck/pitch if continuous route review exposes a size pop.
Then water turns/carry/pickup/salvage/distress/recovery/death and full-set polish.
Goal stays active; this staged milestone does not certify the complete set.
'''
atomic(R/'docs/JAMES_WATER_HANDOFF_2026-09-30.md',lambda b:handoff.encode())
seq=[('tread',j,160) for j in range(6)]+[('swim-start',j,t) for j,t in enumerate([70,90,100,100,90,70])]+[('swim',j,160) for _ in range(2) for j in range(6)]+[('swim-stop',j,t) for j,t in enumerate([70,90,100,100,90,70])]
gif=[];dur=[]
for action,j,t in seq:
 im=Image.new('RGB',(720,360),'#303b40');dr=ImageDraw.Draw(im)
 for col,d in enumerate(['east','south','west','north']):
  p=P.parent/('james-water-'+d+'-v1')
  for row,mode in enumerate(['bare','helmet']):
   f=p/'frames'/action/f'{j:03d}.png' if mode=='bare' else p/'frames/helmet'/action/f'{j:03d}.png';sprite=Image.open(f).convert('RGBA');sc=82/148;sprite=sprite.resize((round(256*sc),round(276*sc)),Image.Resampling.LANCZOS);at=(round(col*180+90-128*sc),round(row*180+90-128*sc));im.paste(sprite,at,sprite);dr.text((col*180+8,row*180+8),d+' / '+mode,fill='white');dr.text((col*180+8,row*180+25),action,fill='#cbd5d8')
 gif.append(im);dur.append(t)
gif[0].save(P/'station-review.gif',save_all=True,append_images=gif[1:],duration=dur,loop=0,disposal=2,optimize=False)
print('Paired water staging milestone recorded; runtime/routes/clearance remain pending')
