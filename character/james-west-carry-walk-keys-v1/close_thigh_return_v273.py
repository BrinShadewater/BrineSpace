from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-window-v273';study=p/'thigh-return-v272';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes());d=json.loads((study/'inputs.json').read_bytes());report=json.loads((study/'package-review.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(112,0,8)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
assert all(sha(r/f)==h for f,h in d['referenceSha256'].items()) and sha(study/'prompt.txt')==d['promptSha256']
for row in d['sources']:assert all(sha(r/item['file'])==item['sha256'] for item in row['files'].values())
report.update(disposition='unselected_return_leg_construction_original_brightness_not_met',rawVisuallyReviewed=True,sourceBoardsReviewed=['coordinate-source-review.png','admission-review.png','thigh-detail-review.png','paired-source-review.png'],nativeIncluded=True,findings=['Pose-specific upper-thigh polygons follow narrowing21..25 leg surfaces. Original glove zone and per-pose knee rectangles are protected; alpha/silhouette/outside component and paired body exact.', 'Quilt/yellow seam construction follows return stance, but same-mask medians54..57to68..71 show brightness increase. No final master material or temporal acceptance.', 'Raw generator reference20/background changes excluded; unchanged original reference preserved. All eight paired20..27 native captures at four sizes and three boards visually reviewed; selected26/27 still retain panel construction.', 'No full49 continuous visual motion, master anatomical/perspective/contact or normal pickup/carry/turn/unload acceptance.'])
(study/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(study/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='434432ea-a8b7-4952-aa31-9a04960de311',method='builtin_imagegen_five_targets_one_reference',rawSha256=sha(study/'raw.png'),prompt='prompt.txt'),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();progress=json.loads(old);new=[]
for phase in range(21,26):new.append(dict(phase=phase,version=272,sources={gear:dict(file=(study/f'phase{phase}/{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(study/f'phase{phase}/{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False))
progress['thighConstructionStudies']=[s for s in progress.get('thighConstructionStudies',[]) if s['phase'] not in range(21,26)]+new
progress['nextVisualRepair']='Remaining26..29 and later panel poses need pose-specific garment construction; 26unselected construction studies now include0/1/2/5..25/47/48, with grade unresolved. Preserve existing correct cloth, anatomy/knees/gloves and alpha. Full49 temporal/master proportion/perspective/contact, normal cargo lifecycle and all-family consistency remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=112,nativeFailures=0,pairedSources=16,reviewedNativeCaptures=8,reviewedNativeBoards=['native-review-0.png','native-review-1.png','native-review-2.png'],sourceIndices=list(range(20,28)),durationsMs=[20,20,30,40,40,40,40,40],reviewedSourceBoard='local-source-review.png',constructionStudy=272,selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James narrowing return-leg thigh construction - October3,2026

V272 five21..25 targets plus unchanged20 reference generated3x2. Original21..26
native-coordinate source board inspected; per-pose thigh polygons narrow with
return stance, original knee ROIs and glove zone96/112/134/147 protected.
Raw/admission/detail/paired sources reviewed before native launch. Quilt/yellow
construction added without changing original alpha/silhouette, protected fittings,
hands, reference20 or outside component; shared body exact. Same-mask medians
54..57to68..71: matte brightness still NOT achieved. UNSELECTED studies only.
V273consecutive20..27, original270ms,16paired sources:112native checks0/
8captures; source and all three native boards reviewed at four sizes/both gears.
Scratch owner profile unchanged and frozen source hashes stable. Original26/27
panel construction remains; no main selected sources or normal runtime changed.

Lesson: narrowing stance requires independent cloth masks and knee protection;
do not carry a wide-stride rectangle into glove or fitting regions. Coordinate
overlays help identify actual source boundaries; they are review aids, not art.
Source protection and technical timing cannot certify anatomical/perspective or
world sole contact, and consistent brighter cloth still fails original matte grade.
Next26..29 and later panel poses, preserve existing correct fabric; construction
study grade unresolved. Full49 temporal/master proportion/perspective/contact,
normal cargo lifecycle and all-family consistency/polish remain open.
Goal active/incomplete. Handoff:
character/james-west-carry-walk-keys-v1/thigh-window-v273/HANDOFF.md.
'''
guides=record_guides(r,section,'### James later diagonal thigh run and edge admission')
for folder in [study,out]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: five return-leg target candidates/frozen prompt and references; per-pose admission; V273 source/native evidence; unselected study ledger and five guides. Checks112/0/8, original profile/hashes preserved.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in [study,out] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(unselectedStudy=272,newConstructionPoses=5,totalConstructionStudies=len(progress['thighConstructionStudies']),checks=112,failures=0,reviewedCaptures=8,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
