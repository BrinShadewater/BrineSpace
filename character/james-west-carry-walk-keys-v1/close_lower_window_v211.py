from pathlib import Path
import json, hashlib, subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'lower-window-v211'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(73,0,5)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
findings=['Phase33 raw/protected crop and paired source boards visually reviewed before native launch; toe/heel and ankle arrangement retained provisionally. Local median64.21to61.67 and95th156.17to155.92: small finish change, not a measured quarter reduction.', 'Phase34V210 rejected at source review: generated boot angles, toe positions and ankle construction shifted; original-alpha admission fragments the moved interior. Not included in native window or ledger.', 'All five phase31..35 paired native captures at four sizes and source window reviewed. Original34/35 retain brighter toe highlights. Continuous moving grade, master anatomy/contact and full49 motion acceptance remain open.']
for phase,version,execution,disposition in [(33,209,'92badfee-37e2-45f7-87f2-e567cb9a5bba','retain_provisional_lower_finish'),(34,210,'1a985e29-9d0d-493f-a65e-dc611653b48a','reject_internal_boot_geometry_drift')]:
 folder=p/f'lower-material-phase{phase}-v{version}';d=json.loads((folder/'inputs.json').read_bytes())
 for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
 assert sha(folder/'prompt.txt')==d['promptSha256']
 review=json.loads((folder/'package-review.json').read_bytes())
 review.update(disposition=disposition,reviewedSourceBoards=['lower-detail-review.png','paired-lower-review.png'],findings=findings,nativeIncluded=phase==33,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
 (folder/'package-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
 (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',disposition=disposition),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());folder=p/'lower-material-phase33-v209';row=progress['states'][33]
sources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']}
if row['candidateSources']!=sources:row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
row.update(candidateSources=sources,sourceAcceptance=False,reviewStatus='provisional_lower_finish_master_motion_pending')
progress['lowerMaterialRefinementPhases']=sorted(set(progress['lowerMaterialRefinementPhases']+[33]))
progress['nextVisualRepair']='Remake phase34 lower finish from original pose; remaining gait finish and continuous master anatomy/contact/grade review, normal lifecycle and all-family polish'
ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=73,nativeFailures=0,reviewedNativeCaptures=5,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],sourceIndices=[31,32,33,34,35],durationsMs=[40]*5,findings=findings,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='### James carrying phase33 finish and phase34 geometry rejection - October3,2026\n\nV209phase33 retained provisionally after raw/protected and paired source review.\n1008 admitted pixels,64528 outside exact; alpha/rim/rows above181 and paired lower\nbody exact. Local median64.21to61.67/95th156.17to155.92: modest material change.\nV210phase34 rejected BEFORE native launch for shifted boot angles/ankles/toes;\noriginal alpha masks cannot rescue moved interior construction. Prior phase34\nV145 remains selected. Lesson: verify raw landmarks and protected composite\nindependently; even a darker crop can fragment boots after alpha admission.\n\nV211phase31..35 five40ms sources200ms:73 native checks,0 failures,5 paired\nfour-size captures, source board and both packed native boards visually reviewed.\nScratch APPDATA owner profile unchanged; frozen inputs stable. Original34/35 toe\nhighlights brighter. Ledger33 upgraded fromV143 toV209;49 candidate coverage\nunchanged. Full49 moving grade/master anatomy/contact/seam, phase34 remake and\nremaining finish, normal lifecycle and all-family consistency remain open.\nNormal selection unchanged; no full source/goal acceptance. Evidence: character/\njames-west-carry-walk-keys-v1/lower-window-v211/review.json.\n'
guides=record_guides(r,section,'### James carrying lower finish phases29 to32 preserves restored knee')
handoff='# Project handoff\n\nObjective: full James set matching original masters, then cross-family polish.\nGoal active/incomplete.\n\nChanged: V209phase33 retained raw/protected sources and ledger; V210phase34\nrejected source evidence; V211 paired five-frame review manifests/APNG/native\nprobe and UID/captures; status/pipeline/bible/repository and installed skill notes.\n\nChecks:73 native/0/5 captures; original200ms window; source/native boards reviewed;\nowner profile unchanged; frozen hashes stable. Fixed silhouettes do not certify\ninterior anatomy or full motion.\n\nRemaining: remake34 preserving exact boot landmarks, remaining lower finish, full\n49 moving grade/contact/master review, versioned normal carrying lifecycle and\nall-family consistency. No normal selection change.\n'
for name in ['lower-material-phase33-v209','lower-material-phase34-v210','lower-window-v211']:(p/name/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for name in ['lower-material-phase33-v209','lower-material-phase34-v210','lower-window-v211'] for f in (p/name).rglob('*') if f.suffix.lower() in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert all(a[i+2]==b'lfs' for i in range(0,len(a)-1,3))
print(json.dumps(dict(retained=[33],rejected=[34],nativeChecks=73,failures=0,reviewedCaptures=5,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
