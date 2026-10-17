from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-window-v261';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(73,0,5)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
studies=[]
for phase,version,execution in [(11,258,'f8e7ede9-da03-4e82-a8cd-afa3c1dd69e2'),(13,259,'3a301861-a9a5-4fb5-9db5-fbc6cbd14c6d'),(14,260,'ddd89740-1eea-4c7f-9b0b-de76ca23a8b5')]:
 folder=p/f'thigh-construction-phase{phase}-v{version}';d=json.loads((folder/'inputs.json').read_bytes());report=json.loads((folder/'package-review.json').read_bytes())
 for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
 assert sha(folder/'prompt.txt')==d['promptSha256']
 proofs=[]
 for gear in ['bare','helmet']:
  a=np.asarray(Image.open(r/d['baseFolder']/f'{gear}-head-protected.png'));b=np.asarray(Image.open(folder/f'{gear}-head-protected.png'))
  for x0,y0,x1,y1 in d['protectedRectangles']:
   assert np.array_equal(a[y0:y1,x0:x1],b[y0:y1,x0:x1]);proofs.append(dict(gear=gear,rectangle=[x0,y0,x1,y1],exact=True))
 (folder/'knee-preservation.json').write_text(json.dumps(dict(proofs=proofs),indent=2)+'\n',encoding='utf-8')
 report.update(disposition='unselected_coordinated_thigh_construction_grade_and_seam_pending',rawVisuallyReviewed=True,reviewedSourceBoards=['thigh-detail-review.png'],reviewedCombinedSourceBoard='../thigh-window-v261/local-source-review.png',nativeIncluded=True,findings=['Original panel removed within protected component; fine quilting and yellow seam now present on four consecutive study poses11..14. Original knee ROI, alpha, silhouette and shared body exact.', 'Quilt ridge contrast and seam path differ between generated poses; phases12/14 appear brighter. Same-mask medians are diagnostic, not proof of material matching across different poses.', 'All five paired native captures at four sizes reviewed. Phase10 retains selected panel and creates construction boundary. No continuous full-cycle visual acceptance, normal lifecycle or anatomical/contact acceptance.'])
 (folder/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',method='builtin_imagegen'),indent=2)+'\n',encoding='utf-8')
 studies.append(dict(phase=phase,version=version,sources={gear:dict(file=(folder/f'{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False))
ledger=p/'material-repair-progress.json';before=ledger.read_bytes();progress=json.loads(before)
progress['thighConstructionStudies']=[s for s in progress.get('thighConstructionStudies',[]) if s['phase'] not in [11,13,14]]+studies
progress['nextVisualRepair']='Coordinate diagonal thigh seam path and charcoal brightness across11..14 and construction boundaries10/15; preserve source geometry and knees. Full gait master anatomy/perspective/contact, normal cargo lifecycle and all-family consistency remain.'
assert ledger.read_bytes()==before
ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=73,nativeFailures=0,pairedSources=10,reviewedNativeCaptures=5,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceBoard='local-source-review.png',sourceIndices=[10,11,12,13,14],durationsMs=[20]*5,studies={11:258,12:256,13:259,14:260},selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James diagonal thigh neighbours and coordinated review - October3,2026

V258phase11/V259phase13/V260phase14 generated from original selected poses with
master fabric reference; raw and packaged details reviewed before native launch.
Original knee ROI134/164/155/185 exact for both gears; alpha, silhouette, outside
admission and shared body preserved. Admitted354/350/349pixels respectively.
Same-mask median55.36to56.46/52.18to58.36/52.71to62.71; peaks softened but
charcoal midtones still vary, particularly12/14. No bounded grade acceptance.
V261 combines new11/13/14 with unselected12V256 and selected10V176, five20ms
poses/100ms.73native checks0/5captures, source and both native boards reviewed at
four sizes/both gears; scratch profile unchanged and frozen source hashes stable.
Four consecutive study poses now carry quilt/yellow construction, but seam path,
ridge contrast and bright12/14 need coordinated correction; panel remains at10.
Studies UNSELECTED. No main selected source or normal runtime replacement.

Lesson: a shared fabric swatch across independent pose edits does not lock seam
topology or padded-ridge brightness. Compare the actual consecutive component
sequence and both boundary poses before claiming material continuity. Protect
the original knee independently of generation, and record full-cycle motion,
normal contact/controller evidence separately from narrow source-window checks.
Next coordinate11..14 garment seam/grade and10/15 boundary construction;
master anatomy/perspective/contact, versioned normal cargo lifecycle and all-family
consistency/polish remain. Full objective active/incomplete, no blocker.
Handoff: character/james-west-carry-walk-keys-v1/thigh-window-v261/HANDOFF.md.
'''
guides=record_guides(r,section,'### James full thigh audit and diagonal construction study')
for folder in [out]+[p/f'thigh-construction-phase{s["phase"]}-v{s["version"]}' for s in studies]:
 (folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: three raw sources/protected paired candidates and frozen prompts; V261 source/native review; unselected study ledger; five guides. Checks:73/0/5, preserved knees/profile/hashes.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in [out]+[p/f'thigh-construction-phase{s["phase"]}-v{s["version"]}' for s in studies] for f in root.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(unselectedStudies=[258,259,260],checks=73,failures=0,reviewedCaptures=5,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
