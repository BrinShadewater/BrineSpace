from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-window-v263';study=p/'thigh-coordinated-v262';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes());d=json.loads((study/'inputs.json').read_bytes());report=json.loads((study/'package-review.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(86,0,6)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
assert all(sha(r/f)==h for f,h in d['referenceSha256'].items()) and sha(study/'prompt.txt')==d['promptSha256']
for source in d['sources']:assert all(sha(r/row['file'])==row['sha256'] for row in source['files'].values())
report.update(disposition='unselected_joint_construction_improvement_boundary_and_master_grade_pending',rawVisuallyReviewed=True,sourceBoardsReviewed=['thigh-detail-review.png','paired-source-review.png'],nativeIncluded=True,findings=['Four-pose joint sheet brings coarse cloth midtones closer together and retains diagonal seam/quilt construction; topological seam continuity is still provisional.', 'Before/after same-mask medians11:56.46to59.60,12:65.50to62.78,13:58.28to61.28,14:62.71to62.43. Each95th rises; joint edit homogenizes partly by brightening. Different masks/poses do not measure identical material or prove flicker absent.', 'Knees, original silhouette/alpha, outside component and body pairing exact. All six native source poses at four sizes/both gears reviewed. Original selected panel at10/15 still creates construction boundaries.', 'No continuous full49 native motion, anatomical/perspective/contact or normal cargo lifecycle acceptance.'])
(study/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(study/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='dacc47e1-de4e-4816-8831-15ddb358e8f0',method='builtin_imagegen_joint_four_pose_sheet',rawSha256=sha(study/'raw.png'),prompt='prompt.txt'),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();progress=json.loads(old);new=[]
for phase in [11,12,13,14]:new.append(dict(phase=phase,version=262,sources={gear:dict(file=(study/f'phase{phase}/{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(study/f'phase{phase}/{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False))
progress['thighConstructionStudies']=[s for s in progress.get('thighConstructionStudies',[]) if s['phase'] not in [11,12,13,14]]+new
progress['nextVisualRepair']='Extend coherent master quilt/seam construction to adjoining selected panel poses10/15; retain anatomical geometry/knee fittings, match original charcoal brightness without joint brightening. Full49 material/proportion/perspective/contact and normal cargo lifecycle/all-family polish remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=86,nativeFailures=0,pairedSources=12,reviewedNativeCaptures=6,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceBoard='local-source-review.png',sourceIndices=[10,11,12,13,14,15],durationsMs=[20]*6,coordinatedStudy=262,selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James coordinated four-pose thigh sheet - October3,2026

V262 joint2x2 edit of unselected11..14 thigh crops with original master fabric.
Raw sheet and two protected-source boards reviewed before native launch.
Original knees, alpha/silhouette, outside component and paired shared body exact.
Joint same-mask medians now59.60/62.78/61.28/62.43 versus56.46/65.50/58.28/62.71;
each95th rises. More even cloth appearance partly achieved through brightening;
not final master material or temporal grade acceptance. Joint candidates retained
as UNSELECTED construction studies, replacing earlier study references only.
V263 includes selected10/15 boundary poses around joint11..14, six20ms/120ms.
86native checks0/6captures, paired four-size source/native boards reviewed;
scratch owner profile unchanged and frozen sources stable. Panel construction at
untouched10/15 remains obvious at close scale. No normal selected bank change.

Lesson: joint pose-sheet editing can reduce inter-pose variation but can homogenize
by raising darker poses' highlights; inspect original master brightness and motion
separately. Preserve exact cell layout, split raw cells once, resize each once,
admit only protected component RGB and retain original alpha/knee/pose geometry.
Joint source-sheet similarity is not normal gait/contact or continuous flash proof.
Next extend master garment construction to10/15 boundaries, check original matte
charcoal grade and full49 motion; anatomical proportions/perspective/contact,
normal cargo lifecycle and all-family consistency/polish remain open.
Full goal active/incomplete. Handoff:
character/james-west-carry-walk-keys-v1/thigh-window-v263/HANDOFF.md.
'''
guides=record_guides(r,section,'### James diagonal thigh neighbours and coordinated review')
for folder in [study,out]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: joint raw sheet/frozen references and prompt, four protected paired sources, V263 native/source evidence, unselected study ledger, five guides. Checks:86/0/6; exact profile/knees/alpha and hashes.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in [study,out] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(unselectedJointStudy=262,checks=86,failures=0,reviewedCaptures=6,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
