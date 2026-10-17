from pathlib import Path
from PIL import Image
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
names=['contact-near','contact-far','contact-near-feet','contact-far-feet','near-feet2']
for name in names:
    inputs=json.loads((p/(name+'-inputs.json')).read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
    f=p/(name+'-review.json');data=json.loads(f.read_bytes());bounds=data.get('boundsAlpha128');data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_contact_source' if bounds[3]==224 else 'superseded_short_contact',findings=['Raw/full/detail/station comparisons inspected. Thigh-root crop gives actual opposed contact ownership: gold near thigh advances from original image-right hip in near pose; trails in far pose.','Original contact soles221/223, first near repair222; retained as short rejected-for-contact sources. Fixed near-feet2 and far-feet sole224.','Source-frame evidence only. Upper-body dynamics, passing poses, full gait cadence/native/cargo context and normal selection remain pending.'])
    f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
for name in ['pair-review','fixed-pair-review']:
    f=p/(name+'.json');data=json.loads(f.read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in data['sourceSha256'].items())
    data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_opposed_contacts_baseline_checked' if name.startswith('fixed') else 'superseded_short_contacts',findings=['Paired full and lower-detail boards inspected. Exact same generated leg pixels in both gears;59376outside lower-body pixels preserved relative to respective base.','Fixed sources reach224in both forward and rear-foot regions at alpha128; plain/gold ownership visibly alternates through hip/thigh/knee/shin.','Not a full gait bank: static base is not a generated passing phase. No timing/native/room/owner/full-master acceptance.'])
    f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
feet=[]
for name in ['near-feet2','contact-far-feet']:
    im=Image.open(p/(name+'.png')).convert('RGBA');bounds=[]
    for a,b in [(88,132),(132,168)]:
        box=im.getchannel('A').crop((a,197,b,240)).point(lambda v:255 if v>=128 else 0).getbbox();assert box[3]+197==224;bounds.append(box)
    feet.append({'source':name,'alpha128FootRegionBounds':bounds,'bothBottoms':224})
(p/'foot-contact-review.json').write_text(json.dumps({'footRegions':[[88,197,132,240],[132,197,168,240]],'poses':feet,'scope':'Static alpha128 foot-region contact geometry plus visual anatomy review; not walking foot sliding/cadence.'},indent=2)+'\n',encoding='utf-8')
section='''### James West cargo opposed contacts at master density — October 2, 2026

character/james-west-carry-gait-master-v2 expands crop to96square(80,144..176,240)
and lower-body admission88,154..176,224, below the carried case. Two independently
generated contacts now move entire thighs from original hips: gold near thigh
forward/plain far trailing versus plain far forward/gold near trailing. This is
visible hip-to-shin ownership, not a stripe reassignment.59376outside pixels exact
relative to respective bare/helmet base, including face/body/case/grip/head.

Original generated contact soles221/223 were too short. Local80square ankle/boot
repairs admit88,197..168,224:63376outside pixels exact. Far repair reaches224;
near first repair222 retained superseded. Near v2 uses separate red baseline
placement guide, omitted from artwork, reaches224. Final sources near-feet2.png
and contact-far-feet.png; both forward/rear alpha128 foot-region bottoms224.
Helmet counterparts reuse exact new legs and existing master-derived gear base.

Five raw/prompt/input sets and all local/full/detail/station comparisons reviewed,
original/final paired boards reviewed, frozen inventories stable, rasters LFS.
No perpose fit, regrade, mirrored art or body movement. Two contacts are provisional
sources, not full gait/continuous cadence/native/context/owner acceptance. No normal
manifest/actor/save binding changes. Full goal active/incomplete.

Lesson: full thigh-root admission can permit real opposed leg movement; preserve
seam continuity from original hip. Prompted baseline is not measured baseline,
and whole-body bounding box does not prove both feet contact. Check both foot
regions and inspect anatomy after localized generated correction. Exact registered
contact poses do not prove a moving gait: next independent passing/descending/
ascending phases, carrying upper-body dynamics, loop cadence/stride and source
joins, then native room/interruptions/Continue and versioned normal admission.
Continue other cardinals and full-set master/matte/proportion/context polish.
Handoff:character/james-west-carry-gait-master-v2/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':at=old.index(b'### James master-based West cargo contact');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West cargo contacts

## Objective and acceptance
Full master-matched James animation set, then full cross-family polish. Incomplete.

## Accepted decisions and constraints
Master-based West turn endpoint/common256/p128224/body148. Preserve upper body,
face/case/grip/gear density. No perpose fit/grade/mirror/costume reassignment.

## Current state
Two genuine opposed contact drafts after admitting entire upper thighs below
case at y154. Original soles221/223 too short. Final near-feet2.png and
contact-far-feet.png reach224in both foot regions; corresponding -helmet.png.
Original paired boards retained; final paired-fixed-contact-study.png and
opposed-fixed-contact-detail.png reviewed. No full gait bank/manifest/selection.
prepare/package/compare/record helpers, five raw/prompt/input sets retained.
Five guides updated. Normal cap/V9/riseV6/caseV7/save bindings unchanged.

## Verification
All five raws and local/full/detail/station comparisons reviewed. Both original
and fixed paired boards inspected.59376outside-body pixels exact,63376outside
boot repair exact, same paired leg pixels. Five pre-call inventories/source
pair hashes stable; both individual foot-region alpha128 bottoms224. Rasters LFS.
No Godot test/profile changes. No continuous motion/native/cargo room acceptance.

## Next action
Generate true passing poses for both leg ownership phases, then down/up/transition
phases for complete carrying gait. Include believable body dynamics; do not call
static standing frame a passing pose. Review anatomy/boot contact/costume/material,
full cadence/stride and turn/pickup/unload joins. Paired native room/interruptions/
Continue/versioned admission; other cardinals and all-family master/matte polish.

## Source provenance
Builtin near exec-bd4d0d96-ec47-4092-b9ab-b52882b976a2;
far exec-71bf54b6-a4d6-43f4-b0fb-c7c81eac8463;
near first boots exec-c4a0cf85-59cd-4a0d-9a0a-86e22c7a32a8;
far boots exec-8d5b43be-380a-43a8-af5e-73c1007b402f;
near boots v2 exec-4fc75c4d-f8c6-4764-ba18-54cce25ed252.
Saved raw/prompt/input stems contact-near,contact-far,contact-near-feet,
contact-far-feet,near-feet2. Near baseline guide is annotation only, not final art.
''',encoding='utf-8')
print('Five sources reviewed; genuine opposed contacts and both-foot224 geometry checked; five guides/handoff updated. Full goal incomplete.')
