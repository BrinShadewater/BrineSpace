from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'local-window-v149';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((o/'native-evidence.json').read_bytes());v=json.loads((o/'native_probe-validation.json').read_bytes());d=json.loads((o/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(73,0,5)
assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in d['preLaunchSha256'].items())
m=json.loads((o/'bare-manifest.json').read_bytes())['states'][0];assert m['sourceIndices']==[33,34,35,36,37] and m['frameDurationsMs']==[40]*5
findings=['Phase34/35 new fitting highlights are subdued while quilt detail stays readable.','V147 exposed older phase36V53 smoother fabric, bulkier boots and simpler fittings; it fails this neighbour consistency review and is superseded, preserved as history.','Phase36V148 rebuild uses original same-phase source and cropped master textile reference; original boots and silhouette retained. Interior anatomy and fitting shapes remain provisional.','All five paired native captures at four sizes and source window reviewed. Unrepaired37 has stronger fittings; protected original lower highlights still need a coordinated finish pass.','Static captures do not prove continuous motion, absence of flashes, full gait or original-master anatomy; normal lifecycle and all-family acceptance remain pending.']
j=json.loads((p/'material-repair-progress.json').read_bytes());folders=[]
for phase,version,execution in [(34,145,'65db0e7d-cc53-433d-a64d-c7dad93f6599'),(35,146,'20415d5a-e7fc-48f0-9719-a8e1e91d974e'),(36,148,'2e2b7df3-519d-4b94-86d8-7fe01e4dcd47')]:
    folder=p/f'local-material-phase{phase}-v{version}';folders.append(folder);i=json.loads((folder/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in i[group].items())
    assert sha(folder/'prompt.txt')==i['promptSha256']
    (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
    report=json.loads((folder/'package-review.json').read_bytes());assert all(report[k] for k in ['alphaExact','outerTwoPixelRingExact','headTop110Exact','bootsBelow200Exact','pairedBodyBelow110Exact'])
    report.update(reviewedSourceBoards=['crop-detail-review.png','paired-local-review.png'],visualReviewer='Codex',findings=findings,nativeIncluded=True,disposition='retain_provisional_candidate');(folder/'package-review.json').write_text(json.dumps(report,indent=2)+'\n')
    row=j['states'][phase]
    if not row['repairCandidateAvailable']:j['remainingSourcePhases'].remove(phase);j['candidatePhases']+=1
    if 'candidateSources' in row:row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
    row.update(repairCandidateAvailable=True,sourceAcceptance=False,reviewStatus='provisional_material_master_contact_motion_pending',candidateSources={mode:dict(file=(folder/f'{mode}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{mode}-head-protected.png')) for mode in ['bare','helmet']})
assert j['candidatePhases']==41 and len(j['remainingSourcePhases'])==8
j['nextVisualRepair']='Phase37/38 and remaining sources; lower finish coordination, full moving gait and normal lifecycle, all-family master consistency'
(p/'material-repair-progress.json').write_text(json.dumps(j,indent=2)+'\n')
for ver,disposition in [(147,'older_phase36_fails_neighbour_consistency_superseded_in_v149'),(149,'retain_provisional_neighbour_study')]:
    window=p/f'local-window-v{ver}';(window/'review.json').write_text(json.dumps(dict(nativeChecks=73,nativeFailures=0,pairedSources=10,sourceIndices=[33,34,35,36,37],durationsMs=[40]*5,reviewedNativeCaptures=5,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='local-source-review.png',visualReviewer='Codex',findings=findings,disposition=disposition,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
section='''### James carrying phase34/35 refined and older phase36 replaced — October 3, 2026

V145phase34/V146phase35/V148phase36 local body-crop generations are terminal/copied,
with frozen original same-phase sources and cropped original master textile authority.
All six crop/paired source boards reviewed. Admission2636/2543/2531pixels;
62900/62993/63005outside exact. Original alpha/two-pixel rim/head above110/boots
from200 down exact; paired body below110 exact. Fine quilt retained, fittings subdued;
interior landmarks remain visual candidates. Original alpha128 bounds respectively
[97,76,160,224],[99,76,163,223],[95,76,167,223]; the223sole is original gait geometry,
not an intentional height normalization or proof of matched master proportions.

V147 neighbouring33..37 review exposed older phase36V53 smoother fabric, bulkier
boots and simpler fittings. Its source window and all5paired four-size captures
were reviewed; it fails neighbour consistency, preserved as history. V148 rebuild
uses original36pose with protected lower pixels rather than adjusting the old
candidate. V149 repeats33..37 with replacement36:40ms each,total200ms;73native
checks/0failures/5paired four-size captures plus source board visually reviewed.
Owner profile unchanged under scratch APPDATA; frozen inputs/runtime/registry stable.
Ledger41/49provisional source phases,8remaining; normal selection unchanged.

Lesson: earlier provisional candidates require renewed neighbour comparison as
finer material repairs advance. A counted source is not accepted art. Supersede
visually inconsistent candidates using original same-phase authority and retain
provenance; do not hide simplified boots or fittings with a darker grade. Remaining
37..44sources, protected lower highlights, full moving gait, normal carrying
lifecycle and cross-family master proportions/perspective/height/colour consistency
and polish remain open. Static tests/captures do not prove absence of flashing or
continuous motion. Evidence:character/james-west-carry-walk-keys-v1/local-window-v149/review.json.
'''
guides=record_guides(r,section,'### James knee fitting protected and carrying coverage extends through phase33')
handoff='''# Project handoff

Updated: October3,2026. Task: full James master-matched animation library and polish.

## Objective and acceptance
Complete all animation families matching masters in art, colour, proportions,
perspective, size and height; verify full motion, normal integration and polish.

## Accepted decisions and constraints
Original masters govern. Reversible source repair authorized; keep owner saves,
normal selections and other characters unchanged. Test success is not art acceptance.

## Changed files and current state
V145/146phase34/35 sources, V148replacement36, V147failed-neighbour evidence,
V149revised review, ledger and five status/pipeline/bible/skill guides.41/49
provisional sources,8remaining. Older36pointer preserved in superseded history.

## Verification
Each native window73checks,0failures;all10paired four-size captures and source
boards reviewed. Owner profile and frozen runtime/input hashes unchanged.
No continuous visual motion, normal lifecycle or full master-match acceptance.

## Remaining work
37..44sources and lower finish; full moving gait, normal carrying lifecycle,
all-family original-master consistency, full animation library and polish.

'''
for folder in folders+[p/'local-window-v147',o]:(folder/'HANDOFF.md').write_text(handoff+section)
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders+[p/'local-window-v147',o] for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert len(a)==3*len(rasters)+1 and all(x==b'lfs' for x in a[2:-1:3])
print(json.dumps(dict(candidates=41,remaining=8,nativeChecksPerWindow=73,failures=0,reviewedCaptures=10,guides=guides,lfsRasters=len(rasters))))
