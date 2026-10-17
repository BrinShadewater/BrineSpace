from pathlib import Path
from PIL import Image
import hashlib,json,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def stable(data,key):assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in data[key].items())
for name in ['far-support','walk12-carry']:
    stable(json.loads((p/(name+'-inputs.json')).read_bytes()),'preCallSha256')
    f=p/(name+'-review.json');data=json.loads(f.read_bytes());data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='rejected_working_far_contact_overshoot' if name=='far-support' else 'provisional_master_walk_local_carry',findings=(['Whole far-leg redraw improves original229sole to225but misses workingfar221. Raw/full/detail/station reviewed; no baseline clipping because admission extends240.','Detailed master confirms staggered foot depth;221/224are working guide levels, not universal moving plane/complete segmentation. No more blind both-feet224repair.'] if name=='far-support' else ['Raw/full/detail/station and master-carry/actual-walk comparison inspected. New two-handed case held in front, original hanging hand removed, retained clothing/gear broadly coherent.','60466outside upper-body pixels exact. All head pixels above104and legs below169exact to actual selected walk12; hip/upper thigh inside local region may change, not entire leg-pixel claim.','One frame only; tool identity/occlusion and case grip need whole-cycle/join review. No native/full gait/owner acceptance.']))
    f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
f=p/'walk-donor-inputs.json';data=json.loads(f.read_bytes());stable(data,'sourceSha256');data.update(visualReviewPending=False,framesReviewed=49,disposition='source_family_compatible_donor_candidate',findings=['All49normal walk source chronology and five representative master-carry comparisons inspected at same148ruler/pivottranslation. Face/body/material broadly same family.','Selected source is not proof of full gait quality; near/far alternation, heavy-case stride/body dynamics and continuous motion remain to audit before carrying admission.']);f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
f=p/'carrying-family-review.json';data=json.loads(f.read_bytes());stable(data,'sourceSha256');assert data['donorBounds']==data['carryingBounds'];data.update(visualReviewPending=False,disposition='provisional_local_carry_source',findings=['Full/upper comparisons of master carry, originalwalk12 and editedwalk12 reviewed. Same donor head/leg silhouettes and source ruler; case in front and two-hand grip.','Donor225sole also edited225: retained actual walk phase geometry, not a new frame height shift. No fit/regrade/leg redraw.','Case scale/grip/tool visibility and movement need full-cycle and actual pickup/turn/unload joins; no temporal/normal acceptance.']);f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
raw=Image.open(p/'far-support-native-crop.png').convert('RGBA');box=raw.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox();below=sum(v>=128 for v in raw.getchannel('A').crop((0,77,96,96)).get_flattened_data());rgba=raw.get_flattened_data();red=sum(a>=128 and rr>150 and rr>g*1.8 and rr>b*1.8 for rr,g,b,a in rgba);green=sum(a>=128 and g>150 and g>rr*1.8 and g>b*1.8 for rr,g,b,a in raw.get_flattened_data())
(p/'raw-support-review.json').write_text(json.dumps({'nativeBounds':box,'worldBottomExclusive':box[3]+144,'alpha128PixelsAtOrBelowWorkingFar221':below,'redGuidePixels':red,'greenGuidePixels':green,'admissionBottom':240,'scope':'Raw full generated leg geometry, not trimmed to working baseline; contact remains unresolved.'},indent=2)+'\n',encoding='utf-8')
section='''### James West carrying gait from the selected master walk — October 2, 2026

character/james-west-carry-depth-v1 compares detailed original West master boots
and unchanged master-derived standing legs. Staggered soles are visually real;
isolated runtime samples220/223corroborate depth, working whole-foot guides221/224
remain provisional. Whole far-leg joint-guided redraw improves229sole to225but
misses workingfar221, REJECTED. Admission extends240so no boot clipping can fake
contact. Master depth remains input to anatomy, not forced bbox normalization.

Ordered literal normal walk-west source is crew-runtime-matte-v1/branforth/
manifest.json,49frames. Complete chronology and five representative same-ruler
comparisons reviewed: head/body/material broadly master-compatible. Source reuse
is candidate-only; selection does not prove gait alternation/heavy-case dynamics.
Local generated two-handed case edit on actual walk12 is promising:60466outside
upper-body pixels exact, head above104and legs below169exact. Hip/upper thigh
within88,104..166,169may change. Donor and edited bounds both87,76..174,225;
no new height change, perpose fit, leg redraw or regrade. Raw/local/full/detail/
station and carrying-family comparisons reviewed, source inventories stable.

Both raw/prompt pairs retained. New walk12carry is provisional/unselected,
sourceAcceptance false; no full gait bank/native/normal/save binding change.
Lesson: cross-reference existing master-compatible motion before repeatedly
redrawing legs. An isolated arm/case edit can preserve source dynamics and head
identity while source-family consistency remains explicit. Carry grip/case size,
tool continuity, limb alternation and whole-cycle rhythm still need evidence.
Next audit donor limb ownership/body/stride, produce representative opposite and
passing carrying upper sources, build full coherent paired gait, review cadence/
actual turn-pickup-unload/room/interruptions/Continue/versioned admission. Other
cardinals/full-set master/matte/proportion/context polish remain. Full goal active.
Handoff:character/james-west-carry-depth-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':at=old.index(b'### James West passing sources');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: master walk -> carrying

## Objective and acceptance
Full master-matched James animations then full cross-family polish. Incomplete.

## Accepted decisions and constraints
Fixed source density/ruler/pivot; no perpose fit/grade/mirror. Original foot depth
is staggered; working221/224guides not universal moving-foot plane. Preserve normal
cap/V9/riseV6/caseV7/save bindings and other actor work.

## Current state
Detailed original/runtime master feet comparison, one whole far-leg redraw still
too long225workingfar221(REJECTED). Literal selected normal walk-west49sources
and chronology inspected. New walk12-carry.png generated local upper-body edit:
60466outside exact, head above104and legs below169retained. Promising provisional
two-hand case pose. Hip/thigh inside169band may change. No full gait manifest.
prepare/package/audit/compare/record helpers, all raws/prompts/inventories/boards
retained; five guides updated. No runtime source replacement or profile changes.

## Verification
Detailed feet and raw/local/full/detail/station boards reviewed for both generated
sources. All49walk chronology plus five representative whole comparisons and
three-way carrying-family full/upper boards inspected. Frozen hashes stable;
donor/editedwalk12bounds exactly87,76..174,225. No native/continuous gait/room/
owner approval. Normal selection alone does not prove alternation/stride quality.

## Next action
Audit donor limb ownership/actual stride/body dynamics first; inspect crop seams
and belt tools. Generate carrying upper edits for representative opposite contact
and passing phases; assemble complete coherent paired gait without inventing
transforms or accepting source selection as gait proof. Review cadence and
turn/pickup/unload/room/interruptions/Continue; versioned normal admission.
Other cardinals and full master/matte/proportion/context consistency pass.

## Source provenance
Builtin far leg exec-bea5e8fc-7b0e-4402-8d5a-f54bbd5ca8c6 rejected;
walk12carry exec-cfaf131a-3eca-4a54-a396-7148d598370b provisional.
Saved far-support-raw.png/prompt.txt/inputs.json and
walk12-carry-raw.png/prompt.txt/inputs.json. All generation calls terminal.
''',encoding='utf-8')
print('Master depth evidence and49walk sources reviewed; one local carrying walk prototype; five guides/handoff updated. Full goal incomplete.')
