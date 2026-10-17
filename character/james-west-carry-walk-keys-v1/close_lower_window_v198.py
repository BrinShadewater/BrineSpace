from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'lower-window-v198';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(86,0,6)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
findings=['Four selected lower repairs retain readable articulated hardware/stride in eight selected source repair boards, six-frame source board and all six paired native captures/four sizes. Source review preceded native launch.', 'Initial phase21V192 still brighter than neighbours in V196 review and was superseded byV197 using original master plus explicitly provisional immediate phase20 material reference. V197midtones closer, strongest highlights still a little above neighbouring repairs; moving grade consistency remains open.', 'Phase21V197upper-tail177.41to170.58/median67.08to62.84;22V193177.88to164.13/64.06to63.55;23V194174.89to159.49/66.00to62.64;24V195173.65to157.92/63.00to58.50. Phase25original boots brighter. No uniform grade or measured25percent reduction claim.', 'Original alpha/one-pixel rim/rows above181/paired body below110 exact. Internal landmarks visually assessed, not original-master anatomy certification. Exact20/20/30/40/40/40ms finite190mswindow; not continuous49motion/no-flash/contact, normal lifecycle or all-family acceptance.']
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());folders=[];metrics=[]
spec=[(21,197,'4fc33e0c-1779-45e3-9569-2ffa17d1c4f0'),(22,193,'8b1ead21-f414-4be6-8414-1e85583f2f29'),(23,194,'e77f64e6-feee-4cfc-aaa3-2391b81c5e89'),(24,195,'7bbab244-9672-422f-bbcf-44896002df9d')]
for phase,version,execution in spec:
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
progress['lowerMaterialRefinementPhases']=sorted(set(progress['lowerMaterialRefinementPhases']+[21,22,23,24]));progress['nextVisualRepair']='Coordinate lower finish starting25 and remaining gait; moving grade review including phase21; full master anatomy/contact/seam review; normal carry lifecycle and all-family consistency'
assert progress['candidatePhases']==49 and not progress['remainingSourcePhases'];ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=86,nativeFailures=0,reviewedNativeCaptures=6,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='local-source-review.png',sourceIndices=[20,21,22,23,24,25],durationsMs=[20,20,30,40,40,40],findings=findings,metrics=metrics,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
previous=p/'lower-material-phase21-v192';d=json.loads((previous/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
assert sha(previous/'prompt.txt')==d['promptSha256']
f=previous/'package-review.json';review=json.loads(f.read_bytes());review.update(disposition='superseded_insufficient_neighbour_finish_match',reviewedSourceBoards=['lower-detail-review.png','paired-lower-review.png'],nativeIncluded=True,reason='V196source/native review shows stronger boot brightness than neighbouring repairs; V197immediate-neighbour finish remake selected provisionally.',sourceAcceptance=False,normalChanged=False);f.write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
(previous/'generation.json').write_text(json.dumps(dict(state='terminal_copied_superseded',execution='95844744-f629-46f7-9bd8-3ce262eaee95',rawSha256=sha(previous/'raw.png'),prompt='prompt.txt',inputs='inputs.json'),indent=2)+'\n',encoding='utf-8')
earlier=p/'lower-window-v196';en=json.loads((earlier/'native-evidence.json').read_bytes());ev=json.loads((earlier/'native_probe-validation.json').read_bytes());ef=json.loads((earlier/'inputs.json').read_bytes())
assert (en['checks'],en['failures'],en['captures'])==(86,0,6) and ev['realProfileUnchanged'] and ev['exitCode']==0 and not ev['timedOut'];assert all(sha(r/f)==h for f,h in ef['preLaunchSha256'].items())
(earlier/'review.json').write_text(json.dumps(dict(disposition='phase21_finish_mismatch_superseded_by_v198',nativeChecks=86,nativeFailures=0,reviewedNativeCaptures=6,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='local-source-review.png',reason='V192phase21brighter than neighbours; replaced withV197inV198. Original stride geometry retained.',continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
folders += [previous,earlier]
section='''### James carrying lower finish phases21 to24 with neighbour remake - October3,2026

V193phase22/V194phase23/V195phase24 and V197phase21 retained provisionally.
Eight selected source repair boards reviewed BEFORE native launch; V198phase20..25
source board/all six paired native captures at four sizes visually reviewed.
V192phase21 was still brighter in V196source/native review (all six captures
reviewed); superseded withV197. Original master plus provisional immediate phase20
finish reference used forV197; it is not a pose/master authority. Strongest21
highlights still slightly above neighbours, so moving grade review remains open.

Local95thpercentiles21:177.41to170.58;22:177.88to164.13;23:174.89to159.49;
24:173.65to157.92. Medians67.08to62.84,64.06to63.55,66.00to62.64,63.00to58.50.
Not uniform grade or measured25percent reduction. Original phase25boots brighter.
Selected admitted1011/1022/1007/1013; outside-exact64525/64514/64529/64523.
Full original alpha, one-pixel rim, rows above181 and paired body below110 exact.
Internal hardware landmarks visually assessed; no master anatomy acceptance.

V19886checks/0failures/sixcaptures, exact20/20/30/40/40/40ms(190ms)finite window,
engine terminal; scratch APPDATA owner profile unchanged, frozen hashes stable.
V196also86/0/six reviewed, but its frozen earlier21source is superseded. Ledger
21..24 nowV197/V193/V194/V195, priorV125/V126/V128/V129 preserved;49/49candidate
coverage unchanged. Normal selection unchanged. V173full-cycle evidence applies
to earlier frozen sources. Continue finish25and remaining gait, moving grade21,
full49master anatomy/contact/flash/seam, normal lifecycle and all-family polish.

Lesson: when a repair's strongest highlights improve only slightly, compare it
with the immediate neighbour before retaining it. A neighbour can guide finish
without replacing original master authority or transferring its pose. Review
boards must use the actual neighbour recorded in frozen inputs; package helper
now reads optional neighbour source/label rather than always displayingphase5.
Geometry-first prompt guidance added for future crops. No final goal acceptance.
Evidence: character/james-west-carry-walk-keys-v1/lower-window-v198/review.json.
'''
guides=record_guides(r,section,'### James carrying lower finish phases18 to20 neighbour review')
handoff='''# Project handoff

Updated: October3,2026. Goal: full master-matched James animation library, then
cross-family consistency/polish. Goal active; coverage is not final acceptance.

Constraints: master authority, matte charcoal/yellow/worn metal, original poses;
preserve owner profile and normal selection. Existing reversible work authorized.

Changed: selected V193phase22/V194phase23/V195phase24/V197phase21 raw/protected
paired sources and frozen prompts/references; V198six-frame native/APNG/evidence,
paired probe UID; supersededV192/V196review evidence; helpers (geometry-priority
prompt/mappings, actual neighbour in boards); ledger; status/pipeline/bible and
repository/installed crew reference. All selected raster exports covered by LFS.

Checks: V19886/0/six native captures/four sizes all reviewed;190msoriginal clocks,
engine0/no timeout, owner unchanged with scratch APPDATA, frozen hashes stable.
Eight selected source boards reviewed before native launch. V19686/0sixreviewed
showed brighter21; V197remake closer but its strongest highlights still elevated.

Remaining: lower finish25onward and moving grade21; continuous full49master
anatomy/contact/flash/seam; normal pickup/carry/turn/unload lifecycle and all-family
consistency. No normal change, continuous motion or final master acceptance.
'''
for folder in folders+[out]:(folder/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in folders+[out] for f in root.rglob('*') if f.suffix.lower() in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(a[i+2]==b'lfs' for i in range(0,len(a)-1,3))
print(json.dumps(dict(retainedPhases=[21,22,23,24],checks=86,failures=0,reviewedCaptures=6,guides=guides,lfsRasters=len(rasters),normalChanged=False,goalComplete=False)))
