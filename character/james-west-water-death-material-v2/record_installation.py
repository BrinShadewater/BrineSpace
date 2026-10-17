from pathlib import Path
import json,hashlib,os,uuid
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];OLD=P.parent/'james-west-water-death-polish-v1'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,b):
 t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(b);os.replace(t,p)
def write(p,v):atomic(p,(json.dumps(v,indent=2)+'\n').encode())
guards={}
for n,count in [('native-staged-behaviour',72),('native-installed',62),('native-installed-behaviour',71),('native-restore',52)]:
 g=read(P/(n+'-validation.json'));assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and not g['profileDelta'];assert not any(t in (P/(n+'.log')).read_text() for t in ['ERROR:','SCRIPT ERROR:']);assert (P/(n+'.gd.uid')).exists();guards[n]={k:g[k] for k in ['exitCode','timedOut','realProfileUnchanged','profileDelta']}
assert read(P/'package-verification.json')['checks']==82
before=read(P/'source-inputs-before.json');after={f:sha(R/f) for f in before};assert before==after;write(P/'source-inputs-after.json',after)
for mode in ['bare','helmet']:
 old=read(OLD/(mode+'-manifest.json'));new=read(P/(mode+'-manifest.json'));a=old['states'][0];b=new['states'][0]
 assert {k:v for k,v in a.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in b.items() if k not in ['frameFiles','provenance']}
 assert {k:v for k,v in old.items() if k not in ['name','status','states']}=={k:v for k,v in new.items() if k not in ['name','status','states']}
original=(P/'grid_canvas-before-install.gd.txt').read_bytes();expected=original
for mode in ['bare','helmet']:expected=expected.replace(f'res://character/{OLD.name}/{mode}-manifest.json'.encode(),f'res://character/{P.name}/{mode}-manifest.json'.encode())
assert (R/'scripts/grid_canvas.gd').read_bytes()==expected
original=read(P/'ACTIVE_ASSETS-before-install.json');expected=json.loads(json.dumps(original))
for field,mode in [('actionOverrides','bare'),('equipmentActionOverrides','helmet')]:expected[field]['branforth-west-water-death-polish']=f'character/{P.name}/{mode}-manifest.json'
assert read(R/'character/ACTIVE_ASSETS.json')==expected
cov=read(R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json')
for mode,gear in [('bare','body'),('helmet','equipment')]:assert cov[gear]['death-water-west']['path']==f'character/{P.name}/{mode}-manifest.json'
write(P/'generation-evidence.json',{'method':'Two built-in image_gen edits, exact prompt files retained; neither selected for runtime.','attempts':[{'output':'rejected-frame-edit.png','prompt':'frame-edit-prompt.txt','sha256':sha(P/'rejected-frame-edit.png'),'originalSize':[256,360],'outputSize':list(Image.open(P/'rejected-frame-edit.png').size),'originalOpaqueBounds':[81,197,200,252],'outputOpaqueBounds':[346,857,814,1070],'decision':'Rejected: resized/repositioned silhouette, unsuitable for a colour-only replacement.'},{'output':'unselected-atlas-edit.png','prompt':'atlas-edit-prompt.txt','sha256':sha(P/'unselected-atlas-edit.png'),'size':list(Image.open(P/'unselected-atlas-edit.png').size),'changedAlphaPixels':77857,'decision':'Unselected: original alpha not retained; native source-builder curve preserves geometry exactly.'}],'runtimePixelSource':'Existing installed12PNGs; one fixed native material curve only.','billing':None})
sel=read(P/'selection.json');sel.update(packageChecks=82,stagedMortalityChecks=72,installedPlayerChecks=62,installedMortalityChecks=71,diskRestoreChecks=52,guards=guards,productionInputsUnchanged=15,sourceReview='All6paired before/after poses, browser source replay entry/terminal beside West masters, all12staged+12installed mortality captures and2restored terminals inspected.',nativeLightingLimit='Flooded native room captures are heavily blue/dim; original-source boards support material comparison. Source replay is separate from continuous native footage.',pending=['Remaining furniture/exterior journeys and full-motion family consistency','Owner and full-set acceptance']);write(P/'selection.json',sel)
q=R/'character/james-water-motion-review-2026-10-01/selection-review.json';v=read(q);v['materialRevision']='character/james-west-water-death-material-v2/selection.json';v['materialRevisionStatus']='Selected native material curve; reviewed scopes and owner-pending status are in linked revision. Original mismatch report remains historical.';write(q,v)
note='''## James West water-death material correction selected — October 1, 2026

Selected paired james-west-water-death-material-v2 reduces bright/pink knee/boot
hardware through one fixed native source-builder highlight curve, shared across
all10interiors. Values below50, gold/skin outside neutral mask, head/shared-helmet
edit regions, all alpha/silhouette/pivots and exact swim-entry RGBA are retained.
Original source geometry, compact boot reach and2000ms finite clock unchanged.
Broad neutral mask can include gloves/boots/hardware; this is not semantic knee-only
grading or regenerated anatomy. RearROI P90RGB112.4/102.3/102.3 ->101.9/93.1/92.3,
closer to selected swim100.2/91.9/89.8; mean>100 fraction.118 ->.088 vs swim.077.

82package,72staged mortality,62installed source-clock,71installed mortality and52
disk-restore checks pass. Allfour engines terminal0/no timeout/clean logs; strict
owner profile unchanged. All6paired old/new source poses and24staged/installed
native mortality captures plus2restored terminals inspected; browser source GIF
observed entry/terminal beside West masters. Flooded native views are heavily blue/
dim, so source boards establish grade. Native fixtures use prescribed clear room
nodes and direct RoomFlooding.kill, not natural oxygen/exterior journeys. Four real
scratch disk restores cover mid3/terminal5 in both gears, exact pixels/clock/pause.

15original source inputs unchanged. Production diff: two literal selected loader
paths and their two existing registry entries only. Current inventory refreshed,
337bare/4280slots,247helmet/3764slots; no added states. Two built-in image edits
are saved with prompts but unselected: singleframe changed placement/canvas,
atlas changed77857alpha pixels. Existing source-builder curve retains all geometry.
Evidence/HANDOFF:character/james-west-water-death-material-v2. Source material
revision reviewed, owner/full-set acceptance remain open. Next full furniture/
exterior journeys and remaining motion/cross-family checks.

'''
q=R/'docs/CURRENT_STATUS.md';atomic(q,note.encode()+q.read_bytes())
lesson='''
## James West water-death material curve — October 1, 2026

The old source-grade neutral gain1.3889 amplified already bright hardware. A fixed
native source-builder highlight compression, shared across every interior/gear,
keeps low values, protected head/helmet regions, non-neutral gold/skin, alpha and
geometry exact while reducing bright pink/grey spots. Existing exact swim entry
remains untouched; finite clock/pivots/compact anatomy retained. Do not fit exposure
per frame or replace accepted anatomy to solve grade. Broad neutral masks can include
gloves/boots/hardware and are not semantic region labels. Source P90rear diagnostic
112.4/102.3/102.3 ->101.9/93.1/92.3, near swim100.2/91.9/89.8, supports visible change
but cannot certify material or world lighting independently.

Two built-in image edits were retained with exact prompts but not selected: first
changed canvas/placement, second changed77857alpha pixels. Generated material edits
must pass geometry/alpha/identity constraints before replacement. Here native source
builder calibration preserves12original alpha/silhouettes, exact entries and shared
helmet ownership. Production selection changes only two literal loader paths and
two existing registry values.15source inputs unchanged.

82package/72staged/62installed-clock/71mortality/52disk-restore checks pass; allfour
engines terminal0/clean logs/strict owner profiles unchanged. All6paired poses,
24mortality snapshots and2restored terminals reviewed; source GIF entry/terminal
observed beside masters. Dark blue flooded snapshots support pose/room contact;
source boards establish material comparison, not continuous native cadence. Direct
RoomFlooding.kill at prescribed clear nodes and same-process scratch disk restores
do not prove natural oxygen/exterior journeys. Evidence:
character/james-west-water-death-material-v2. Full James goal/owner acceptance open.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:atomic(q,q.read_bytes()+lesson.encode())
handoff='''# Project handoff

Updated:October1,2026 · Project:Brine Space · Task:James West water-death material

## Objective and acceptance
Full James set/master/style/perspective/size/proportions/grade, then family polish.
Previous turn was progress:108water poses reviewed and material mismatch identified.
This turn selects a checked correction; full-set/owner acceptance still open.

## Accepted decisions and constraints
Matte graphite/ochre, exact swim entry, compact limbs, original alpha/pivots/148ruler,
shared helmet,2000ms finite clock. Scratch APPDATA/strict owner fingerprint guard.

## Current state
New native source-builder curve and12derived PNGs, paired manifests, reproducible
review/verify/install/record helpers, four native scripts with pairedUIDs, all reports.
Two literal loader paths in grid_canvas.gd and two existing ACTIVE_ASSETS entries
select this revision. Current coverage337bare/4280slots,247helmet/3764slots unchanged.
Five guidance docs updated, prior mismatch review linked. Two imagegen candidates
and exact prompts saved but unselected. Original15source inputs unchanged.

## Verification
82package/72staged/62installed-clock/71mortality/52disk-restore checks PASS.
Allfour exactsessions57121/65367/89111/86766 terminal0/no timeout/clean logs,
strict owner profiles unchanged.12source alpha/silhouettes/exactentry preserved,
head regions/non-mask pixels unchanged, shared body outside helmet exact. Complete
state/header metadata unchanged except paths/provenance/name/status. All6paired
source poses,12staged+12installed mortality captures and2restored terminals inspected.
Browser observed source GIF entry/terminal beside West masters. Flooded native views
blue/dim; source boards establish grade, not continuous native-motion certification.
Directkill clear-node setup, four same-process diskrestore phases3/5bothgears only;
not natural oxygen, exterior journeys, all layouts or owner/full-set acceptance.

## Next action
Continue full furniture/exterior journeys and remaining full-motion/master-family
comparisons. Source-preview loopback server90906/8796 is still available; browsertab1
shows candidate-material.html. Generated candidates need no further integration.
'''
atomic(P/'HANDOFF.md',handoff.encode())
print(json.dumps({'packageChecks':82,'nativeChecks':257,'ownerGuards':'all unchanged','selectedMaterialRevision':P.name,'fullGoalComplete':False}))
