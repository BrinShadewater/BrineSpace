from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'lower-window-v178';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(86,0,6)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
findings=['Both new lower finishes retain readable articulated hardware and softer toe/ankle highlights in four source boards, six-frame source board and all six paired four-size native captures.', 'Phase10 upper-tail luma176.02to160.36 and median64.56to64.20; phase11 upper-tail174.79to167.61 but median67.00to70.26. Midtone brightness is not uniformly reduced. Phase13 original boots remain brighter; broader finish coordination still open.', 'Full original alpha, one-pixel rim, rows above181 and paired body below110 exact. Internal hardware structure visually assessed; outline protection does not certify anatomy.', 'Original30/20/20/20/20/20ms window (130ms) verified in finite fixture. No continuous full49motion/flash/contact acceptance, normal controller integration or cross-family completion.']
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());folders=[];metrics=[]
for phase,version,execution in [(10,176,'35a29212-a6ea-4673-9710-70d121ff9273'),(11,177,'21a4819b-192f-4422-a1d7-493d0f6023c3')]:
 folder=p/f'lower-material-phase{phase}-v{version}';folders.append(folder);d=json.loads((folder/'inputs.json').read_bytes())
 for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
 assert sha(folder/'prompt.txt')==d['promptSha256']
 review=json.loads((folder/'package-review.json').read_bytes())
 assert all(review[k] for k in ['alphaExact','outerOnePixelRingExact','allRowsAbove181Exact','pairedBodyBelow110Exact'])
 review.update(disposition='retain_provisional_lower_finish',reviewedSourceBoards=['lower-detail-review.png','paired-lower-review.png'],findings=findings,nativeIncluded=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
 (folder/'package-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
 (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n',encoding='utf-8')
 row=progress['states'][phase];sources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']}
 if row['candidateSources']!=sources:row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
 row.update(candidateSources=sources,sourceAcceptance=False,reviewStatus='provisional_lower_finish_master_motion_pending')
 metrics.append(dict(phase=phase,admitted=review['admittedPixelCount'],outsideExact=review['outsideExactPixels'],luma=review['localLumaQuartilesAnd95']))
progress['lowerMaterialRefinementPhases']=sorted(set(progress['lowerMaterialRefinementPhases']+[10,11]));progress['nextVisualRepair']='Coordinate lower finish starting13 and remaining gait; continuous master anatomy/foot-contact review; normal carry lifecycle and all-family consistency'
assert progress['candidatePhases']==49 and not progress['remainingSourcePhases'];ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=86,nativeFailures=0,reviewedNativeCaptures=6,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='local-source-review.png',sourceIndices=[8,9,10,11,12,13],durationsMs=[30,20,20,20,20,20],findings=findings,metrics=metrics,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James carrying lower finish phases10 and11 neighbour review - October3,2026

V176phase10/V177phase11 retained provisionally after four source repair boards,
V178phase8..13 source board and all six paired native captures/four sizes were
visually reviewed. Fine hardware remains readable with softer toe/ankle highlights.
Phase13 original boots still brighter. Alpha, one-pixel rim, rows above181 and
paired body below110 exact; interior hardware is visually assessed, not pixel
protected anatomy.1030/1032admitted and64506/64504outside-exact pixels.

Local95thpercentile phase10:176.02to160.36; phase11:174.79to167.61.
Medians64.56to64.20 and67.00to70.26 respectively. No uniform darkening claim.
Lesson: restrained highlights alone do not prove matching midtones or temporal
continuity. Assess cloth/metal separately at actual size and against neighbours;
the provisional phase5 finish reference does not replace the original master.

V17886checks/0failures/sixcaptures, original30/20/20/20/20/20ms(130ms),
engine terminal, scratch APPDATA owner profile unchanged, frozen input/runtime
hashes stable. Ledger10/11 nowV176/V177, priorV107/V108 preserved.49/49candidate
coverage unchanged. Normal selection unchanged. HistoricalV173full-cycle evidence
is frozen to its earlier sources, not a full-motion validation of these repairs.
Continue lower finish13and remaining gait, continuous master anatomy/contact/
flash/seam review, normal carry lifecycle and full James cross-family polish.
Evidence: character/james-west-carry-walk-keys-v1/lower-window-v178/review.json.
'''
guides=record_guides(r,section,'### James carrying lower finish phase9 neighbour review')
handoff='''# Project handoff

Updated: October3,2026. Goal: full James animation library matching masters,
style/perspective/proportions/grade, followed by full cross-family consistency.
Goal active; source coverage does not establish final acceptance.

Accepted constraints: original master authority, matte warm charcoal/yellow/worn
metal, original pose/registration. Preserve owner profile and normal selection.

Changed: V176phase10/V177phase11 raw sources, paired protected candidates,
frozen prompts/references/package reviews; V178six-frame manifest/APNG/native
probe/paired UID/captures/evidence; lower helper phase10/11 mappings; ledger;
CURRENT_STATUS, pipeline, bible and repository/installed crew consistency skill.

Checks:86native/0failures/sixcaptures, exact original130mswindow; all six paired
captures/four sizes, four repair boards and six-frame source board visually reviewed.
Engine0/no timeout, scratch APPDATA owner profile unchanged, frozen hashes stable.
Full alpha/rim/upper rows preserved. New highlights softer; phase11midtones lighter.

Remaining: coordinate lower finish from13through rest of gait; continuous full49
master anatomy/contact/flash/seam review; versioned normal pickup/carry/turn/unload
integration and all-family consistency. No normal change or continuous acceptance.
V173full-cycle evidence remains specific to its frozen earlier source versions.
'''
for folder in folders+[out]:(folder/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in folders+[out] for f in root.rglob('*') if f.suffix.lower() in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(a[i+2]==b'lfs' for i in range(0,len(a)-1,3))
print(json.dumps(dict(retainedPhases=[10,11],checks=86,failures=0,reviewedCaptures=6,guides=guides,lfsRasters=len(rasters),normalChanged=False,goalComplete=False)))
