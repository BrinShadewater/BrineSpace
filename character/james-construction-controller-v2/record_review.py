from pathlib import Path
import json, os, uuid, hashlib
P=Path(__file__).resolve().parent; R=P.parents[1]
n=json.loads((P/'validate-evidence.json').read_text())
v=json.loads((P/'validate-validation.json').read_text())
review=json.loads((P/'review-evidence.json').read_text())
assert n['failures']==0 and v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged']
assert len(n['cases'])==4 and all(c['completed'] for c in n['cases'])
assert len(review['boards'])==9 and review['uniqueWorkCaptures']==347
def atomic(path,data):
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp'); tmp.write_bytes(data); os.replace(tmp,path)
result={'status':'actual_paid_construction_reviewed_owner_pending','fullSetComplete':False,'runtimeChanges':False,'nativeChecks':n['checks'],'failures':0,'cases':n['cases'],'uniqueWorkCaptures':347,'allCaptures':sum(c['captures'] for c in n['cases']),'sourceTransitions':len(n['records']),'profileGuard':v,'visualReview':'All347 distinct torch work captures reviewed on nine fixed viewport boards: coherent matte material, planted feet, stable apparent standing height, belt tools and forward-facing torch. Doorway overlay intentionally differs from PNG flame position. All approach sources were captured, but not exhaustively visually reviewed here.','scope':n['scope'],'remaining':['Actual power/door interruption and fresh Continue during construction phases','Repair versus construction overlay/contact contexts','Broader cross-family motion, gear/furniture rotations, owner and export acceptance']}
result['reviewBoards']=[{'path':f,'sha256':hashlib.sha256((P/f).read_bytes()).hexdigest()} for f in review['boards']]
atomic(P/'selection-review.json',(json.dumps(result,indent=2)+'\n').encode())
selected=R/'character/james-torch-material-residue-v2/selection.json'
s=json.loads(selected.read_text());s['actualConstructionReview']={'path':'character/james-construction-controller-v2/selection-review.json','bareCardinals':4,'nativeChecks':n['checks'],'workCapturesReviewed':347,'ownerAccepted':False}
s['remaining']=['Actual construction interruption and fresh Continue; repair effect/contact contexts','Other families/cardinals/rotations/gear/travel contexts','Full James consistency, owner and export acceptance']
atomic(selected,(json.dumps(s,indent=2)+'\n').encode())
block='''## James actual paid construction torch review — October 1, 2026

character/james-construction-controller-v2 verifies four actual paid life-support
jobs, genuine James core release, normal game updates at 60Hz and real navigation,
draw/held/stow/completion. Each spends5metal, places the paid room and releases its
reservation. Work feet remain planted/standable; facing matches the connection;
snapshots admit; sparks exist only in held welding and target the actual doorway.
12654checks/0failures, engine0/no timeout, scratch APPDATA, strict owner unchanged.
657native captures/1940source transitions; all347 distinct torch-work captures
reviewed on nine fixed viewport boards. Matte material and apparent standing
height remain coherent at station scale. No runtime or artwork change needed.

Construction deliberately welds the shared doorway, per owner decision; repairs
use torch-tip offsets. An orderless prescribed construction pose falls back to
the torch tip and cannot establish real construction overlay placement. The
South doorway projects near the boots; that effect is separate from sprite color.
Actual construction admits bare crew, so helmet library views do not establish
helmet construction eligibility. Keep those claims separate. Work-clock GIFs use
actual recorded source intervals but reuse first captures for repeated sources;
they do not continuously record spark flicker. Approach captures exist but were
not exhaustively visually reviewed. Initial fixture reservation-method error
archived before correction; no gameplay regression or runtime fix inferred.

Next actual construction interruptions/fresh Continue, repair effect/contact,
broader family/gear/furniture/rotation motion and owner/export acceptance. Full
James goal remains active/incomplete. Handoff: this review folder/HANDOFF.md.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,path in enumerate(paths):
    old=path.read_bytes();new=block.encode();assert new not in old
    atomic(path,new+old if i==0 else old+b'\n\n'+new)
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James construction controller review

## Objective and acceptance
Full James animation set matching masters and consistent across families. Goal
active/incomplete; this actual construction review is verified, owner pending.

## Accepted decisions and constraints
Matte material, fixed148 standing ruler, stable anatomy, forward torch and belt
wrench. Construction sparks land at doorway; repair sparks use torch tip. Normal
construction admits bare crew. Preserve original motion and concurrent changes.

## Current state
New validate.gd/.uid and build_review.py/record_review.py, native captures,
evidence, nine reviewed boards/four work-clock GIFs and selection-review.json.
Existing material selection gains this scoped proof; five guides updated. No
gameplay or art changes. Initial fixture method error retained separately.

## Verification
Four paid jobs through normal60Hz game updates;12654checks/0failures;657captures,
1940source transitions, all347 distinct work poses visually reviewed. Each job
spends5metal, completes placement and releases reservation. Engine0/no timeout;
scratch APPDATA and strict real owner profile unchanged. Work-clock GIF repeats
first native lighting/spark captures per source; not a continuous gameplay video.
No helmet eligibility, interrupted/Continue job or full approach visual claim.

## Next action
Actual construction power/door interruptions and fresh disk Continue in each
torch phase; repair overlay/contact, broader family/gear/furniture/rotation
consistency and owner/export acceptance. No native/provider process from this
review remains running. Previous accepted art and all other actors preserved.
'''
atomic(P/'HANDOFF.md',handoff.encode())
print(json.dumps({'checks':n['checks'],'failures':0,'reviewedWorkCaptures':347,'guidesUpdated':5,'runtimeChanges':False}))
