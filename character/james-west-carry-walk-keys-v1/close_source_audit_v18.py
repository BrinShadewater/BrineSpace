from pathlib import Path
from PIL import Image
import hashlib,json,os,uuid,time,subprocess,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];bridge=p/'start-bridge-v17';out=r/'character/james-full-set-review-2026-10-02'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
def stable(d,k):assert all(sha(r/f)==v for f,v in d[k].items())
generations=[]
for i in (1,2):
 name=f'start-{i:03}';inputs=json.loads((bridge/f'{name}-inputs.json').read_bytes());stable(inputs,'preCallSha256')
 a=np.array(Image.open(r/inputs['baseFile']).convert('RGBA'));b=np.array(Image.open(bridge/f'{name}.png').convert('RGBA'));mask=np.ones((256,256),bool);mask[104:228,88:166]=False
 assert mask.sum()==55864 and np.array_equal(a[mask],b[mask])
 f=bridge/f'{name}-review.json';d=json.loads(f.read_bytes());assert d['rawSha256']==sha(bridge/f'{name}-raw.png')
 d.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='rejected_endpoint_like_stance',findings=['Both raw and native comparisons reviewed. Changed donor endpoint makes both interiors close to walking; neither establishes deliberate chronological stance progression from standing.',
 'Inherited comparison left-caption says standing endpoint but base is the actual walking endpoint; inputs.baseFile governs. No finite bridge/native adoption inferred. Use actual authored pose donors for next attempt instead of fractional yaw prompts.'])
 save(f,d);g=json.loads((bridge/f'{name}-generation.json').read_bytes());assert g['terminal']
 generations.append({'slot':i,'tool':'builtin_image_gen','prompt':f'{name}-prompt.txt','raw':f'{name}-raw.png','rawSha256':d['rawSha256'],'terminal':True,'used':False,'disposition':d['disposition']})
save(bridge/'generation-index.json',{'generations':generations,'allTerminalAndCopied':True})
inventory=json.loads((out/'source-inventory.json').read_bytes());stable(inventory,'sourceSha256');s=inventory['summary']
assert s['bareStates']==338 and s['helmetStates']==248 and s['pairedStateIds']==248
assert s['missingFrameSources']==s['invalidDeclaredCounts']==s['invalidClockLengths']==0
assert all(x['sameFrameCount'] and x['sameClock'] for x in inventory['pairedContracts'])
assert all(not any('mirror' in k.lower() for k in json.loads((r/x['manifest']).read_bytes())) for x in inventory['orderedManifestLoads'])
profile=json.loads((out/'profile-pair-review.json').read_bytes());stable(profile,'inputSha256');assert len(profile['records'])==48
consumers=[r/'scripts/crew_life.gd',r/'scripts/bill_npc.gd',r/'scripts/branforth_npc.gd',r/'scripts/bill_meal.gd',r/'scripts/bill_inspection.gd']
life=consumers[0].read_text();assert 'if actor.helmet_equipped and value in ["eat","drink"]: return "inspect"' in life
assert consumers[2].read_text().startswith('extends "res://scripts/bill_npc.gd"')
profile.update(visualReviewPending=False,reviewedBoards=8,reviewedSourceSlots=48,visualAcceptance=False,
 postReviewConsumerSha256={f.relative_to(r).as_posix():sha(f) for f in consumers},
 findings=['Eight bare/helmet eating/drinking profile boards at identical148 world ruler and fixed pivot translation reviewed. Equipped rows depict inspection rather than meals.',
 'CrewLife remaps equipped eat/drink to inspect. Inherited Bill special meal/inspection clocks reject James script type, preserving this generic route. Source aliases are deliberate; do not regenerate meals through sealed helmets.',
 'Different canvases alone do not prove height/pivot defects. Actual room/equipment scheduler and furniture still require runtime verification; no source or profile fix made.'])
save(out/'profile-pair-review.json',profile)
assessment={'primarySourceSummary':s,'inventorySha256':sha(out/'source-inventory.json'),'allPairedFrameCountsAndClocksMatch':True,'mirrorDeclarations':0,
 'profileDifferenceStates':[x['state'] for x in inventory['pairedContracts'] if not x['sameCanvasPivotRuler']],
 'sourceVisualReview':{'mealProfileBoards':8,'prescribedSourceSlots':48,'existingWestSettleBoards':2},
 'nextMotionReference':{'state':'carry-settle-west','sourceManifest':inventory['states']['bare']['carry-settle-west']['manifest'],'poses':6,'status':'pose_reference_only_not_new_master_matched_bridge'},
 'rejectedStanceAttempts':[str((bridge/'generation-index.json').relative_to(r))],'nativeRunThisTurn':False,'realProfileTouched':False,'normalChanged':False,'fullGoalComplete':False,
 'scope':'Primary literal manifest source inventory and static semantic/profile review. Not full runtime cue coverage, actual room acceptance, continuous motion or full goal completion.'}
save(out/'audit-assessment.json',assessment)
rasters=[f.relative_to(r).as_posix() for root in (bridge,out) for f in root.rglob('*') if f.suffix.lower() in ('.png','.apng')]
a=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(a)==len(rasters)*3+1 and all(x==b'lfs' for x in a[2:-1:3])
section='''### James full primary-source inventory and stance reference audit — October 2, 2026

V17 two walking-endpoint-authored start interiors terminal/copied/raw/native-detail
reviewed, rejected: still endpoint-like, no convincing stance progression. Both
55864 outside pixels/frozen inputs exact. No failed bridge manifest/adoption made.
Stop repeating fractional yaw prompts; compare actual six-pose normal West settle
motion donors instead. Whole/leg source boards reviewed against current endpoints;
these old donors are pose references, not master-matched replacement artwork.
Fresh literal catalog/grid inventory:143 manifest loads,338 bare/248 helmet state
IDs,4287/3771 frame references,248 paired IDs. Zero missing frame sources, invalid
declared counts or clock lengths; all paired counts/clocks match,no mirror metadata.
Counts exclude cargo-player/controller special cues and do not prove unique poses
or visual acceptance. Eight meal/drink canvas/profile differences reviewed in eight
fixed-pivot/148-ruler boards,48 source slots. Equipped rows intentionally inspect:
CrewLife remaps eat/drink while helmet-equipped to inspect; inherited Bill special
clocks reject James type. Do not mislabel these aliases or90 bare-only meal/cup/
equipment source IDs as automatically missing required helmet actions.
Lesson: matching source counts/clocks can conceal different action meanings; inspect
consumer semantics and normalize only through declared pivot/ruler before changing
art. Record failed endpoint-biased prompts and move to actual authored pose guides.
V16 standing-head carrying candidate preserved; no normal bank/controller/profile
changes or Godot run this turn. Native room/cue/equipment dispatch,stance/unload
bridges,continuous case/material review,interruptions/Continue/versioned adoption
and full James cardinal/cross-family polish remain open. Full goal incomplete.
Handoffs:character/james-west-carry-walk-keys-v1/HANDOFF.md;
character/james-full-set-review-2026-10-02/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 for attempt in range(3):
  old=path.read_bytes();entry=section.encode()
  if entry.split(b'\n',1)[0] in old:break
  if path.name=='CURRENT_STATUS.md':
   at=old.index(b'### James West carrying standing-head consistency candidate');new=old[:at]+entry+b'\n'+old[at:]
  else:new=old+b'\n'+entry
  temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
  try:
   assert path.read_bytes()==old;os.replace(temp,path);break
  except PermissionError:
   temp.unlink()
   if attempt==2:raise
   time.sleep(5)
(out/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · James full-set primary source review

## Objective and acceptance
Full master-matched James animation set and full cardinal/cross-family polish.
Incomplete. Source coverage is not actual runtime/art/owner acceptance.

## Accepted decisions and constraints
All comparisons use declared148 ruler and pivot translation; no bounding-box fit.
Helmet eat/drink routes to inspect deliberately. Bare-only meal/cup source IDs
and differing canvas extents are not automatically missing/defective gear coverage.

## Current state
Read-only inventory143 literal manifest loads:338 bare/248 helmet source state IDs,
4287/3771 references,248 paired IDs. No missing sources/count/clock-length defects.
All paired clocks/counts match,no mirror metadata. Eight paired-profile boards and
two existing West settle donor whole/leg boards reviewed. V17 stance trials rejected.
V16 carrying master-head candidate remains current, no normal source/code changes.

## Verification
Source/manifest hashes stable;48 prescribed meal/drink slots reviewed. Consumer
remap and inherited Bill-clock James exclusion inspected. No native runtime test
or owner profile write this turn. New raster LFS verified. All five guides updated.

## Next action
Use actual six-pose West settle chronology as pose guide for master-matched stance
source repair, not more fractional endpoint prompts. Stance/unload/case/material
polish; actual room/equipment/cargo special cues and interruption/Continue checks;
versioned adoption,remaining cardinal/full-family consistency. Inventory does not
include controller special source dispatch, so verify it separately before closeout.
''',encoding='utf-8')
f=p/'HANDOFF.md';old=f.read_text();anchor='## Next action\n';at=old.index(anchor)
old=old[:at]+'''## Latest motion attempt and full-set evidence
V17 two walking-endpoint stance interiors rejected after raw/native-detail review:
both remain endpoint-like. Frozen inputs/55864 outside guards exact, all jobs
terminal/copied. No finite bridge or native promotion. Stop repeating fractional
yaw prompts; next actual six-pose West settle source donor study.
Full primary-source inventory and eight meal/profile+two settle source boards in
character/james-full-set-review-2026-10-02/HANDOFF.md. No normal changes/native test
this turn. V16 master-head candidate and earlier native922/0 scope remain intact.

## Next action
Actual authored stance pose guides for master-matched start/unload bridge repair;
rigid-case/latch/grip/material continuity; actual room/distance/equipment/cargo cue
dispatch,interruptions/Continue/versioned adoption,full cardinal/cross-family polish.
'''
f.write_text(old,encoding='utf-8')
print(json.dumps({'rejectedTrials':2,'primaryBareStates':338,'primaryHelmetStates':248,'missingSources':0,'profileBoardsReviewed':8,'settleBoardsReviewed':2,'guides':5,'nativeRun':False,'normalChanged':False,'lfsRasters':len(rasters)}))
