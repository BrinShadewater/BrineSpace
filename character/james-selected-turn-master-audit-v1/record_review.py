from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
path=p/'review.json';review=json.loads(path.read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in review['inputSha256'].items())
assert all(v['reverseSourcePixelsExact'] for v in review['states'].values())
assert all(v['distinctRegisteredTurnEndpointImages']==1 for v in review['endpointFamilies'].values())
review.update(visualReviewPending=False,normalSelectionChanged=False,
 reviewedBoards=review['boards']+[v['board'] for v in review['endpointFamilies'].values()],
 reviewedForwardPosePresentations=92,reverseReferenceCoverage=92,
 findings=['All twelve chronological boards/92forward pose presentations inspected with four selected standing idle references, plus eight same-direction endpoint comparison boards/full upper crops. Twelve reverse banks byte-identical in reverse order cover the other92references; not independently watched reverse cadence.',
 'All selected dry turn endpoint variants share one identical registered whole pose per direction/gear. No cross-turn endpoint artwork repair needed from this source audit. Selected carry frame0 is a moving carry phase, not a stationary endpoint; stance differences are deliberate action differences.',
 'Bare crown-to-root diagnostics148..150; helmet150..157. Camera-dependent shell projection contributes to height range, particularly rear vs side/front. No basis for whole-body height normalization. Alpha-crown/head-band/foot union measurements do not certify anatomical proportions.',
 'Helmet SouthWest crowns156,156,154,156,157,156 and EastWest156,155,155,156,156,156,156,154,156,157,156 expose local dips/rebounds requiring enlarged collar/shell/source cadence comparison. NorthSouth150..156 rotation trend must be distinguished from vertical bob.',
 'Matte dark fabric/yellow material broadly consistent on these full-size source boards; no blanket regrade selected. South legs retain planted turn stance; exact skeletal contact/continuous native motion remains unproven.',
 'Original master source lineage beyond selected canonical idles, unrelated actions, natural game cadence, actual native renderer/room contexts and full-set acceptance remain outside this audit.'],
 next='Build enlarged registered shell/collar comparisons of SouthWest rows1-4 and EastWest rows5-9 beside shared angular helmet sources and canonical shells. Decide whether variation is camera projection, shell placement or shape drift before authoring coherent source repair. Retain normal V9 return bridge as separate unresolved join.')
atomic(path,(json.dumps(review,indent=2)+'\n').encode())
section='''### James selected dry-turn master comparison — October 2, 2026

Read actual grid_canvas literal James load order, including later compact East
head overrides; resolve12dry turn states per gear/184frame references. Register
each original image by declared pivot onto256/p128224/H148, no resize/grade/pose
fit. All twelve chronological boards/92forward pose presentations and eight
same-direction whole/upper endpoint boards inspected beside selected standing
idles. Twelve reverse banks byte-identical reversed cover other92references;
not independently watched reverse cadence. Targeted input hashes unchanged.

All turn endpoints share ONE exact registered whole image per direction/gear.
No cross-turn endpoint artwork divergence here. Selected carry frame0 is a walking
carry phase, not stationary turn endpoint; do not force its stride stance onto turns.
Bare alpha32 crown-root148..150; helmet150..157 includes camera shell projection,
not anatomical height proof. SouthWest helmet156,156,154,156,157,156 and EastWest
local154dip/rebound need enlarged shell/collar/cadence audit. Rear-side rotation
trend differs from body bob; do not normalize entire bodies to helmet crown bounds.
Matte grade broadly consistent in these source boards; no blanket regrade chosen.

Lesson: read final runtime override order, then compare whole endpoints across
families before regenerating joins. Separate action stance, shell projection and
anatomical scale. Byte-identical reverse sources can reuse source review but do
not prove reverse cadence/native behavior. Next targeted enlarged helmet dip
diagnosis, while West return join and other contexts/full cross-family polish stay
open. No selection/code/source change, generation spend, owner profile access or
full-goal acceptance. Original master lineage/native/continuous playback pending.
Evidence: character/james-selected-turn-master-audit-v1/review.json and20boards.
Five maintained guides updated; full goal active/incomplete.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James whole endpoint atlas source gate');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James turn consistency

## Objective and acceptance
Complete James set matching masters/style/camera/height/proportions/matte grade,
then full cross-family polish. Incomplete; normal V9/riseV6/caseV7 retained.

## Accepted decisions and constraints
Follow actual final load order and declared registration. Separate walking stance
from planted turns, shell projection from anatomical scale. No wholebody fitting.

## Current state
character/james-selected-turn-master-audit-v1: builder,20boards,review/record scripts.
Actual12dryturns per gear/184references and selected four-direction idle/carry0.
Prior endpoint atlas and coherent video rejected for bridge replacement.
Five maintained guides updated; normal code/art unchanged.

## Verification
All12chronological boards/92forward presentations and8endpoint/detail boards
inspected.12reverse banks exact reversed bytes cover92more references. Targeted
hashes unchanged; all direction/gear turn endpoints identical across families.
Bare crown148..150, helmet150..157 are diagnostics, not anatomy proof. Local
SouthWest/EastWest shell dips remain. No continuous/native/owner acceptance claim,
original master lineage/full-set context pending. No owner profile access/spend.

## Next action
Enlarge registered SouthWest helmet rows1-4 and EastWest5-9 with shared shell
sources/collars, identify projection vs placement vs shape drift, then repair
coherent sources if needed. West cargo return and other contexts/master/cross-
family polish remain. Goal active/incomplete; no blocker or live provider job.
'''
atomic(p/'HANDOFF.md',handoff.encode()) if (p/'HANDOFF.md').exists() else (p/'HANDOFF.md').write_text(handoff)
print(json.dumps({'reviewedBoards':len(review['reviewedBoards']),'references':184,'inputHashes':len(review['inputSha256']),'allReverseBanksExact':True,'allTurnEndpointsShared':True,'guidesUpdated':5}))
