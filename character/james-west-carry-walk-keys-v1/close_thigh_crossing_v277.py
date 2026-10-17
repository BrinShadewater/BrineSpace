from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-window-v277';study=p/'thigh-crossing-v276';original=p/'thigh-crossing-v274';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes());d=json.loads((study/'inputs.json').read_bytes());report=json.loads((study/'package-review.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(112,0,8)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
assert all(sha(r/f)==h for f,h in d['referenceSha256'].items()) and sha(study/'prompt.txt')==d['promptSha256']
assert sha(study/'raw.png')==sha(original/'raw.png')==d['rawSha256']
proof=[]
for row in d['sources']:
 assert all(sha(r/item['file'])==item['sha256'] for item in row['files'].values())
 for gear in ['bare','helmet']:
  a=np.asarray(Image.open(r/row['files'][gear]['file']));b=np.asarray(Image.open(study/f'phase{row["phase"]}/{gear}-head-protected.png'))
  for x0,y0,x1,y1 in row['protectedRectangles']:assert np.array_equal(a[y0:y1,x0:x1],b[y0:y1,x0:x1])
  proof.append(dict(phase=row['phase'],gear=gear,protectedRectangles=row['protectedRectangles'],exact=True))
(study/'protected-fitting-proof.json').write_text(json.dumps(dict(proofs=proof,phase30FullFittingRectangle=[104,155,129,184],scope='Exact original source knee/glove rectangles, not full-body anatomical/contact acceptance.'),indent=2)+'\n',encoding='utf-8')
report.update(disposition='unselected_crossing_cloth_complete_knees_protected_grade_pending',rawVisuallyReviewed=True,sourceBoardsReviewed=['coordinate-source-review.png','admission-review.png','thigh-detail-review.png','paired-source-review.png'],nativeIncluded=True,findings=['Five26..30 near-thigh surfaces now have quilt/yellow construction. Source leg overlap, alpha/silhouette, outside component, gloves and expanded complete knee rectangles exact for both gears. Phase30 entire fitting104/155/129/184 preserves priorV240 finish.', 'Raw changed other leg cloth/seams, reference25, equipment and backdrop; all outside admission excluded. V276 reuses exact raw274 with broader knee protection; no new generation.', 'Same-mask cloth medians55..57to71..74 still exceed originals. Far-side panel/parallel stripes remain in crossing poses and need separate component review. Selected31 kept unchanged.', 'All eight24..31 paired native captures/four sizes and three boards reviewed. Original320ms clock checks pass. No full49 visual motion/master grade, anatomy/perspective/contact or normal lifecycle acceptance.'])
(study/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(original/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='2aca2248-2e2a-4983-b995-3506e20569d6',method='builtin_imagegen',rawSha256=sha(original/'raw.png'),prompt='prompt.txt'),indent=2)+'\n',encoding='utf-8')
(study/'generation.json').write_text(json.dumps(dict(state='reused_raw_packaging_only',newGeneration=False,execution='2aca2248-2e2a-4983-b995-3506e20569d6',rawSource=d['rawSource'],rawSha256=sha(study/'raw.png')),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();progress=json.loads(old);new=[]
for phase in range(26,31):new.append(dict(phase=phase,version=276,sources={gear:dict(file=(study/f'phase{phase}/{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(study/f'phase{phase}/{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False))
progress['thighConstructionStudies']=[s for s in progress.get('thighConstructionStudies',[]) if s['phase'] not in range(26,31)]+new
progress['nextVisualRepair']='Audit remaining31..46 and separate far-side crossing cloth panels;31unselected near-thigh studies include0/1/2/5..30/47/48, grade unresolved. Preserve correct existing fabric, complete knee fittings, gloves and alpha. Full49 temporal/master anatomy/perspective/contact, normal cargo lifecycle and all-family consistency remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
for folder in [p/'thigh-window-v275',out]:
 (folder/'review.json').write_text(json.dumps(dict(nativeChecks=112,nativeFailures=0,pairedSources=16,reviewedNativeCaptures=8,reviewedNativeBoards=['native-review-0.png','native-review-1.png','native-review-2.png'],sourceIndices=list(range(24,32)),durationsMs=[40]*8,constructionStudy=274 if folder.name.endswith('275') else 276,superseded=folder.name.endswith('275'),selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James crossing near-thigh construction and complete knee protection - October3,2026

V274 five26..30 target near-thigh surfaces plus unchanged25 reference generated
3x2sheet. Original26..31 coordinate source crops inspected; per-pose cloth masks
follow crossing leg angles. First raw/protected sources and V275native112/0/8
reviewed; small knee rectangles did not establish protection of complete rims.
V276 reuses exact raw with wider knee guards, particularly30full104/155/129/184
fitting containing priorV240 matte finish. Final source/admission/detail/paired
boards reviewed, twelve paired fitting/glove rectangle proofs exact; original
alpha/silhouette, outside component, source overlap and shared body preserved.
V277eight24..31 poses/original320ms:112native checks0/8captures; all three
four-size paired native boards reviewed. Scratch owner profile unchanged and
frozen inputs stable. V275 superseded packaging, no second generation for276.
Median cloth55..57to71..74 still too bright; far-side panel/stripe construction
remains separately visible in crossing poses. Source31 preserved unchanged.
31UNSELECTED near-thigh studies now retained; no main/normal source replacement.

Lesson: a knee-centre rectangle can exclude the fitting rim and erase prior
material repairs. Preserve complete original hardware extent, including existing
finish, then admit neighbouring cloth; exact small-ROI checks are not full-fitting
proof. Repair one visible thigh surface without claiming the occluded/other leg
also matches. Garment coverage does not certify anatomy, perspective or contact.
Next audit31..46, separate far-side crossing cloth and original charcoal grade;
full49 motion/master proportions/perspective/contact, normal cargo lifecycle and
all-family consistency/polish remain open. Goal active/incomplete. Handoff:
character/james-west-carry-walk-keys-v1/thigh-window-v277/HANDOFF.md.
'''
guides=record_guides(r,section,'### James narrowing return-leg thigh construction')
for folder in [original,study,p/'thigh-window-v275',out]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: five crossing source targets/frozen prompt, reused raw/full fitting admission, V275/V277 source/native evidence, protected-ROI proof, study ledger and five guides. Final112/0/8 with profile/hashes preserved.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in [original,study,p/'thigh-window-v275',out] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(unselectedStudy=276,reusedRaw=274,totalConstructionStudies=len(progress['thighConstructionStudies']),checks=112,failures=0,reviewedCaptures=8,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
