from pathlib import Path
import hashlib,json,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
inputs=json.loads((p/'selected-inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
for stem in ['material-bake','validate','validate-selected','native-arrival-continue']:
 d=json.loads((p/(stem+'-validation.json')).read_bytes());assert d['exitCode']==0 and d['realProfileUnchanged'] and not d['profileDelta']
route=json.loads((p/'native-arrival-continue-evidence.json').read_bytes());assert route['failures']==route['mismatches']==0 and len(route['results'])==8
normal=json.loads((p/'validate-selected-evidence.json').read_bytes());assert normal['failures']==0
package=json.loads((p/'package-review.json').read_bytes());assert package['sourceAcceptance'] and not package['visualReviewPending']
invpath=r/'character/james-full-set-review-2026-10-02/current-selection-v27/source-inventory.json';inv=json.loads(invpath.read_bytes());assert all(sha(r/f)==v for f,v in inv['sourceSha256'].items())
prior=json.loads((invpath.parent.parent/'source-inventory.json').read_bytes());changed=[]
for mode in ['bare','helmet']:
 for key,state in inv['states'][mode].items():
  old=prior['states'][mode][key]
  if state['manifest']!=old['manifest']:
   changed.append(dict(mode=mode,state=key,old=old['manifest'],new=state['manifest']))
assert {(x['mode'],x['state']) for x in changed}==({(m,k) for m in ['bare','helmet'] for k in ['inspect-east','interact-east']}|{('helmet','eat-east'),('helmet','drink-east')})
assert inv['summary']['missingFrameSources']==inv['summary']['invalidDeclaredCounts']==inv['summary']['invalidClockLengths']==0
selection=json.loads((p/'selection-evidence.json').read_bytes())
selection.update(normalChecks=normal['checks'],routeChecks=route['checks'],routeFreshSceneRestores=8,allRouteDirectionsAndGearsPassed=True,
    normalNativeCapturesReviewed=4,routeCaptureReviewPending=False,routeBoardsReviewed=2,routeCapturesReviewed=24,wholeRealProfileUnchanged=True,currentSourceInventory=str(invpath.relative_to(r)),changedPrimaryStateSelections=changed,
    continuousVisualMotionReviewed=False,fullGoalComplete=False,
    scope='Selected East paired hair/body native material correction. All282 source frames reviewed; normal loader and eight explicit generic dry room arrivals/fresh-scene disk restores verified. Two24-capture room boards reviewed, actor visible with appropriate facing/active/stowed tablet; north partly overlaps workshop backdrop. Autonomous schedules/locker changes/rotation/full James acceptance unproven.')
save(p/'selection-final-evidence.json',selection)
rasters=[f.relative_to(r).as_posix() for folder in [p,r/'character/james-east-inspect-body-grade-v25'] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==len(rasters)*3+1 and all(x==b'lfs' for x in attrs[2:-1:3])
section='''### James East diagnostic hair/body correction selected — October 2, 2026

V26 native bounded smooth violet-chroma correction selected through both whole
grid-loader and ACTIVE_ASSETS paths. Original282 source alpha/geometry and RGB
outside selector exact, endpoints exact, source clocks/counts/pivot/H148 unchanged,
shared helmet differences exact and paired body below60 exact. Selected matte-v3
tablet repair retained;V24 generated image remains color reference,not a pose.
V25 failed outside-mask protection at byte mean16 due float epsilon; archived.
V26 authoring selection rounds source bytes and uses integer sum>48; smooth shader
weights retained. Lesson: a zero correction weight does not guarantee untouched
pixels after native render roundtrip; copy original RGB outside a byte-defined
admission selector and independently verify it. Selector is bounded chroma,not
semantic hair/fabric segmentation;do not claim every warm skin/amber pixel was
semantically classified. No warping/fitting/new artwork or revised motion.
All282 candidate source frames in10boards and two master/current/candidate boards
reviewed;four staged and four selected native paired148/82/54/27 captures reviewed.
Staged loader2357/0,selected loader2356/0. Eight explicit dry maintenance-room
direction/gear arrival and fresh-scene midpoint disk restores pass; exact resumed
actor/playback/clock/pause/pixels and6s completion. Owner whole profile unchanged
under scratch APPDATA. Two24-capture room boards reviewed;not autonomous
scheduler,locker/equipment changes,workstation rotations,title fresh-process or
continuous native motion acceptance.141-frame paired APNG decoded RGBA/clock exact.
FreshV27 primary inventory keeps338bare/248helmet states;East inspect/interact
pergear plus deliberate helmet eat/drink inspection aliases select new manifests,
zero source/count/clock defects. V18 is historical
before-selection evidence,not current source authority. Full goal incomplete;
cargo joins,other cardinal action colors and room/context consistency remain open.
Evidence:character/james-east-inspect-body-grade-v26/selection-final-evidence.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
 r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
 for attempt in range(3):
  old=path.read_bytes();entry=section.encode()
  if entry.split(b'\n',1)[0] in old:break
  if path.name=='CURRENT_STATUS.md':at=old.index(b'### James East diagnostic body color diagnosis');new=old[:at]+entry+b'\n'+old[at:]
  else:new=old+b'\n'+entry
  temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
  try:assert path.read_bytes()==old;os.replace(temp,path);break
  except PermissionError:
   temp.unlink()
   if attempt==2:raise
   time.sleep(2)
handoff='''# Project handoff

## Objective and acceptance
Full James master-matched set then cardinal/cross-family polish. Incomplete.

## Accepted decisions
Tablet faces James,wrench holstered,torch repairs. Original authored motion/alpha,
matte tablet and shared helmet retained. No silhouette fit or mirrored motion.

## Current state
V26 paired hair/body neutral matte material bank selected in normal grid and
ACTIVE_ASSETS. V25 outside-mask boundary failure archived;V24color guide only.
V27 current primary-source inventory supersedes V18 as current selection authority.
Original282alpha/outside selector/endpoints,clocks/pivot/ruler exact. All282 source
frames and two comparison boards/four staged/four normal native captures reviewed.

## Verification
Staged2357/0,normal2356/0;eight explicit dry room approaches and fresh-scene disk
restores pass with exact pose/clock/contact/gear and6scompletion. Whole real owner
profile unchanged,scratch APPDATA. APNG141pairedframes decoded exact sourceclock.
All five guides/LFS updated. See selection-final-evidence.json for exact scope.

## Next action
Two24-capture room boards reviewed;then other cardinal action color/
master checks and cargo stance/case joins. Autonomous scheduler,actual locker/gear
changes,rotation/title fresh-process/continuous native motion and full James owner
acceptance remain unproven. Manifest pending-validation status is historical
selection metadata;final evidence records passing checks without mutating inputs.
'''
(p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
for f in [r/'character/james-west-carry-walk-keys-v1/HANDOFF.md',r/'character/james-full-set-review-2026-10-02/HANDOFF.md']:
 old=f.read_text(encoding='utf-8');marker='## V26 selected East body material\n'
 if marker not in old:
  at=old.index('## Next action\n');old=old[:at]+marker+'''Paired East hair/body correction selected,original282alpha/outside selector and
motion/clock/pivot exact;source10boards/two comparison/four staged/four selected
native captures reviewed.2357staged/2356normal checks pass;eight explicit dry
direction/gear arrivals and fresh-scene disk restores pass. Owner profile unchanged.
V27current-selection inventory supersedes V18currentness. Two24-capture room
boards reviewed;see character/james-east-inspect-body-grade-v26/HANDOFF.md.
Cargo joins and full cardinal/context/cross-family acceptance remain open.

'''+old[at:];f.write_text(old,encoding='utf-8')
print(json.dumps(dict(normalChecks=normal['checks'],routeChecks=route['checks'],routeRestores=8,guides=5,lfsRasters=len(rasters),fullGoalComplete=False)))
