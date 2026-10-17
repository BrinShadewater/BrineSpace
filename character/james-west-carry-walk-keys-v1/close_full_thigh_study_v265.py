from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'full-gait-review-v265';study=p/'thigh-boundaries-v264';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes());d=json.loads((study/'inputs.json').read_bytes());report=json.loads((study/'package-review.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(939,0,49)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
assert all(sha(r/f)==h for f,h in d['referenceSha256'].items()) and sha(study/'prompt.txt')==d['promptSha256']
for row in d['sources']:assert all(sha(r/item['file'])==item['sha256'] for item in row['files'].values())
changed=[];reused=[];previous=p/'full-gait-review-v242'
for phase in range(49):
 a=out/f'native/carry-full-review-west-{phase:03d}.png';b=previous/f'native/carry-full-review-west-{phase:03d}.png'
 if sha(a)==sha(b):reused.append(dict(phase=phase,fromEvidence=b.relative_to(r).as_posix(),sha256=sha(a)))
 else:changed.append(phase)
assert changed==[0,1,2,10,11,12,13,14,15,47,48]
(out/'visual-evidence-reuse.json').write_text(json.dumps(dict(changedPhasesReviewed=changed,changedNativeBoardsReviewed=[0,3,4,5,15,16],reusedPreviouslyReviewedCaptures=reused,scope='Changed native poses freshly viewed;38 identical PNG captures reuse V242 review chain. All49 thigh crop board freshly viewed. Not continuous visual motion acceptance.'),indent=2)+'\n',encoding='utf-8')
report.update(disposition='unselected_boundary_construction_master_grade_pending',rawVisuallyReviewed=True,sourceBoardsReviewed=['thigh-detail-review.png','paired-source-review.png'],nativeIncluded=True,findings=['Target10/15 now have fine quilting/yellow seam in protected thigh component; original knees/alpha/silhouette/equipment exact. Reference11/14 pixels remain wholly original despite generator rewriting them in raw sheet.', 'Same-mask medians10:49.21to61.50,15:55.14to62.35; phase15p95:81.76to97.83. Requested original brightness not met; candidate retained only as construction study, not final material acceptance.', 'Complete mixed49 source cycle shows panel/quilt design changes persist in other regions. Native939/0/49 covers exact sources/clocks/pivots and three time-based fixture loops; no normal lifecycle/world contact or full visual acceptance.'])
(study/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(study/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='6bb3d196-da32-4482-8be2-ec0fc31b1c24',method='builtin_imagegen_two_targets_two_unchanged_references',rawSha256=sha(study/'raw.png'),prompt='prompt.txt'),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();progress=json.loads(old);new=[]
for phase in [10,15]:new.append(dict(phase=phase,version=264,sources={gear:dict(file=(study/f'phase{phase}/{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(study/f'phase{phase}/{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False))
progress['thighConstructionStudies']=[s for s in progress.get('thighConstructionStudies',[]) if s['phase'] not in [10,15]]+new
progress['nextVisualRepair']='Full49 source board confirms remaining rectangular thigh panels in5..9,16..29 and other later poses; extend coherent master construction in pose-specific grouped sheets, preserve already-correct cloth and original charcoal brightness. Full temporal/proportion/perspective/contact, normal cargo lifecycle and all-family consistency remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=939,nativeFailures=0,pairedSources=98,nativeCaptures=49,newlyReviewedChangedPhases=changed,reusedIdenticalReviewedCaptures=len(reused),reviewedSourceBoards=['all-thigh-review.png','seam-master-review.png'],selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['All49 thigh regions freshly reviewed; several blocks retain invented rectangular panels. Current studies produce closer quilt/yellow construction but brighten some charcoal. Full cycle garment design still inconsistent.', 'Native screenshot technical pass and original1680ms APNG do not certify actual ground contact, full continuous visual motion or normal pickup/carry/turn/unload behavior.']),indent=2)+'\n',encoding='utf-8')
section='''### James thigh boundaries and full49 construction review - October3,2026

V264 two-target/two-reference sheet repairs selected10/15 rectangular panels;
raw/details/paired sources reviewed. Original knees, alpha/silhouette, outside
component and shared body exact. Reference11/14 retain entire original pixels.
355/335 admitted pixels; medians49.21to61.50/55.14to62.35; phase15 peak rises
81.76to97.83. Construction closer, requested original brightness not met.
Boundary candidates UNSELECTED, retained for coherent garment study only.
V265 full49 mixed selected+unselected studies0/1/2/10..15/47/48,98sources,
original1680ms cycle.939native checks0/49captures/three time-based fixture loops;
scratch owner profile unchanged and frozen hashes stable. Changed11poses viewed
freshly in six native boards;38PNG captures identical to reviewedV242 evidence.
All49 thigh crop board and master loop-join board freshly inspected. Remaining
panel design changes persist5..9,16..29 and later regions; no full source acceptance.
HTML playback98embedded sources checked byte-exact to frozen study manifests;
do not build mixed-study previews from the selected ledger alone.

Lesson: preserve reference-cell bytes locally even when generation alters them;
grouped targets can still lift original charcoal midtones. Review complete family
design coverage before admitting a repaired window, and give previews the exact
frozen manifest rather than a different source selector. Crop diagnostics do not
prove anatomy/contact, and time-based fixtures do not prove normal traveling gait.
Next extend coherent construction through remaining panels, preserve correct quilt
poses and original matte brightness; full temporal/master proportion/perspective/
contact, normal cargo lifecycle and all-family consistency/polish remain open.
Goal active/incomplete. Handoff:
character/james-west-carry-walk-keys-v1/full-gait-review-v265/HANDOFF.md.
'''
guides=record_guides(r,section,'### James coordinated four-pose thigh sheet')
for folder in [study,out]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: boundary raw/frozen prompt/two protected paired sources; full49 frozen review/native/browser artifacts; unselected study ledger and five guides. Checks:939/0/49,98 HTML sources, preserved owner profile/hashes. No normal bank changed.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in [study,out] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(unselectedBoundaryStudy=264,checks=939,failures=0,captures=49,changedPhasesViewed=len(changed),identicalEvidenceReused=len(reused),guides=guides,lfsRasters=len(rasters),goalComplete=False)))
