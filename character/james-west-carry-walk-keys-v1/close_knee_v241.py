from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];folder=p/'knee-material-phase30-v240';out=p/'lower-window-v241';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(73,0,5)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
d=json.loads((folder/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
assert sha(folder/'prompt.txt')==d['promptSha256']
review=json.loads((folder/'package-review.json').read_bytes());assert all(review[k] for k in ['alphaExact','outerOnePixelRingExact','outsideRectangleExact','pairedBodyBelow110Exact'])
findings=['Raw and knee-detail/paired-neighbour source boards visually reviewed before native launch. No added prominent fasteners; near-knee placement/outline and leg overlap retained provisionally.', '292 original opaque interior pixels admitted in restored knee rectangle;65244 outside pixels and all alpha/rim exact. Local median73.07to71.93 and95th184.13to147.30; quieter highlight, not proof of complete master grade.', 'Five paired native captures at four sizes and local source board reviewed. Static knee sequence closer in brightness; continuous full49 grade/contact/proportion and normal lifecycle acceptance remain open.']
review.update(disposition='retain_provisional_knee_finish',reviewedSourceBoards=['knee-detail-review.png','paired-neighbor-review.png'],findings=findings,nativeIncluded=True)
(folder/'package-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
(folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='1f31e081-b3dd-4ae0-9933-fc2ca1292bc6',rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',referenceRoles=['edit-target','master-metal-reference']),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());row=progress['states'][30];sources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']}
if row['candidateSources']!=sources:row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
row.update(candidateSources=sources,sourceAcceptance=False,reviewStatus='provisional_knee_finish_master_motion_pending')
progress['nextVisualRepair']='Freeze current49 including opening and knee finish; continuous original-master grade/proportions/perspective/contact/seam review, versioned normal cargo lifecycle and all-family consistency'
ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=73,nativeFailures=0,pairedSources=10,reviewedNativeCaptures=5,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],sourceIndices=[28,29,30,31,32],durationsMs=[40]*5,findings=findings,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James restored knee finish candidate retained - October3,2026

V240 phase30 knee finish retained provisionally after raw and two repair boards
visually reviewed BEFORE native launch. Motif-free original-master surface sample
avoids previous brass-fastener transfer.292 opaque interior pixels admitted within
original restored knee rectangle108/157/127/183;65244 outside pixels, alpha/rim
and shared paired body exact. Existing fitting position and leg overlap retained
visually; alpha alone is not anatomy acceptance. Median73.07to71.93,
95th184.13to147.30 for the same admitted interior; quieter knee highlight.

V241 phases28..32 five40ms poses200ms:73 native checks/0 failures/5 paired
captures, ten frozen sources. Source board and both native four-size boards
reviewed; owner profile unchanged, input hashes stable. Ledger30 upgradesV205
toV240 with history; original anatomical restoration preserved as source evidence.
Lesson: a motif-free material sample plus narrow fixed admission can reduce
highlight drift without transferring conspicuous hardware, but actual interior
construction and neighbouring motion must still be reviewed.
Next freeze current49 including opening/knee refinements and review full motion
against original master for grade/proportions/perspective/contact/seam, then
versioned normal cargo lifecycle and all-family consistency/polish. Normal
selection unchanged; broad objective incomplete. Evidence:
character/james-west-carry-walk-keys-v1/lower-window-v241/review.json.
'''
guides=record_guides(r,section,'### James knee material reference contamination rejected')
handoff='# Project handoff\n\n'+section+'\nChanged: V240 references/prompt/raw/protected paired sources; V241 manifests/APNG/native probe and UID/captures; ledger30 and five guides. Checks and remaining work above.\n'
for f in [folder,out]:(f/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in [folder,out] for f in root.rglob('*') if f.suffix.lower() in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(a[i+2]==b'lfs' for i in range(0,len(a)-1,3))
print(json.dumps(dict(retainedPhase30=240,checks=73,failures=0,reviewedCaptures=5,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
