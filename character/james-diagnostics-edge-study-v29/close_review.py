from pathlib import Path
import json,hashlib,subprocess,os,uuid,time
p=Path(__file__).resolve().parent;r=p.parents[1]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((p/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
validation=json.loads((p/'edge-study-validation.json').read_bytes());assert validation['exitCode']==0 and validation['realProfileUnchanged']
package=json.loads((p/'package-review.json').read_bytes());assert package['sourceFrames']==18 and package['originalAlphaRedBlueExact'] and package['outsideEdgeAdmissionExact']
review=dict(reviewedComparisonBoards=6,reviewedCandidateSources=18,visualReviewPending=False,sourceAcceptance=False,normalChanged=False,methodSuitableForFullCycleStudy=True,
    findings=['All six paired same-direction master/current/edge-study comparisons reviewed. Green hair/arm/backpack/boot edging reduced; interior suit shading/tablet/equipment retained.',
    'All18 source alpha/R/B bytes and all RGB outside edge admission exact. Green only decreases at strong green pixels with alpha<128 or alpha0 eight-neighbour contact. This is bounded numeric admission,not semantic classification.',
    'Full864frame V30 staging prepared from the same native material program, original endpoints excluded, integer slot filename formatting. Whole-cycle source and loader/room review remain pending.',
    'V29 package-review.json remains frozen historical packaging evidence because V30 input inventory references it; this separate visual review records later disposition. No revised normals installed.'],
    scope='Representative18frame native editable material study, not full-cycle or normal runtime acceptance.',fullGoalComplete=False)
(p/'review-acceptance.json').write_text(json.dumps(review,indent=2)+'\n')
rasters=[f.relative_to(r).as_posix() for f in p.rglob('*.png')]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert len(a)==len(rasters)*3+1 and all(x==b'lfs' for x in a[2:-1:3])
section='''### James diagnostic edge-material representative study — October 2, 2026

V29native edge-only green-channel material study:18South/North/West paired poses
reviewed in six master/current/candidate boards. Hair/arm/backpack/boot green
edging reduced without altering interior shading/tablet/equipment.36native checks
pass;independent all18source alpha/R/B and RGB outside byte-defined edge selector
exact. Selector:green>20and1.3timesbothR/B,alpha>0,andalpha<128or8-neighbour alpha0.
Not semantic segmentation;do not assume every intentional equipment color is
classified. Only admitted rendered green is exported;original R/B/alpha restored
to avoid changing other channels through native roundtrip quantization.
All frozen inputs stable,owner profile unchanged,scratch APPDATA,LFS checked.
Separate review-acceptance.json records visual disposition;package-review.json
remains frozen historical packaging evidence referenced by V30input inventory.
V30full864frame staging prepared using same method,master endpoints excluded,
integer slot filename formatting. No normal source/loader adoption yet. Whole-cycle
source/material/helmet/clock/pivot and actual loader/room checks remain required.
Keep laterV26East correction and deliberate helmet meal aliases when packaging
shared continuity override. Cargo joins/full cardinal/context acceptance open.
Evidence:character/james-diagnostics-edge-study-v29/review-acceptance.json;
full staging:character/james-diagnostics-edge-matte-v30/inputs.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
 r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 for attempt in range(3):
  old=f.read_bytes();entry=section.encode()
  if entry.split(b'\n',1)[0] in old:break
  if f.name=='CURRENT_STATUS.md':at=old.index(b'### James remaining diagnostics source comparisons');new=old[:at]+entry+b'\n'+old[at:]
  else:new=old+b'\n'+entry
  temp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
  try:assert f.read_bytes()==old;os.replace(temp,f);break
  except PermissionError:
   temp.unlink()
   if attempt==2:raise
   time.sleep(2)
(p/'HANDOFF.md').write_text('''# Project handoff

## Objective and acceptance
Full James master-matched set/cardinal/cross-family polish. Incomplete.

## Accepted decisions
Authored poses/alpha/clock/master endpoints/selected V26East colors retained.
Tablet faces James,wrench stays holstered. Native material program only edge green.

## Current state
18representative pairedSouth/North/West edge studies retained as method study:
six comparison boards reviewed,green edging reduced. V30full864frame staging
prepared and launched. No normal adoption or new animation motion.

## Verification
36native checks0fail,whole owner profile unchanged/scratchAPPDATA. Independent
18source alpha/R/B/outside mask exact. Frozen inputs stable,LFS and five guides
updated. Separate review-acceptance.json is visual disposition;package-review
is frozen historical source forV30,do not mutate it to update review status.

## Next action
Inspect authoritative V30 native process/evidence,never relaunch from stale intent.
Then package/verify all864frames/master endpoints/clocks/pivots/helmet differences,
whole-cycle source review,actual loader/room before adoption. Retain laterV26East
override and original meal aliases. Cargo joins/full context acceptance remain open.
''',encoding='utf-8')
for f in [r/'character/james-west-carry-walk-keys-v1/HANDOFF.md',r/'character/james-full-set-review-2026-10-02/HANDOFF.md']:
 old=f.read_text(encoding='utf-8');marker='## V29 edge-material study\n'
 if marker not in old:
  at=old.index('## Next action\n');old=old[:at]+marker+'''18paired edge studies reviewed in six boards;green edging reduced,alpha/R/B and
outside edge selector exact.36native checks0,ownerprofile unchanged,all guides/LFS
updated. V30full864frame staging launched;inspect actual process/evidence next.
No normal adoption. See character/james-diagnostics-edge-study-v29/HANDOFF.md.

'''+old[at:];f.write_text(old,encoding='utf-8')
print(json.dumps(dict(reviewedCandidates=18,reviewedBoards=6,nativeChecks=36,guides=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
