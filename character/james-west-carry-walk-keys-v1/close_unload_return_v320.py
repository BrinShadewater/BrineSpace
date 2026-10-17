from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-return-original-v320';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());f=json.loads((o/'native-inputs.json').read_bytes())
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert(n['checks'],n['failures'],n['captures'])==(69,0,7)
assert all(sha(r/x)==h for x,h in f['preLaunchSha256'].items())
inputs=json.loads((o/'inputs.json').read_bytes());assert all(sha(r/x)==h for x,h in inputs['references'].items());assert sha(o/'prompt.txt')==inputs['promptSha256'];assert sha(r/inputs['originalTarget'])==inputs['originalTargetSha256']
g=json.loads((o/'generation.json').read_bytes());assert sha(o/'raw.png')==g['rawSha256']
m=json.loads((o/'bare-review-manifest.json').read_bytes());s=m['states'][1];old=json.loads((p/'north-unload-rise-between-v317/bare-review-manifest.json').read_bytes())['states'][1]
assert all(s['frameFiles'][i]==old['frameFiles'][i] for i in [0,1,2,3,5,6]);assert s['frameDurationsMs']==old['frameDurationsMs'];assert sum(s['frameDurationsMs'])==520
dec=Image.open(o/'bare-unload-study.apng');assert dec.n_frames==7
for i,src in enumerate(s['frameFiles']):
 dec.seek(i);assert np.array_equal(np.asarray(dec.convert('RGBA')),np.asarray(Image.open(r/src[6:]).convert('RGBA')));assert dec.info['duration']==s['frameDurationsMs'][i]
measure=json.loads((o/'source-measurements.json').read_bytes());assert measure['sources'][4]['boundsAlpha128']==[90,107,165,225]
review=dict(disposition='diagnostic_original_pose_return_not_selected',rawAndFullChronologyReviewed=True,nativeCapturesReviewed=7,nativeChecks=69,nativeFailures=0,decodedApngExact=7,totalMs=520,normalChanged=False,selected=False,sourceAcceptance=False,fullGoalComplete=False,findings=['Original unload4 geometry plus original master cloth reference retains crown107; sole225 versus original224, width75 versus original73. This is near original registration, not exact joint/foot preservation.', 'Cleaned source edge rendering and finer visible detail, but hard diamond quilt and bright metal bands remain. Body/head/backpack appearance still changes toward slimmer317 rise. Material-only prompt preserves bent registration better than319 neighbor transfer, but does not solve cross-pose master fidelity.', '69native checks0, all7static native phases viewed at148/82/54/27; owner profile unchanged and frozen hashes stable.7APNG source pixels/clocks exact at520ms. No advancing browser320 playback or actual arrival-controller proof.', '320 is an alternative diagnostic bank.317 remains current provisional review candidate. No helmet or normal adoption; unload support/material/rise/case joins, full cargo/arrival lifecycle and all-family consistency remain.'])
(o/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';before=ledger.read_bytes();d=json.loads(before)
d['northUnloadOriginalReturnTrial']=dict(version=320,file=(o/'review.json').relative_to(r).as_posix(),disposition=review['disposition'],nativeChecks=69,nativeFailures=0,selected=False,normalChanged=False)
d['nextVisualRepair']='320 original-geometry material edit retains crown107 with1px sole drift, unlike3196px float. Original geometry plus actual master cloth reference is the safer source basis, but hard quilt/bright bands and4-to5 body/gear change remain.320 not selected;317 current review candidate. Refine matching garment/hardware identity across bent return and rise, then advancing playback and helmet; cargo stop/turn/arrival integration, lifecycle and all-family master polish remain.'
assert ledger.read_bytes()==before;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James original-pose unloading return comparison - October3,2026

V320 built-in transparent surface edit starts from exact original unload4 enlarged
whole canvas, with actual original West master quilt crop as appearance reference.
Inputs/prompt frozen, raw1254 saved, whole nearest256 once. Crown107 matches
original; sole225 versus224, width75 versus73. Near registration is not exact
joint/support preservation. Raw/full seven-pose chronology and all7native captures
at148/82/54/27 viewed.69checks0, owner profile unchanged/frozen hashes stable;
7APNG source pixels/clocks exact, original520ms. Only candidate slot4 differs.
No advancing320 browser playback or actual arriving-controller proof. Hard diamond
quilt/bright bands and body/head/backpack change into slimmer317 remain.320 retained
as diagnostic alternative, not selected;317 provisional bank and normal unchanged.

Lesson: original-pose geometry plus a material-only master reference avoids the
large floating-foot change of appearance-neighbor transfer, but technical source
registration does not establish master surface or cross-pose character identity.
Compare garment stitch shape, hardware construction and body bulk across bent and
rise phases before choosing a replacement; don't admit it because69checks pass.
Next material/gear continuity repair, then advancing playback and shared helmet.
Full cargo/arrival integration, lifecycle and all-family consistency remain open.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-return-original-v320/HANDOFF.md.
'''
guides=record_guides(r,section,'### James unloading appearance-transfer rejection - October3,2026')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James unloading return

## Objective and acceptance
Full master-matched James set, actual integration and all-family consistency.
Source registration, runtime checks and visual acceptance are separate evidence.

## Accepted decisions and constraints
Matte master fabric/gear, wrench on belt, empty return hands, floor case in front
between legs, natural bend with stable support. No procedural body correction.

## Current state
320 frozen original-pose/master-cloth inputs and prompt, builtin raw/receipt,
whole256 source, alternative7-pose manifest/APNG/chronology/measurements, native
probe/UID/evidence and7captures/3boards. Ledger and five guides updated.320 is
diagnostic and unselected;317 current provisional bank, normal game unchanged.

## Verification
Raw/chronology/all7native four-size captures viewed.69checks0, scratch owner
unchanged, frozen hashes stable,7APNG frames/clocks exact520ms. Crown107 matches
original but sole1px lower and width2px greater. Hard quilt, bright bands and
return-to-rise body/head/backpack change remain. No new live motion observation.

## Next action
Repair matching garment/hardware identity across return/rise from original
geometry/master appearance. Advancing playback, support/rise/case joins, helmet,
carry-to-turn and actual arrival selection, normal lifecycle/Continue/interruptions
and all-family polish remain. Full goal active; no external blocker.
''',encoding='utf-8')
with(p/'HANDOFF.md').open('a',encoding='utf-8') as stream:stream.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in o.iterdir() if f.suffix in('.png','.apng')]
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(checks=69,failures=0,capturesReviewed=7,decodedExact=7,totalMs=520,guides=guides,lfsRasters=len(rasters),selected=False,normalChanged=False,fullGoalComplete=False)))
