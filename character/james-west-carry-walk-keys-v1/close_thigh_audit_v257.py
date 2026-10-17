from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-window-v257';audit=p/'thigh-audit-v253';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes());assert (n['checks'],n['failures'],n['captures'])==(73,0,5)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
ai=json.loads((audit/'inputs.json').read_bytes());assert all(sha(r/row['file'])==row['sha256'] for row in ai['sources'])
(audit/'review.json').write_text(json.dumps(dict(reviewedBoard='all-selected-thighs.png',reviewedSelectedPhases=49,clearPanelExamples=[0,8,12,21,25,28,34,37,39,44,48],quiltAlreadyVisibleExamples=[3,4,5,29,30,31,32,33,35,36,41,42],findings=['Rectangular panel/parallel stripe construction recurs through substantial parts of the carrying stride, rather than only at loop entry.', 'Examples are visual triage, not a complete component segmentation or anatomical acceptance. Some thighs leave fixed crop104/136/144/176; absence of seam in this crop is not proof it is missing on the whole leg.', 'Use pose-specific thigh extents and preserve existing correct construction before extending repair.'],normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
folders=[p/'thigh-construction-phase0-v254',p/'thigh-construction-phase12-v255',p/'thigh-construction-phase12-v256']
for folder in folders:
 d=json.loads((folder/'inputs.json').read_bytes())
 for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
 assert sha(folder/'prompt.txt')==d['promptSha256']
 report=json.loads((folder/'package-review.json').read_bytes());assert report['alphaExact'] and report['outerOnePixelRingExact'] and report['pairedBodyBelow110Exact']
 if folder.name.endswith('v254'):
  report.update(disposition='rejected_before_native_brightness_and_contrast_increase',findings=['Cloth swatch is isolated from yellow seam and equipment, but candidate still brightens same-admission median62.49to64.78 and95th90.29to93.26; quilt lines stronger. Requested darker neighbour grade not achieved. Excluded before native; phase0studyV244 remains unchanged.'],nativeIncluded=False)
 elif folder.name.endswith('v255'):
  report.update(disposition='superseded_packaging_mask_left_panel_border',findings=['Raw generated quilt/seam follows diagonal thigh; first polygon under-covers original panel boundary, leaving a visibly retained border. No native test of this packaging. Repacked asV256 without another generation.'],nativeIncluded=False)
 else:
  base=r/d['baseFolder'];proof=[]
  for gear in ['bare','helmet']:
   a=np.asarray(Image.open(base/f'{gear}-head-protected.png'));b=np.asarray(Image.open(folder/f'{gear}-head-protected.png'))
   for x0,y0,x1,y1 in d['protectedRectangles']:
    assert np.array_equal(a[y0:y1,x0:x1],b[y0:y1,x0:x1]);proof.append(dict(gear=gear,rectangle=[x0,y0,x1,y1],exact=True))
  (folder/'knee-preservation.json').write_text(json.dumps(dict(proofs=proof,scope='Original fitting ROI exact to phase12 base for both gears; not complete anatomical/perspective acceptance.'),indent=2)+'\n',encoding='utf-8')
  report.update(disposition='unselected_diagonal_thigh_construction_master_motion_pending',findings=['Expanded pose-specific polygon removes old panel border more cleanly; protected original knee ROI exact for both gears.292 admitted pixels,65244 outside exact; original alpha/rim/shared body preserved.', 'Same-admission median60.46to65.50,95th117.83to97.04: softer hardware-like panel highlight but cloth brighter. Neighbours retain panel construction; family grade/style continuity pending.', 'Raw and source boards reviewed before native launch; all five paired V257 native poses/four sizes and source board now reviewed. No continuous full49 grade/contact or normal controller acceptance.'],nativeIncluded=True)
 report.update(rawVisuallyReviewed=True,reviewedSourceBoards=['thigh-detail-review.png','paired-neighbor-review.png']);(folder/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
for version,execution in [(254,'be3109f0-ffeb-4c15-9bda-dbbaeca3ff86'),(255,'45304c28-a7b9-4d28-9fb7-42c3191b90ae')]:
 folder=folders[0] if version==254 else folders[1];(folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt'),indent=2)+'\n',encoding='utf-8')
(folders[2]/'generation.json').write_text(json.dumps(dict(state='reused_raw_packaging_only',execution='45304c28-a7b9-4d28-9fb7-42c3191b90ae',rawSource='thigh-construction-phase12-v255/raw.png',rawSha256=sha(folders[2]/'raw.png'),newGeneration=False),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());study=dict(phase=12,version=256,sources={gear:dict(file=(folders[2]/f'{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folders[2]/f'{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False)
progress['thighConstructionStudies']=[s for s in progress.get('thighConstructionStudies',[]) if s['phase']!=12]+[study];progress['nextVisualRepair']='Pose-specific diagonal thigh construction across recurring panel phases; preserve correct quilt poses, coordinate garment seam and grade in motion; master anatomical/perspective/contact and versioned normal cargo lifecycle, all-family consistency'
ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=73,nativeFailures=0,pairedSources=10,reviewedNativeCaptures=5,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],sourceIndices=[10,11,12,13,14],durationsMs=[20]*5,phase12Study=256,excludedBeforeNative=[254,255],selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James full thigh audit and diagonal construction study - October3,2026

V253 all49 selected thigh crops visually reviewed; recurring rectangular panels
across substantial stride regions, with already-quilted examples recorded separately.
Fixed crop may miss extended thighs; use pose-specific component extents.
V254phase0 swatch edit REJECTED before native: median62.49to64.78,
95th90.29to93.26 and stronger quilt contrast despite darker cloth reference.
V255phase12 generated diagonal quilt/seam; first mask left old panel border.
V256 reuses same raw with expanded component polygon and exact protected knee
ROI134/164/155/185 for both gears.292 admitted pixels,65244 outside exact;
alpha/rim/shared body exact. Median60.46to65.50,95th117.83to97.04; cloth brighter,
family grade pending. Raw and source boards reviewed before native launch.

V25710..14 five20ms poses100ms:73 native checks/0 failures/5 paired four-size
captures; source and both native boards reviewed, owner profile unchanged and
frozen hashes stable. Candidate UNSELECTED; neighbours retain old panels.
Lesson: masks can preserve the defect itself; inspect original component boundary
and protected fitting separately. Record repackaging as reuse of existing raw,
never as another generation. Colour swatch instructions still require output review.
Next coordinated pose-specific thigh construction, seam/grade continuity in motion,
master anatomy/perspective/contact, normal cargo lifecycle and all-family polish.
Full objective active/incomplete; selected and normal sources unchanged. Evidence:
character/james-west-carry-walk-keys-v1/thigh-audit-v253/review.json;
character/james-west-carry-walk-keys-v1/thigh-window-v257/review.json.
'''
guides=record_guides(r,section,'### James thigh join extended and over-dark frame0 remake rejected')
for folder in folders+[audit,out]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: V253 audit; V254 rejected study; V255 raw/first package; V256 wider protected package; V257 native review; study ledger and five guides.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in folders+[audit,out] for f in root.rglob('*') if f.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(auditedPhases=49,unselectedStudy=256,rejectedBeforeNative=254,checks=73,failures=0,reviewedCaptures=5,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
