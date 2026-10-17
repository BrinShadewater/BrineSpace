from pathlib import Path
import hashlib,json,subprocess,os,uuid,time
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-full-set-review-2026-10-02/diagnostics-v28'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
d=json.loads((out/'review.json').read_bytes());assert all(sha(r/f)==v for f,v in d['sourceSha256'].items());assert len(d['records'])==60
edges=json.loads((out/'edge-diagnostic.json').read_bytes());assert all(sha(r/f)==v for f,v in edges['sourceSha256'].items());assert len(edges['records'])==864
d.update(visualReviewPending=False,reviewedBoards=12,reviewedSourceSlots=60,sourceAcceptance=False,normalChanged=False,
    findings=['All12 whole/enlarged boards reviewed, South/North/West9distributed phases pergear plusidle. Hair/fabric colors generally track same-direction masters more closely than pre-V26 East; no blanket violet correction justified by this sample.',
    'Green edging visible around several animated hair/arm/backpack silhouettes. Read-only diagnostic covers864sourceframes;most strong-green pixels border alpha0 or have alpha<128. Threshold flags are not semantic evidence that every green pixel should change.',
    'All three directions share the selected James inspection material continuity manifests. Preserve later V26 East override and deliberate equipped meal aliases if staging an edge-only native material correction.',
    'Next stage source-preserving edge-only green spill correction;protect authored pose/alpha,clocks/master endpoints and opaque intentional equipment colors. Review representative corrected phases before expanding/adopting full cycles.',
    'Nine distributed phases do not prove continuous head motion,all-framegrade,toolgearcontinuity or full room acceptance. No existing James source or loader changed this turn.'])
save(out/'review.json',d)
rasters=[f.relative_to(r).as_posix() for f in out.glob('*.png')]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(a)==len(rasters)*3+1 and all(x==b'lfs' for x in a[2:-1:3])
section='''### James remaining diagnostics source comparisons — October 2, 2026

V28South/North/West bare+helmet9distributed inspect phases each against same-view
idle masters reviewed in12whole/enlarged boards,60prescribed slots. Fixed declared
pivot/H148translation only,no silhouette fitting. Hair/fabric generally track
these masters more closely than pre-V26East;do not apply East's violet correction
blindly. Green silhouette edging visible in several animated poses.
Read-only chroma/alpha-neighbour diagnostic covers864sources:most strongly green
pixels border alpha0 or have alpha<128. Source thresholds are diagnostic,not
semantic equipment masks;not every flagged pixel is proven unwanted. Next stage
an edge-only native spill correction preserving original poses/alpha/clocks/master
endpoints and opaque intentional equipment colors;review representative results
before expansion/adoption. Three directions share inspection continuity manifests;
keep later selectedV26East override and deliberate helmet meal inspection aliases.
No art/normal source/loader changes or new Godot run this turn. Nine distributed
samples cannot certify continuous helmet/head movement or complete color/tool/
room consistency. Full James goal and cargo stance/case joins remain open.
Evidence:character/james-full-set-review-2026-10-02/diagnostics-v28/review.json
and edge-diagnostic.json. All source hashes stable,LFS checked.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
 r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 for attempt in range(3):
  old=f.read_bytes();entry=section.encode()
  if entry.split(b'\n',1)[0] in old:break
  if f.name=='CURRENT_STATUS.md':at=old.index(b'### James East diagnostic hair/body correction selected');new=old[:at]+entry+b'\n'+old[at:]
  else:new=old+b'\n'+entry
  tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
  try:assert f.read_bytes()==old;os.replace(tmp,f);break
  except PermissionError:
   tmp.unlink()
   if attempt==2:raise
   time.sleep(2)
(out/'HANDOFF.md').write_text('''# Project handoff

## Objective and acceptance
Full James master-matched set and full cardinal/cross-family polish. Incomplete.

## Accepted decisions
Master scale/pivot/material/proportions;tablet faces James,wrench holstered,torch
repairs. Preserve authored poses/alpha,endpoints,and selected V26East correction.

## Current state
South/North/West12whole/enlarged bare+helmet boards reviewed,60source slots.
Colors generally track respective masters. Green edging visible in some moving
poses;864frame read-only diagnostic flags predominantly edge/lowalpha green.
No source correction or loader change this turn. Thresholds are not semantic masks.

## Verification
All sampled/dignostic hashes stable,all12rasters LFS checked,all five guides updated.
No new native run or full-cycle/continuous motion/room acceptance established.

## Next action
Stage edge-only native green spill correction on representative phases,retain
original alpha/motion/clocks/master endpoints and opaque legitimate equipment
colors. These3directions share continuity manifests;retain laterV26Eastoverride
and intentional helmet meal aliases. Then whole-cycle/loader review before adoption.
Cargo stance/case joins and full context/cardinal owner acceptance remain open.
''',encoding='utf-8')
for f in [p/'HANDOFF.md',out.parent/'HANDOFF.md']:
 old=f.read_text(encoding='utf-8');marker='## V28 remaining diagnostic comparisons\n'
 if marker not in old:
  at=old.index('## Next action\n');old=old[:at]+marker+'''South/North/West12bare+helmet whole/enlarged boards reviewed,60distributed source
slots. Respective master colors generally consistent;green silhouette edging
needs source-preserving edge-only study.864source read-only chroma/alpha diagnostic
mostly flags edge/lowalpha,butnotsemanticproof. No source/native/loader change.
See character/james-full-set-review-2026-10-02/diagnostics-v28/HANDOFF.md.

'''+old[at:];f.write_text(old,encoding='utf-8')
print(json.dumps(dict(reviewedBoards=12,reviewedSlots=60,diagnosticSourceFrames=864,guides=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
