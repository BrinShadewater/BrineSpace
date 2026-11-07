"""Bind whole-source join authoring to current native and interruption evidence."""
from pathlib import Path
from PIL import Image
import json,hashlib,ast,subprocess,shutil
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-walk-joins-v1';N=D/'native-motion-v2';O=R/'output/bill-east-walk-join-native-v2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8'))
review=read(D/'review.json');native=read(N/'review.json');v=read(N/'validation.json');assert v['passed'] and not v['inputChanges'] and not v['ownerChanges']
for mapping in [review['inputs'],review['sourceWalkInputs']]:assert all(sha(Path(p))==h for p,h in mapping.items())
frozen=read(N/'inputs-before.json')
for p in [R/'scripts/grid_canvas.gd',R/'tools/bill_east_walk_join_candidate_v1.gd',R/'tools/bill_east_walk_join_candidate_v1.gd.uid']:assert sha(p)==frozen[str(p)]
for slot in [0,12,24,36]:
 S=D/f'settle-{slot:03}';prov=read(S/'provenance.json');assert sha(S/'raw.png')==prov['rawSha256'] and sha(S/'prompt.txt')==prov['promptSha256'] and sha(Path(prov['generatedPath']))==prov['rawSha256']
 for ref in prov['references']:assert sha(Path(ref['path']))==ref['sha256'] and sha(Path(ref['source']))==ref['sourceSha256']
decoded=[]
for variant in ['candidate','selected']:
 records=[r for r in native['records'] if r['variant']==variant];groups=[]
 for rec in records:
  path=O/rec['worldFile'];assert sha(path)==rec['worldSha256'];pixels=Image.open(path).convert('RGBA').crop(tuple(native['crop'])).tobytes()
  if groups and groups[-1][0]==pixels:groups[-1][1]+=rec['durationMs']
  else:groups.append([pixels,rec['durationMs']])
 for speed in [1,4]:
  with Image.open(N/f'{variant}-{speed}.png') as im:
   assert im.n_frames==len(groups);duration=0
   for i,(pixels,ms) in enumerate(groups):
    im.seek(i);assert im.convert('RGBA').tobytes()==pixels and im.info['duration']==ms*speed;duration+=im.info['duration']
   decoded.append(dict(path=f'{variant}-{speed}.png',frames=im.n_frames,durationMs=duration))
branches=read(R/'output/bill-walk-join-branches-v1/verification.json');assert branches['passed'];shutil.copyfile(R/'output/bill-walk-join-branches-v1/verification.json',D/'branch-verification.json')
tools=['prepare_bill_walk_join_sources_v1.py','build_bill_walk_join_sources_v1.py','prepare_bill_east_walk_join_native_v1.py','prepare_bill_east_walk_join_native_v2.py','run_bill_east_walk_join_native_v1.py','run_bill_east_walk_join_native_v2.py','run_bill_walk_join_branches_v1.py','prepare_bill_join_native_publisher_v1.py','prepare_bill_join_native_publisher_v2.py','publish_bill_walk_joins_native_v1.py','publish_bill_walk_joins_native_v2.py','record_bill_walk_join_milestone_v1.py']
for name in tools:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
gds=['bill_east_walk_join_candidate_v1.gd','test_bill_walk_join_candidate_v1.gd','review_bill_east_walk_join_native_v1.gd','review_bill_east_walk_join_native_v2.gd','ensure_bill_east_walk_join_native_v1_uids.gd','ensure_bill_east_walk_join_native_v2_uids.gd'];ids=[(R/'tools'/(name+'.uid')).read_text().strip() for name in gds];assert len(set(ids))==len(ids)
pngs=list(D.rglob('*.png'));result=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(p.relative_to(R).as_posix() for p in pngs)+'\0').encode(),cwd=R,capture_output=True,check=True);fields=result.stdout.split(b'\0');assert len(fields)==len(pngs)*3+1 and all(fields[i]==b'lfs' for i in range(2,len(fields)-1,3))
native.update(status='current_join_navigation_and_branch_checks_pass',visualReviewed=True,fullVisualAcceptance=False,normalAdmission=False,decodedAPNG=decoded,pageHashes={p:sha(N/p) for p in native['pages']},browserScreenshotSha256=sha(N/'browser-quarter.png'),visualFindings='All four same-source route comparison pages and normal/quarter browser snapshots inspected. New first-step middle and stop middle reduce direct standing/extended-stride changes. Matte detail and warmer face remain visible; slight head/collar/boot differences persist. This is scoped pose/capture review, not continuously watched full-library motion acceptance.')
(N/'review.json').write_text(json.dumps(native,indent=2)+'\n',encoding='utf-8')
review.update(status='whole_join_candidate_scoped_native_pass',visualReviewed=True,nativeTested=True,normalAdmission=False,fullVisualAcceptance=False,nativeChecks=4064,branchChecks=536,visualFindings='Four whole raws, full walk/middle/idle/density board and eight native comparison pages inspected. Intermediate poses narrow stride without ghost limbs or component splicing. Heights145/149/143/149,sole224all4. New faces/collars/boots remain subtly variable. NativeV2 uses same master gait/idle banks with joins on/off.',openIssues=['Normal admission and real equipment/water/death/reset dispatch remain untested; provider is explicitly installed only in bare East fixture.','Neighbor joins to run/carry/work and full-library master acceptance remain.','No autonomous goals, fresh fullSave/TitleContinue or continuous-cadence/2Dplanted-foot certification.'])
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
validation=dict(passed=True,authoredWholePoses=4,poseHeights=[r['height'] for r in review['records']],soleY=[r['bounds'][3] for r in review['records']],nativeChecks=4064,nativeFailures=0,nativeInputCount=4846,inputChanges=[],ownerNonLogCount=2931,ownerChanges=[],branchChecks=536,branchFailures=0,decodedAPNG=decoded,pythonSyntaxFiles=len(tools),newGDUidPairs=len(gds),pngLfsCount=len(pngs),normalAdmission=False,fullVisualAcceptance=False)
(D/'validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
note=f'''

## Bill East whole-figure first-step/stop joins — October4,2026

`character/bill-east-walk-joins-v1/` adds four built-in authored half-settled
whole poses from walk anchors0/12/24/36 toward the exact current idle endpoint.
Four jobs terminal, raws saved immediately with generation/receipt/prompt/ref
hashes; original-master identity and same1024physical-profile references retained.
Initial idle-reference preparation incorrectly resized raw1254 into184profile;
detected during pre-submit image inspection, corrected to exact current184idle
canvas inside common256profile BEFORE any generation. No output used bad reference.
Uniform256packing and lossless whole Yregistration2/0/3/0; occupied heights
145/149/143/149,sole224all4, no anatomical fitting/head stamp/local grading or
crossfade ghosts. All whole raws and full walk/middle/idle/density board inspected.
Existing48master gait sources and2000ms timing remain byte unchanged.

`tools/bill_east_walk_join_candidate_v1.gd` is an opt-in provider through the
small nullable `human_walk_join` hook in grid_canvas.gd (normal defaultnull).
First step holds standing<45ms then authored middle to130ms before rejoining
the continuously distance-driven gait. Stop holds exact last displayed pose30ms,
then closest quarter-stride middle until140ms before live idle. Foot/path/speed
and underlying gait clock unchanged. Short moves stopped before visible first
step cancel without a phantom step; restarting during settle retains the current
displayed pose and branch. No normal loader/source selection change or art preload.

NativeV1 current-art-with-joins versus older selected art:4064checks0,4828inputs
unchanged,92.62s. V2 after interruption fixes isolates join effect with identical
current master gait/idle art for joined/unjoined controls:4064checks0,94.85s,
4846inputs unchanged;320unit legal ColdStore route,348steps/6.96s pervariant,
all48gait poses displayed,190actual world/source capture pairs. Both native runs
engine0/noERROR/WARNING;2931owner non-log hashes unchanged under scratchAPPDATA.
All eight full native comparison pages and current normal/quarter browser snapshots
inspected. {sum(d['frames'] for d in decoded)}current native APNG decoded frames exactRGBA/timing.
Targeted isolated headless checks536/0 cover all48stop phases, repeat-at-paused-time,
restart during settle, tiny-move cancellation and direct provider gear/water/
other-state bypass. That bypass is provider-unit evidence, not actual equipped/
water/death renderer dispatch acceptance (those paths may return before this hook).
{len(tools)}Python syntax,{len(gds)}new paired uniqueGDUIDs,{len(pngs)}PNG LFS checked.

Visual outcome: smaller first-step/standing changes without changing the walking
art; current matte detail/warm face survive. Small face/collar/boot differences
remain provisional. Source/capture/branch review does not certify continuously
watched full cadence or2Dplanted feet. Normal family admission, run/carry/work
boundaries, actual context cancellation/equipment/water dispatch, autonomous jobs,
fresh fullSave/TitleContinue and remaining West/cardinal/life/hazard/cargo master
closeout still open. No commit/export. Full Bill objective incomplete; authorized
work continues. Handoff:character/bill-east-walk-joins-v1/HANDOFF.md.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths += [root/'references/crew-consistency.md',root/'references/source-density.md']
for path in paths:
 with path.open('a',encoding='utf-8') as out:out.write(note)
handoff='''# Project handoff

Updated: October4,2026 · Project: Brine Space · Task: Bill first-step/stop joins

## Objective and acceptance
Finish consistent Bill animation library soon. First-step/arrival pose jump now
has authored whole-source easing; full-library/native-context acceptance pending.

## Accepted decisions and constraints
Preserve48whole walk poses,2000ms gait, actual distance-driven movement and master
matte identity. No component splicing/ghost crossfades. Reversible work authorized;
normal sources remain selected pending family boundaries. No commit/export.

## Current state
Four authored settling poses/raw receipts/frames/manifest/whole comparison here.
native-motion-v2 is current same-art joined/unjoined game-rendered comparison.
Opt-in helper in tools/bill_east_walk_join_candidate_v1.gd; small nullable hook
in scripts/grid_canvas.gd, defaultnull in normal game. Short-move cancellation
and settle-restart continuity handled; no actor/path/clock changes.

## Verification
Four raws/whole board/eight native pages/browser snapshots inspected. Pose heights
145/149/143/149,sole224all4; full48source hashes/timing unchanged. NativeV2 actual
Bill.update/move/arrive/distance renderer4064checks0,4846inputs/2931owner files
unchanged,scratchAPPDATA,190captures,all48gait poses. Headless536checks0 covers
all48stop phases/pause/restart/short cancellation/provider context bypass.
Current native APNGs pixel/timing exact,12Python syntax,6GDUID pairs,PNG LFS.
Scoped review, not full continuous cadence/2Dfeet or actual equipment dispatch.

## Next action
Close actual renderer context reset/bypass and East run/carry/work boundaries,
then normal East family admission. Continue remaining West/cardinal/equipment/
water/life/hazard/cargo master checks and full station jobs/save/TitleContinue.
Do not regenerate accepted48walk poses or repeat unrelated UI tests.
'''
(D/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (R/'character/bill-east-walk-navigation-v1/HANDOFF.md').open('a',encoding='utf-8') as out:out.write('\n\nOctober4 continuation: authored first-step/stop joins now have scoped native/branch passes in ../bill-east-walk-joins-v1/HANDOFF.md. Current same-source comparison in native-motion-v2; normal/context admission remains open.\n')
print(json.dumps(validation))
