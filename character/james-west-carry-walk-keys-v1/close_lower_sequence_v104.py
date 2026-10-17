from pathlib import Path
import hashlib,json,subprocess
from milestone_notes import record_guides

p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'lower-sequence-v104'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
frozen=json.loads((out/'inputs.json').read_bytes())
assert all(sha(r/f)==v for f,v in frozen['preLaunchSha256'].items())
n=json.loads((out/'native-evidence.json').read_bytes())
v=json.loads((out/'native_probe-validation.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(86,0,6)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
manifest=json.loads((out/'bare-manifest.json').read_bytes())['states'][0]
assert manifest['sourceIndices']==[3,4,5,6,7,8]
assert manifest['frameDurationsMs']==[40,40,40,40,40,30]
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes())
spec=[(6,101,'59c73a35-b8b5-42b0-a303-81045d9e4a1a'),(7,102,'4769ba20-3a85-4873-b0ac-eee854296453'),(8,103,'3fae76a6-f1aa-4e11-a8f1-b9f2c97bb67b')]
findings=[
 'Toe and ankle highlights are warmer and less stark in six reviewed source boards and all six paired native captures at four sizes.',
 'Original alpha, one-pixel rim, rows above181 and paired body below110 are exact; interior hardware landmarks are visually assessed rather than pixel-protected geometry.',
 'Phase3 retains simpler boot construction than phases4..8; bright protected rim pixels remain. Complete sequence finish and absence of temporal flashing remain unproven.',
 'Original-master body proportions, full49-frame continuous motion, normal carry lifecycle and cross-family consistency are still pending.'
]
metrics=[]
for phase,version,execution in spec:
 folder=p/f'lower-material-phase{phase}-v{version}';d=json.loads((folder/'inputs.json').read_bytes())
 for group in ['sourceSha256','referenceSha256']:
  assert all(sha(r/f)==h for f,h in d[group].items())
 assert sha(folder/'prompt.txt')==d['promptSha256']
 (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
 f=folder/'package-review.json';review=json.loads(f.read_bytes())
 assert all(review[k] for k in ['alphaExact','outerOnePixelRingExact','allRowsAbove181Exact','pairedBodyBelow110Exact'])
 review.update(disposition='retain_provisional_lower_material_refinement',reviewedSourceBoards=['lower-detail-review.png','paired-lower-review.png'],visualReviewer='Codex',nativeIncluded=True,findings=findings,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
 f.write_text(json.dumps(review,indent=2)+'\n')
 row=progress['states'][phase]
 sources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']}
 if row['candidateSources']!=sources:row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
 row.update(candidateSources=sources,sourceAcceptance=False,reviewStatus='provisional_lower_material_refinement_master_neighbor_finish_motion_pending')
 metrics.append(dict(phase=phase,admitted=review['admittedPixelCount'],outsideExact=review['outsideExactPixels'],luma=review['localLumaQuartilesAnd95']))
assert progress['candidatePhases']==20 and len(progress['remainingSourcePhases'])==29
progress['lowerMaterialRefinementPhases']=[4,5,6,7,8]
ledger.write_text(json.dumps(progress,indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=86,nativeFailures=0,pairedSourceSlots=12,reviewedNativeCaptures=6,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='lower-source-review.png',visualReviewer='Codex',sourceIndices=manifest['sourceIndices'],durationsMs=manifest['frameDurationsMs'],sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,continuousVisualMotionAcceptance=False,findings=findings,metrics=metrics),indent=2)+'\n')
section='''### James carrying lower finish reviewed through phase8 — October 2, 2026

V101phase6, V102phase7 and V103phase8 lower-crop sources are terminal/copied with
exact prompts and frozen hashes. All six crop/paired source boards and V104
phase3..8 source window plus six paired native captures at four sizes visually
reviewed by Codex. New candidates retain warmer, less stark toe/ankle highlights
and readable construction. Phase3 still has simpler boot construction than4..8;
bright protected outer-rim pixels remain. No absence-of-flash or continuous motion
acceptance. Phase5 is a material anchor for6..8, not their immediate predecessor.

Admitted lower pixels1040/1032/1042; outside exact64496/64504/64494. Full original
alpha, one-pixel rim and rows above181 remain exact to prior local body sources;
paired body below110 exact. Interior hardware geometry is visually assessed,
not strict original-master landmark equality. Local95thpercentile before/after:
phase6 174.01/166.86, phase7 173.15/164.71, phase8 172.00/161.08. Diagnostic only:
phase8 median rises64.31to67.85 despite lower upper-tail highlights. Reduced
highlight extremes do not establish uniformly darker material or consistent grade.

V104 retains original40/40/40/40/40/30ms sequence (230ms), twelve paired sources.
Native86checks/0failures/six captures, engine terminal; owner profile unchanged
under scratch APPDATA. Frozen runtime/registry/input hashes remain exact. Ledger
phase6..8 points to V101..103, preserving prior candidates. Still20/49candidate
phases with29 remaining; lower refinement does not add new source coverage.
Normal selection unchanged. Full49gait, original-master anatomy/detail acceptance,
normal carrying lifecycle and full James cross-family consistency remain open.

Lesson: inspect construction continuity separately from highlight statistics.
A lower95thpercentile can coexist with a brighter median. Material anchors must
be labeled as anchors, and fixed alpha cannot establish interior anatomy fidelity.
Evidence: character/james-west-carry-walk-keys-v1/lower-sequence-v104/review.json.
'''
guides=record_guides(r,section,'### James carrying boot and ankle highlights refined')
folders=[p/f'lower-material-phase{phase}-v{version}' for phase,version,_ in spec]+[out]
handoff='''# Project handoff

Updated: October2,2026. Task: James complete master-matched animation library.

## Objective and acceptance
Full set plus original-master style, proportions, perspective and material matching;
complete motion, integration and cross-family polish remain required.

## Accepted decisions and constraints
Reversible repairs authorized. Original master is authority. Preserve normal
selection and owner profile; technical passes do not establish art acceptance.

## Current state
Three lower crop studies retained provisionally; six-frame native/source review
closed. Ledger and five guides updated. No commit, export or normal installation.

## Verification
86 native checks, zero failures; six captures and seven source boards reviewed.
Frozen input hashes and owner profile unchanged. Full motion acceptance pending.

## Next action
Address simpler phase3 construction and remaining29 original carry phases;
review whole gait and normal handoffs, then finish cross-family master comparison.

'''
for folder in folders:(folder/'HANDOFF.md').write_text(handoff+section,encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==3*len(rasters)+1 and all(x==b'lfs' for x in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=86,failures=0,capturesReviewed=6,candidates=20,remaining=29,guides=guides,lfsRasters=len(rasters),normalChanged=False)))
