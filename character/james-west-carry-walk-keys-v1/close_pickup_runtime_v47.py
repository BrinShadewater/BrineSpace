from pathlib import Path
import hashlib,json,subprocess,os,uuid,time,difflib
from PIL import Image,ImageDraw

p=Path(__file__).resolve().parent
r=p.parents[1]
out=p/'pickup-runtime-v47'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((out/'inputs.json').read_bytes())
assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
visual=json.loads((out/'visual-inputs.json').read_bytes())
assert all(sha(r/x['file'])==x['sha256'] for x in visual['sourceRecords'])
native=json.loads((out/'native-evidence.json').read_bytes())
validation=json.loads((out/'native_probe-validation.json').read_bytes())
assert native['checks']==320 and native['failures']==0
assert len(native['results'])==8 and sum(x['diskResume'] for x in native['results'])==2
assert sum(x['normalPickupSlots'] for x in native['results'])==48
assert sum(len(x['captures']) for x in native['results'])==24
assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
changes={}
for name in ['james_cargo_actor.gd','bill_npc.gd']:
    old=(out/(name+'.before')).read_text().splitlines(True)
    new=(r/'scripts'/name).read_text().splitlines(True)
    diff=''.join(difflib.unified_diff(old,new,fromfile=name+'.before',tofile=name))
    changes[name]=diff
(out/'scoped-runtime-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
evidence=dict(runtimeInstalled=True,normalArtworkChanged=False,nativeChecks=320,nativeFailures=0,cases=8,sourceSlots=48,diskResumes=2,roomCaptures=24,reviewedSourceBoards=4,reviewedRoomBoards=4,sourceAcceptance=False,fullGoalComplete=False,realProfileUnchanged=True,scope='Normal James dry workshop pickup, prescribed clear floor, actual work completion and carry handoff. Not autonomous scheduler or full uninterrupted cargo lifecycle.',remaining=['Full cargo lifecycle and interruption review','Pickup terminal to staged preparation endpoint comparison','North/South terminal narrow walking stance review','Master/cross-family consistency polish'])
(out/'review-acceptance.json').write_text(json.dumps(evidence,indent=2)+'\n')
section='''### James normal dry workshop pickup installed — October 2, 2026

James now selects the existing six-source pickup clip from the inherited520ms
workshop_pickup simulation timer, instead of displaying idle during that phase.
Shared checkpoint validation now admits the actual stationary dry pickup stage,
with finite0..520ms timer, idle state, no route and live actor. No art selection,
navigation, work durations or scheduler changes. Scoped before-file diff retained.

Native320checks/0failures, four directions/both gears,48exact source slots,
24room captures; two West midpoint disk restores use the normal bank without
candidate reinstallation. Owner profile unchanged under scratch APPDATA. All four
source boards and four room boards visually reviewed. Selected idle is a same-view
reference, not newly certified original-master acceptance. Open-floor fixture
does not establish every workstation placement or uninterrupted lifecycle motion.
North/South terminal pickup source has a narrow first-step stance: review it through
movement handoff. West fresh-scene source pixels match; room lighting need not.

Lesson: authored state coverage can remain unreachable from a controller. Bind
finite actions to their simulation clock and admit their real checkpoint stage.
PhysicalH148 ruler does not require crouches to retain standing bounding-box height.
Existing V44 preparation and V16 West walk remain staged, with case/body projection
join unresolved. Compare normal pickup terminal to preparation before integration;
then check arrival turns, interruptions, furniture contact and full-set polish.
Evidence:character/james-west-carry-walk-keys-v1/pickup-runtime-v47/review-acceptance.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James staged West cargo room and disk-resume review'.encode());new=old[:at]+entry+b'\n'+old[at:]
    else:new=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    try:
        for attempt in range(5):
            assert f.read_bytes()==old
            try:os.replace(tmp,f);break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()
(out/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full master-matched James library and consistency polish; incomplete.\n\n'+section+'\nChanged: scripts/james_cargo_actor.gd pickup presentation/clock; scripts/bill_npc.gd pickup snapshot admission; fixture, review evidence and five maintained guides. No commit/PR/export.\n',encoding='utf-8')
parent=p/'HANDOFF.md'
if section.encode().split(b'\n',1)[0] not in parent.read_bytes():
    with parent.open('ab') as f:f.write(b'\n'+section.encode())

# Fixed-pivot source comparison: no source rescaling, repainting or pose repair.
comp=p/'pickup-carry-contact-v48';comp.mkdir(exist_ok=True)
inventory=json.loads((r/'character/james-full-set-review-2026-10-02/current-selection-v31/source-inventory.json').read_bytes())
board=Image.new('RGBA',(256*7,280*2),(47,58,63,255));draw=ImageDraw.Draw(board)
records=[]
for row,mode in enumerate(['bare','helmet']):
    pickup=inventory['states'][mode]['pickup-west']
    prep=json.loads((p/'finite-handoff-v44'/(mode+'-manifest.json')).read_bytes())['states'][0]
    paths0=[pickup['frameFiles'][4],pickup['frameFiles'][5],*prep['frameFiles']]
    walk=json.loads((p/'master-head-review-v16'/(mode+'-manifest.json')).read_bytes())
    walkstate=next(x for x in walk['states'] if x['id']=='carry-west')
    paths0.append(walkstate['frameFiles'][0])
    normalwalk=inventory['states'][mode]['carry-west']
    paths0.append(normalwalk['frameFiles'][0])
    for col,(label,f) in enumerate(zip(['pickup4','pickup5','prep0','prep1','prep2','candidate-walk0','normal-walk0'],paths0)):
        rel=f.removeprefix('res://')
        # Pickup manifest paths can be relative to its own package.
        source=r/rel
        if not source.exists():
            manifest=pickup['manifest'] if col<2 else normalwalk['manifest'] if col==6 else str((p/'master-head-review-v16'/(mode+'-manifest.json')).relative_to(r))
            source=r/Path(manifest.removeprefix('res://')).parent/rel
        assert source.exists(),source
        im=Image.open(source).convert('RGBA');assert im.size==(256,256)
        board.alpha_composite(im,(col*256,row*280+24))
        draw.text((col*256+8,row*280+5),mode+' '+label,fill='white')
        records.append(dict(mode=mode,label=label,file=source.relative_to(r).as_posix(),sha256=sha(source)))
board.save(comp/'source-contact-review.png')
(comp/'inputs.json').write_text(json.dumps(dict(sourceRecords=records,scope='Seven fixed-pivot West sources per gear including normal walk entry. Native256 canvas, no rescaling. Comparison only; no admission.'),indent=2)+'\n')
rasters=[f.relative_to(r).as_posix() for folder in [out,comp] for f in folder.rglob('*.png')]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(checks=320,failures=0,guides=5,lfsRasters=len(rasters),runtimeInstalled=True,comparison=str(comp/'source-contact-review.png'))))
