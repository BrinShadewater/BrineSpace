from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'lower-window-v100';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
native=json.loads((out/'native-evidence.json').read_bytes());validation=json.loads((out/'native_probe-validation.json').read_bytes())
assert native['checks']==60 and native['failures']==0 and native['captures']==4
assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
spec=[(4,97,'0a47f2cb-3378-4ec4-804f-640789f707c7'),(5,98,'588bc246-7003-4b93-a7be-801bd3e7e7d1'),(4,99,'bb7599c2-9259-4b1e-a801-4d1510504a8d')]
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes())
for phase,version,execution in spec:
    folder=p/f'lower-material-phase{phase}-v{version}';d=json.loads((folder/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
    assert sha(folder/'prompt.txt')==d['promptSha256']
    (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
    f=folder/'package-review.json';review=json.loads(f.read_bytes())
    assert review['alphaExact'] and review['outerOnePixelRingExact'] and review['allRowsAbove181Exact'] and review['pairedBodyBelow110Exact']
    review.update(reviewedSourceBoards=['lower-detail-review.png','paired-lower-review.png'],sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
    if version==97:
        review.update(disposition='rejected_highlights_brightened',nativeIncluded=False,findings=['Initial toe-metal master sample carried strong reflections; source became brighter despite matte-only request.','Local95th percentile171.04to176.16 corroborates visual review but is not an acceptance measure.','Superseded by V99; do not adopt V97or count it as another repaired phase.'])
    else:
        review.update(disposition='retain_provisional_lower_material_refinement',nativeIncluded=True,findings=['Toe/ankle highlights more subdued and warm-neutral; construction/rivets retained in reviewed source/native views.','Alpha/outerrim and all rows above181 exactly match preceding local-body candidate, protecting head/case/upper body/knees. Internal lower hardware landmarks remain visual candidates, not pixel-protected geometry.','Original outer rim highlights remain; adjacent phase3simplification and phase6unrepaired lower finish still differ.','No full49gait, continuous visual motion, original-master anatomy acceptance or normal installation.'])
        row=progress['states'][phase];row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
        row.update(candidateSources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']},sourceAcceptance=False,reviewStatus='provisional_lower_material_refinement_master_neighbor_finish_motion_pending')
    f.write_text(json.dumps(review,indent=2)+'\n')
assert progress['candidatePhases']==20 and len(progress['remainingSourcePhases'])==29
progress['lowerMaterialRefinementPhases']=[4,5];ledger.write_text(json.dumps(progress,indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=60,nativeFailures=0,pairedSourceSlots=8,reviewedNativeCaptures=4,reviewedSourceWindowBoard=True,sourceIndices=[3,4,5,6],durationsMs=[40,40,40,40],sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,continuousVisualMotionAcceptance=False,findings=['Repaired lower-phase4V99andphase5V98 reviewed between current phase3/6. Highlights more subdued and construction retained.','Preserved bright outerrim and neighboring simplified/unrepaired lower gear still differ; not consistent full family finish or absence-of-flash acceptance.']),indent=2)+'\n')
section='''### James carrying boot and ankle highlights refined — October 2, 2026

Three authored lower96crop studies: V97phase4 REJECTED for brighter highlights;
V98phase5 and V99phase4 retained as provisional lower-material refinements. Raw,
exact prompts and frozen references copied. Six source boards (crop/paired per
study) visually reviewed. Reflective original toe-metal sample encouraged V97
brightness despite matte instruction. V99uses original leg-metal/quilting sample
and repaired adjacent V98finish as a material anchor, with explicit highlight
restraint. Same-pose target remains original local V90phase4, not V97geometry.

Admitted V99/V98lower interiors1014/1000pixels;64522/64536outside exact. Original
full alpha/one-pixel rim and every row above181remain exact to their prior body
candidate. Head/case/upper body/knees protected; paired body below110exact. Boot
footprints/sole rows fixed by original alpha, but internal strap/toe geometry is
only visually reviewed, not strict original-master landmark equality. Some bright
rim pixels remain. Local95thpercentileV99171.02to166.72,V98171.45to163.65; V97
171.04to176.16. Distribution supports the visual diagnosis, not a grading gate or
claimed25percent reduction. Fine rivets/boot construction remain readable.

V100paired phase3/4/5/6 window retains40/40/40/40ms. Native60checks/0failures,
eight exact sources and four paired four-size captures plus source window board
all viewed. Scratch APPDATA owner profile unchanged; frozen runtime/registry/input
hashes stable. Lower4/5warm subdued metal is closer, but simplified phase3and
unrepaired phase6lower finish still differ; no continuous visual motion or full
gait/master acceptance. Ledger remains20/49candidate phases,29without sources;
phase4/5candidate pointers now V99/V98with previous versions preserved. Nothing
new installed. Full James set, normal carry lifecycle and full consistency/polish
remain incomplete. All three generation jobs and engine run terminal.

Lesson: reference patches carry their lighting as well as construction. A highly
reflective master crop can contradict a matte instruction; choose a restrained
surface sample and compare adjacent repaired material without transferring pose.
Check failed as well as retained outputs. Exact alpha preserves foot contact but
does not prove internal equipment geometry or grade consistency. Next extend lower
finish through remaining neighbors, remaining49source gait, full motion/normal
integration, original-master proportions/detail and cross-family consistency.
Evidence:character/james-west-carry-walk-keys-v1/lower-window-v100/review.json.
'''
guides=record_guides(r,section,'### James local carrying material repairs extended through phase8')
folders=[p/f'lower-material-phase{phase}-v{version}' for phase,version,_ in spec]+[out]
for folder in folders:
    (folder/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched set and complete consistency polish; incomplete.\n\n'+section+'\nChanged: three lower material studies with one rejection, paired protective packaging, isolated four-frame native study, reusable guide-update helper, ledger and five guides. No normal art/controller change, commit/PR/export.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=60,failures=0,nativeCapturesReviewed=4,lowerRefinedPhases=[4,5],rejectedTrials=1,candidatePhases=20,remaining=29,guides=guides,lfsRasters=len(rasters),normalChanged=False)))
