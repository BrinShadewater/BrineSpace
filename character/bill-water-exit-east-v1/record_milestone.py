from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;A=R/'character/bill-land-water-phase-audit-v1'
game=Image.new('RGB',(1152,460),'#182932');d=ImageDraw.Draw(game)
for j,h in enumerate([82,54,27]):
 for i in range(6):
  im=Image.open(P/f'frames/swim-land-east/{i:03}.png').convert('RGBA');im=im.resize((round(320*h/148),round(320*h/148)),Image.Resampling.LANCZOS);game.paste(im,(i*192+(192-im.width)//2,j*150+20),im)
 d.text((5,j*150+3),f'{h}px standing ruler',fill='white')
game.save(P/'gameplay-review.png')
html=(P/'index.html').read_text();(P/'index.html').write_text(html.replace('<img src="source-leave.png">','<img src="gameplay-review.png"><img src="source-leave.png">'),encoding='utf-8')
note='''## Bill actual phase audit and separate water exit — October 2, 2026

New phase audit binds exact normal-loaded retained route sources: enter tick64
walk28 -> tick66swim0 both gears; leave tick412swim2 -> tick414walk34bare/
walk0helmet. These are last/first30Hz samples, NOT exact60Hz handoff state.
Four new500ms source montages use captured endpoints and unchanged four bridge
interiors; all24decoded frames exact. Four full boards inspected. They expose
walk-stride versus idle entrance mismatch and swim2 tucked arms versus reversed
reaching interior. Separate bare grid clock/helmet player clock require actual
runtime coordination; merely replacing endpoints does not solve phase admission.

Authored distinct bare exit, not reversed entrance: tucked swimmer -> boot plant
-> crouch -> first step. Three built-in sources/exact prompts retained. V1 heads/
landscape proportions unsuitable; V2 head-only edit changed bodies, rejected.
Portrait V3 gives more room for near-standing pose. Four alpha>250components/
3pxfringe, one.24approximate near-standing anatomical scale across all interiors,
frozen entry-V2 neutral curve. No per-pose normalization/body painting. Exact
captured normal swim2/walk34 endpoint RGBA and6APNGframes/500ms verified.
Original-master board inspected: tucked-arm phase and near-standing stature
closer; source/art review remains incomplete, initial rise spacing visibly large.
Crown targets181->108->98->76 do not prove support/contact or smoothness.

No native bridge replay, Godot run, production loader/controller/renderer changes
or owner profile access this interval. Draft does not assign runtime water-mode
metadata. Next authored midpoint/registration for tucked-swimmer -> planted boot,
master/density review, paired helmet after source gate, exact60Hz gait sampling,
finite clocks/collision/support/safety/Continue and cardinal expansion. Full Bill
set/master/cross-family polish goal active/incomplete. No commit/export.

Lesson: sample actual outgoing/incoming gait phases before authoring transitions.
Reverse entry can violate elbow/leg phase on exit. A head-only generated edit is
not preservation evidence; retain failed result. Choose atlas cell aspect ratio
that fits original standing anatomy rather than encouraging short/thick legs.
Reviews: character/bill-land-water-phase-audit-v1/index.html and
character/bill-water-exit-east-v1/index.html.

'''
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 f=R/rel;f.write_text(note+f.read_text(encoding='utf-8'),encoding='utf-8')
for rel in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=R/rel;f.write_text(f.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');f.write_text(f.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill actual phase audit/separate water exit

## Objective and acceptance
Complete Bill's full master-consistent animation set and cross-family polish.
Source availability and package checks do not establish motion/native acceptance.

## Accepted decisions and constraints
Original master and exact normal endpoints; fixed shared scale/matte grading.
No per-pose normalization or body painting. Preserve other actors/owner state.

## Current state
Phase-audit build/evidence, four montages/APNGs and endpoint boards. Separate
exit raw3generations/prompts, build/manifest/registration, master/density/APNG
review. Landscape V1/head-attempt V2 rejected; portrait V3 source-only candidate.
Four new exit interiors preserve tucked arms rather than reversing reaching entry.
Pipeline/bible/current-status/Bill continuation/maintained+installed skills updated.

## Verification
Actual retained normal-source hashes/pivots/H148 bound to30Hz boundary captures.
Four6-frame phase APNGs and one6-frame exit APNG decode exact/500ms each.
Original exit endpoints exact; fixed.24body scale/frozen neutral curve.
All phase boards and original-master exit board inspected. No Godot run/native
bridge/production admission. Actual60Hz transition frame not yet captured.

## Next action
Fix large initial rise gap between tucked swimmer and boot plant, assess full
source/master/material/density before fitting helmet. Stage separate bare and
helmet playback clocks with exact incoming phase/terminal handoff; then contact/
collision/medium, priorities/Continue/native motion/allcardinals. Cargo lifecycle,
water treatment admission and full-set consistency remain. Full goal incomplete.
'''
for folder in [P,A]:(folder/'HANDOFF.md').write_text(handoff,encoding='utf-8')
e=json.loads((P/'registration.json').read_text());e['visualReview']='Original master/full sequence inspected; first rise spacing remains visibly large. No motion/contact acceptance.';(P/'registration.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('Phase mismatch and independent exit source milestone recorded; next initial rise midpoint/support; full goal incomplete.')
