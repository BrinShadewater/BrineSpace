import hashlib,json,os,subprocess,uuid
from pathlib import Path
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
def atomic(path,data):
    t=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,path)
def write(path,data):atomic(path,(json.dumps(data,indent=2)+'\n').encode())
guards={}
for name in ['validate','compatibility']:
    d=json.loads((P/f'{name}-validation.json').read_bytes())
    assert d['exitCode']==0 and not d['timedOut'] and d['realProfileUnchanged'] and d['profileDelta']==[]
    guards[name]=d
source=json.loads((P/'source-evidence.json').read_bytes())
assert source['references']==448 and source['maximumWorldError']<.8
outputs=[P/'torch-tip-offsets.json',P/'source-evidence.json']+list(P.glob('source-page*.png'))
before={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in outputs}
subprocess.run(['C:/Python314/python.exe',str(P/'build.py')],cwd=R,check=True,stdout=subprocess.DEVNULL)
after={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in outputs}
assert before==after
native=json.loads((P/'native-evidence.json').read_bytes());assert native['failures']==0 and native['actualPaidComplete']
review={'status':'installed_repair_effect_contact_verified_owner_review_pending','runtimeInstalled':True,'fullSetComplete':False,'newDrawings':0,'newSourceStates':0,
        'native':native,'profileGuards':guards,'compatibilityChecks':8,
        'sourceReferences':448,'maximumWorldError':source['maximumWorldError'],'minimumOldWorldError':source['minimumOldWorldError'],
        'deterministicRebuild':{'files':len(outputs),'byteIdentical':True,'hashes':after},
        'runtimeHash':hashlib.sha256((R/'scripts/station_effects.gd').read_bytes()).hexdigest(),
        'visualReview':'All448 unchanged selected work refs across8source boards; all16 native before/corrected views at148/82/54/27 and all27 actual North held-source views reviewed. Matte source grade/body/rulers retained. Warm repair spark overlay now coincides with cyan flame. Fixed measured viewport crop486,362; raw fixture footViewport estimate is incorrect and unused.',
        'diagnostics':'Initial naive source-unit board and initial native interval retained. First native pass exposed double-added deck lift; final physical-foot transform subtracts/adds .038 only through existing getter/renderer. Generic-source flame segmentation also selected cyan helmet visor; final paired bare flame masks bound that region. before-render-transform-fix is superseded, not final acceptance.',
        'remaining':'Hull repair presently jumps directly into/out of held weld. Complete tool entry/finish and actual interruption/Continue lifecycle, broader natural facings/equipment/furniture/rotation/owner/export polish. Full goal active.'}
write(P/'selection-review.json',review)
parent=R/'character/james-torch-material-residue-v2/selection.json';d=json.loads(parent.read_bytes());d['repairContactReview']='res://character/james-repair-contact-v1/selection-review.json';write(parent,d)
block='''## James repair flame contact — October 1, 2026

Installed James-specific measured flame offsets in station_effects.gd via the
whole literal character/james-repair-contact-v1/torch-tip-offsets.json path.
All448 paired selected held torch refs remain immutable; no drawings or states
added. Shared construction_door override remains the doorway; hull seam vapor
and ordinary repair sparks use corrected torch contact. Bill measured points
and other actors' generic fallback pass8compatibility checks unchanged.

Physical foot is the rendered pivot: main subtracts .038cells and renderer adds
it back. Convert source displacement through384*.17/148 with no additional lift.
Initial native comparison caught double-added lift, superseded by final run.
Do not average cyan helmet glass into flame contact; bound to the paired bare
source's flame mask. Fixed directional means stay within .779world units of all
448flame centroids; old generic anchors miss by at least18.502world units.
10measurement/board files rebuild byte-identically; source PNG hashes frozen.

Final6567native checks/0failures: selected whole pixels/rulers/effects at four
sizes, one actual paid hull request with natural North anchor/facing,27held
source views, fixed work foot, completion once/no second charge. All448source
refs on8boards,16prescribed before/corrected bare/helmet comparisons at148/82/
54/27 and27actual North views reviewed. Helmet held weld comparisons do not
prove natural helmet hull eligibility. Both final native intervals engine0,
no timeout/strict owner profile unchanged/scratch APPDATA. Initial native pass
and bad crop estimates retained as diagnostic data; final fixed screenshot
crop486,362, no per-pose scale/recentering. Source matte identity/height unchanged.

Hull repair currently jumps into/out of held weld; tool entry/finish and actual
interruption/Continue are next. Other natural facings, broader gear/furniture/
rotation and owner/export polish remain. Full animation goal active/incomplete.
Evidence/HANDOFF:character/james-repair-contact-v1.

'''
guides=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,path in enumerate(guides):
    old=path.read_bytes()
    if block.splitlines()[0].encode() in old:continue
    b=block.encode();atomic(path,b+old if i==0 else old+b'\n'+b.rstrip()+b'\n')
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James repair flame contact

## Objective and acceptance
Full matching animation set and cross-family consistency/polish. Active and
incomplete. Current contact correction installed/native reviewed, owner pending.

## Accepted decisions and constraints
Selected matte whole sources,148ruler/p92,172, forward torch, belt wrench and
fixed work feet. Construction targets shared doorway by owner decision. Existing
repair costs/safety/eligibility retained. Preserve concurrent actor work; scratch
APPDATA only, owner profile fingerprint before/after every native interval.

## Current state
station_effects.gd: James-specific measured offsets; source selection unchanged.
New measurement/review helpers, paired native fixtures/UIDs, contact JSON and
hash/evidence/boards. Parent torch selection and five guides updated. No new art
or state coverage. before-render-transform-fix archived diagnostic run; raw
fixture footViewport estimate double-stretches coordinates and is not evidence.
Fixed actual screenshot foot486,362 is used for all27 reviewed source crops.

## Verification
6567native checks/0failures;8Bill/peer compatibility checks/0failures. Final two
intervals engine0/no timeout/strict owner unchanged.448selected sources match
native pixels/rulers; four render sizes measured. Max flame error .779worldunits;
old minimum miss18.502.10measurement/board files byte-identical rebuild.
All448refs/eight boards,16before/corrected native views and27real paid North
held views reviewed. Genuine core release/normal hull request/normal controller
approach and work; fixed contact/completion once/no extra charge. Prescribed
helmet work only; not natural eligibility/allfacing hull routing/Continue.

## Next action
Complete hull repair tool draw/finish using exact selected sources and normal
paid work/safety; actual interruptions and fresh Continue. Current controller
enters held weld directly and releases straight to idle. Then broader natural
facings/gear/furniture/rotations and full-family owner/export consistency polish.
Do not treat source coverage or bounded effect checks as full-set completion.
'''
atomic(P/'HANDOFF.md',handoff.encode())
print('Recorded installed repair-contact milestone, rebuild proof and five guides.')
