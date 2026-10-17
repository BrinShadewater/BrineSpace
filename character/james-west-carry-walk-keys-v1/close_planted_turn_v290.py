from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
import numpy as np
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-refine-v290';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();d=json.loads((o/'inputs.json').read_bytes());f=json.loads((o/'native-inputs.json').read_bytes());v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());m=json.loads((o/'registration-diagnostic.json').read_bytes())
assert all(sha(r/x)==h for x,h in d['referenceSha256'].items()) and sha(o/'prompt.txt')==d['promptSha256'] and sha(r/d['sourceFile'])==d['sourceSha256']
assert all(sha(r/x)==h for x,h in f['preLaunchSha256'].items())
assert (n['checks'],n['failures'],n['captures'])==(22,0,1)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
a=np.asarray(Image.open(r/d['sourceFile']).convert('RGBA'))[:,:,3]>=128;b=np.asarray(Image.open(o/'fixed-canvas-source.png').convert('RGBA'))[:,:,3]>=128;iou=float((a&b).sum()/(a|b).sum());report=dict(disposition='provisional_single_bare_planted_turn_source',rawVisuallyReviewed=True,sourceBoardReviewed=True,nativeBoardReviewed=True,nativeChecks=22,nativeFailures=0,nativeCaptures=1,geometry=m['rows'],alpha128SilhouetteIoU=iou,silhouetteExact=False,sourceAcceptance=False,selected=False,normalChanged=False,fullGoalComplete=False,findings=['Existing planted pose anchor preserves gross registration: original148high/crown77/sole224, candidate149/crown76/sole224. One global1254to256 canvas resize; no body-fit or pose translation.', 'Fine quilt and restrained charcoal surface detail closer to original master; raw and native148/82/54/27 comparisons reviewed. Equipment remains on belt and case held; exact hardware/detail/case identity still needs sequence-wide review.', 'Whole raw generated silhouette is not byte-exact: same horizontal bounds do not prove same anatomy. Bare single source only; no helmet, full turn, endpoint joins, moving contacts or ordinary arrival integration.'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n');(o/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='a0c7eb89-2d8a-450d-b612-570883b4efc9',method='builtin_imagegen_registered_planted_turn_geometry_target',rawSha256=sha(o/'raw.png'),prompt='prompt.txt',disposition=report['disposition']),indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old);j['arrivalTurnSourceStudy']=dict(version=290,bareFile=(o/'fixed-canvas-source.png').relative_to(r).as_posix(),sha256=sha(o/'fixed-canvas-source.png'),selected=False,sourceAcceptance=False);j['nextVisualRepair']='V290 one bare planted-turn source149px at originalsole224, fine quilting closer to master. Extend consistent geometry-anchored turn sequence and exact carry/unload endpoint joins, inspect case/belt/hardware/anatomy/grade before shared helmet/actual arrival integration. Stance/root contact and normal lifecycle/all-family polish remain.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James planted turn geometry anchor yields provisional source - October3,2026

V290 builtin edit uses existing west-north turn3 as geometry target and original
West master as appearance reference. Raw1254 globally resized to256 once, no
body-fit/translation. Original148/crown77/sole224, candidate149/crown76/sole224;
same horizontal bounds89..156. Finer flat cloth detail/matte surface closer to
master; raw/master-source and native148/82/54/27boards inspected. Entire generated
silhouette is NOT byte-exact; extent agreement alone does not certify anatomy.
Single bare static provisional source, not full turn or final master acceptance.

22native checks0/1comparison capture (3bare source rows,4sizes), scratch owner
unchanged; source/prompt/reference/runtime hashes stable. No helmet, full chronology,
exact endpoint join, moving contact or ordinary arrival proved. Case/belt/hardware
and original-master grade/proportions still need sequence-wide review. Normal bank
unchanged. Previous288/289 rejected trials retained.

Lesson: an already registered planted pose anchors generation better than asking
for a whole turn from cardinal appearance references with placement numbers.
Validate raw/full-source geometry and equipment before creating helmets or wiring
runtime. Preserve uncertainty: same bounds are weaker than silhouette/anatomy.
Next geometry-anchored complete turn with latest carry/north unload exact joins,
shared helmet, actual arrival/lifecycle/Continue; stance foot/root contact, whole
master fidelity and all-family consistency/polish remain. Goal active/incomplete.
Handoff: character/james-west-carry-walk-keys-v1/arrival-turn-refine-v290/HANDOFF.md.
'''
guides=record_guides(r,section,'### James arrival-turn coverage and rejected whole-pose placement trials')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James planted arrival turn

## Objective and acceptance
Full master-matched James set, normal lifecycle and all-family consistency/polish.

## Accepted decisions and constraints
Master matte quilt/yellow accents/proportions/perspective. Wrench remains on belt,
case in hands. Whole source registration; no body-fit scaling to hide deviations.

## Current state
V290 single bare back-left planted turn3 appearance revision. Frozen target/original
master/prompt, generated raw, fixed global256source, master/source/native comparisons,
review and provisional source ledger. Five guides updated. Normal bank unchanged.

## Verification
Raw/master-source/native four-size board viewed.22checks0/1capture; scratch owner
unchanged, frozen hashes stable. Original148/crown77/sole224 vs149/76/224; no source
fit or translation. Silhouette not exact; source still provisional. No helmet/full
turn joins, physical moving contacts or actual arrival wiring tested.

## Next action
Extend consistent registered turn poses and exact latest carry/north-unload joins.
Review head/anatomy/case/belt/hardware/grade before shared helmet/native lifecycle.
Then moving stance/root contacts, normal source/checkpoint admission, interruptions/
Continue, full action coverage and cross-family consistency/polish.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in o.glob('*.png')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(provisionalBareSource=290,checks=22,failures=0,alphaSilhouetteIoU=round(iou,4),guides=guides,lfsRasters=len(rasters),goalComplete=False)))
