from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
for name in ['passing-near-support','passing-far-support','passing-far-support-v2','far2-feet']:
    inputs=json.loads((p/(name+'-inputs.json')).read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
    f=p/(name+'-review.json');data=json.loads(f.read_bytes());data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition={'passing-near-support':'provisional_near_support_source','passing-far-support':'wrong_swing_direction_master_depth_review_pending','passing-far-support-v2':'rejected_raw_sole229_admission_clips_boot','far2-feet':'rejected_shortening_ignored_sole229'}[name],findings=['Raw/full/detail/station comparisons inspected; upper body/case/head preserved. No complete gait/native/selection.','Near support has gold planted leg and raised plain far foot, raw native sole224 with zero guide pixels/overshoot. Far v1 lifts gold foot backward; raw sole221 is not by itself a defect until far-foot master depth is resolved.','Far v2 moves gold thigh/foot forward but raw sole229 extends154alpha128pixels at/below224; packaged lower admission crops sole. Local repair retains229, rejected. Never certify contact from cropped bounding box.'])
    f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
f=p/'source-study-review.json';data=json.loads(f.read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in data['sourceSha256'].items());data.update(visualReviewPending=False,findings=['Three adjacent source poses and paired helmet/full/detail boards inspected. Near support contributes one genuine lifted-foot pose; not complete loop.','Existing contact sources use common224line. That technical condition is not proof of correct master camera depth; original standing foot planes differ and must be reconciled before gait selection.'])
f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
base=Image.open(p/'base.png').convert('RGBA');samples=[]
for a,b,label in [(100,112,'far-side toe-only columns'),(140,152,'near-side outer sole columns')]:
    box=base.getchannel('A').crop((a,205,b,240)).point(lambda x:255 if x>=128 else 0).getbbox();samples.append({'label':label,'region':[a,205,b,240],'bounds':box,'bottomExclusiveWorld':box[3]+205})
board=Image.new('RGBA',(384,410),(48,59,63,255));board.alpha_composite(base.crop((80,144,176,240)).resize((384,384),Image.Resampling.NEAREST),(0,26));ImageDraw.Draw(board).text((5,7),'Original master-derived legs: camera-depth audit pending',fill='white');board.convert('RGB').save(p/'master-ground-depth.png')
(p/'master-ground-review.json').write_text(json.dumps({'source':'character/james-carry-headcaps-v1/frames/004.png','baseSha256':hashlib.sha256((p/'base.png').read_bytes()).hexdigest(),'samples':samples,'scope':'Limited non-overlapping toe/outer-sole columns: screen-depth difference evidence, not complete anatomical foot isolation. Original whole-foot masks/contact planes still need reconciliation.','decision':'Do not impose common224sole on every support phase. Preserve148standing ruler/pivot independently from visible pose bounds; audit master perspective before more height repair.'},indent=2)+'\n',encoding='utf-8')
section='''### James West passing sources and master foot-depth correction — October 2, 2026

character/james-west-carry-passing-v1: four builtin raw/prompt/input sets reviewed,
all frozen input hashes stable. Near support source has gold leg planted/plain far
foot raised, raw native lowest sole224, no red guide or cropped overshoot. Shared
helmet source reuses same legs; adjacent contact/passing/contact full/detail boards
reviewed, no complete gait or native/normal selection.59376outside lower-body
pixels exact for pose edits. Four source reviews retain sourceAcceptance false.

Far v1 lifts gold foot BACKWARD, not requested forward passing; raw sole221. Far
v2 correctly advances gold thigh but raw sole229 and154alpha128pixels at/below224;
admission crops away boot sole, REJECTED. Uncut reconstruction for local ankle
repair retained whole boot; repair still229, REJECTED.61752outside repair exact
does not establish successful movement. Guide instructions do not prove placement.

Correct prior assumption: master-derived standing feet have screen-depth offset.
Limited disjoint toe/outer-sole columns finish220versus223; these are samples, not
whole anatomical foot masks. Both-foot224checks from previous contact study prove
only that chosen registration condition; they do NOT prove master camera contact.
Do not shrink/extend every support leg until its visible bounds match near sole.
Keep148standing ruler/pivot independent from leg phase and perspective. Raw221
far support is not alone proof of height error. Next map actual original near/far
foot contact planes and reconcile existing contact candidates; then correct far
passing anatomy at its proper plane, complete phase/body dynamics/cadence/joins,
native room/interruptions/Continue/versioned admission and other cardinals/full-set
master/matte/context polish. Normal cap/V9/riseV6/caseV7/save bindings unchanged.
Full goal active/incomplete. Handoff:character/james-west-carry-passing-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':at=old.index(b'### James West cargo opposed contacts');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James passing/foot depth

## Objective and acceptance
Full master-matched James animation set then all-family polish. Active/incomplete.

## Accepted decisions and constraints
Fixed256/p128224/148standing ruler; no perpose fit/regrade/mirror. Perspective
foot depth must follow master; do not force every sole to near-foot224baseline.

## Current state
Near support passing source provisional: gold planted/plain raised, raw224 and
paired helmet plus adjacent contact source filmstrip. Far v1 wrong swing direction;
far v2 correct thigh ownership but raw229, cut package REJECTED; local ankle repair
still229 REJECTED. Four raw/prompt/input sets, helpers and review boards retained.
record_review.py closes sources and updates five guides; master-ground-review.json
records limited disjoint toe/outersole sample depths220/223. No full gait manifest.

## Verification
All four raw/full/detail/station boards and three-source paired/detail boards
reviewed. Inputs stable, source hashes stable,59376outside pose/61752outside ankle
repair exact. Raw-contact-review.json catches154alpha128overshoot pixels for far
v2 before admission; no red guide contamination. No Godot/native/profile changes.
Original master leg/camera foot planes need whole anatomical contact isolation;
limited column sampling is evidence of offset, not final plane measurement.

## Next action
Resolve original master near/far contact-depth offset BEFORE further baseline
repairs. Reconcile previous contact-v2 common224condition as technical-only, not
master perspective acceptance. Then complete correct far passing/phase anatomy,
body dynamics/cadence/stride/joins, paired native room/interruptions/Continue and
versioned normal admission. Other cardinals/full master/matte/context polish.

## Source provenance
Builtin near pass exec-994296a7-5952-4108-a5d5-dc5fc63ec997;
far pass exec-50bee024-22c3-4119-b033-531b94c799d6;
far v2 exec-3f936709-005d-408a-ac82-643e3fe0785b;
far ankle repair exec-b1bc9de4-a468-40e5-b80f-3c9f5e18735c.
Saved stems passing-near-support,passing-far-support,passing-far-support-v2,
far2-feet with raw.png,prompt.txt,inputs.json. All calls terminal, no live jobs.
''',encoding='utf-8')
print('One provisional near passing source, three rejected/pending far sources reviewed; master foot-depth assumption corrected in five guides. Full goal incomplete.')
