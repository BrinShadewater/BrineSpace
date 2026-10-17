from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'local-window-v144';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((o/'native-evidence.json').read_bytes());v=json.loads((o/'native_probe-validation.json').read_bytes());d=json.loads((o/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(73,0,5)
assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in d['preLaunchSha256'].items())
m=json.loads((o/'bare-manifest.json').read_bytes())['states'][0];assert m['sourceIndices']==[30,31,32,33,34] and m['frameDurationsMs']==[40]*5
new=p/'local-material-phase33-v143';knee=p/'knee-protection-phase30-v142';i=json.loads((new/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in i[group].items())
assert sha(new/'prompt.txt')==i['promptSha256']
(new/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='7c790899-bba1-46ab-ba3c-af19e0ec00e0',rawSha256=sha(new/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
findings=['Phase30 original knee fitting and buffer restored exactly; surrounding V138 fabric unchanged. This fixes generated drift relative to same-phase source, not master anatomy acceptance.','Phase33 fitting highlights subdued and quilt retained. Source crop and paired boards visually reviewed. Head, outer silhouette and boots protected; internal landmarks remain provisional.','All five paired native captures at four sizes and source window reviewed; unrepaired34 retains stronger fittings and original lower highlights differ.','Static review does not establish absence of flashes, full continuous gait, complete master proportions or normal lifecycle acceptance.']
for folder,boards in [(new,['crop-detail-review.png','paired-local-review.png']),(knee,['knee-before-review.png','knee-after-review.png'])]:
    report=json.loads((folder/'package-review.json').read_bytes());report.update(reviewedSourceBoards=boards,visualReviewer='Codex',findings=findings,nativeIncluded=True,disposition='retain_provisional_candidate');(folder/'package-review.json').write_text(json.dumps(report,indent=2)+'\n')
j=json.loads((p/'material-repair-progress.json').read_bytes())
for phase,folder in [(30,knee),(33,new)]:
    row=j['states'][phase]
    if not row['repairCandidateAvailable']:j['remainingSourcePhases'].remove(phase);j['candidatePhases']+=1
    if 'candidateSources' in row:row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
    row.update(repairCandidateAvailable=True,sourceAcceptance=False,reviewStatus='provisional_material_master_contact_motion_pending',candidateSources={mode:dict(file=(folder/f'{mode}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{mode}-head-protected.png')) for mode in ['bare','helmet']})
assert j['candidatePhases']==39 and len(j['remainingSourcePhases'])==10
j['nextVisualRepair']='Phase34/35 and remaining sources, lower finish, full gait and normal lifecycle, all-family master consistency'
(p/'material-repair-progress.json').write_text(json.dumps(j,indent=2)+'\n')
(o/'review.json').write_text(json.dumps(dict(nativeChecks=73,nativeFailures=0,pairedSources=10,sourceIndices=[30,31,32,33,34],durationsMs=[40]*5,reviewedNativeCaptures=5,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='local-source-review.png',findings=findings,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
section='''### James knee fitting protected and carrying coverage extends through phase33 — October 3, 2026

V142 restores phase30 original knee fitting plus buffer (rectangle108,157..127,183),
256 pixels changed per gear variant versus V138; all outside pixels remain exact.
This is deterministic source protection, not new generated art or master anatomy
acceptance. Before/after full-figure and knee crops reviewed. Original fitting
brightness is retained rather than admitting a reshaped generated plate.

V143 phase33 body material source generated with frozen original pose and master
textile references. Both source boards reviewed;2557 admitted pixels,62979 outside
exact. Original alpha/two-pixel rim/head above110/boots from200 down and paired body
below110 exact. Fine quilt retained and fitting highlights subdued; interior
landmarks remain provisional. V144 window30..34,40ms each,total200ms:73 native
checks/0failures/5paired four-size captures and source window visually reviewed.
Frozen inputs/runtime/registry and owner profile unchanged; scratch APPDATA only.
Ledger39/49 provisional source phases,10remaining; normal selection unchanged.

Lesson: outer-alpha protection cannot preserve internal hardware contours. Restore
original same-phase fitting pixels with a surrounding buffer when a material edit
changes the fitting; disclose retained brightness rather than claiming full finish
acceptance. Next34/35and remaining sources, lower finish coordination, full moving
gait and normal lifecycle integration; master proportions/perspective/colour and
all-family consistency/polish remain incomplete. Static captures do not prove
absence of flashing or continuous motion. Evidence:character/james-west-carry-walk-
keys-v1/local-window-v144/review.json.
'''
guides=record_guides(r,section,'### James carrying coverage extends through phase32 with knee-detail flag')
handoff='''# Project handoff

Updated: October3,2026. Task: full James master-matched animation library and polish.

## Objective and acceptance
Complete all animation families matching masters in art, colour, proportions,
perspective, size and height; verify full motion, normal integration and polish.

## Accepted decisions and constraints
Original masters govern. Reversible source repair authorized; keep owner saves,
normal selection and other characters unchanged. Test success is not art acceptance.

## Changed files and current state
V142 phase30 knee protection, V143 phase33 material source, V144 neighbour review,
ledger and five pipeline/status/bible/skill guides.39/49 candidates,10remaining.

## Verification
73checks,0failures;5paired four-size captures and source boards reviewed. Owner
profile and frozen runtime/input hashes unchanged. No full motion acceptance.

## Remaining work
Remaining sources and lower finish; full gait, normal carrying lifecycle, all
families compared to original masters and full consistency/polish acceptance.

'''
for folder in [knee,new,o]:(folder/'HANDOFF.md').write_text(handoff+section)
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in [knee,new,o] for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert len(a)==3*len(rasters)+1 and all(x==b'lfs' for x in a[2:-1:3])
print(json.dumps(dict(candidates=39,remaining=10,nativeChecks=73,failures=0,reviewedCaptures=5,guides=guides,lfsRasters=len(rasters))))
