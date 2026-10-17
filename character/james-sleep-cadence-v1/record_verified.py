from pathlib import Path
import json,os
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
n=json.loads((P/'validate-evidence.json').read_text());w=json.loads((P/'validate-validation.json').read_text());v=json.loads((P/'packaging-validation.json').read_text())
assert n['failures']==0 and len(n['journeys'])==2 and w['exitCode']==0 and not w['timedOut'] and not v['failures']
status='installed_native_verified_owner_review_pending'
for mode in ['bare','helmet']:
    file=P/(mode+'-manifest.json');m=json.loads(file.read_text());m['status']=status;file.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
(P/'selection.json').write_text(json.dumps({'status':status,'runtimeInstalled':True,'fullSetComplete':False,'statesPerMode':4,'sourceReferences':48,'pixelChanges':0,'cycleMs':3600,'packageChecks':v['checks'],'native':n,'profileGuard':{'realProfileUnchanged':w['realProfileUnchanged'],'profileDelta':w['profileDelta']},'visualReview':'All48 original sleeping poses inspected in paired four-direction source board; six actual retained q0 North berth captures reviewed. Source-clock previews prepared, no new artwork.','remaining':['Owner cadence/full-motion review','Other actual bunk layouts/rotations and actual gear changes','Full-frame and cross-family master/material/anatomy/motion/hand-off polish across James library']},indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(3*260,2*190),'#303b40');d=ImageDraw.Draw(board)
for row,j in enumerate(n['journeys']):
    for col,ref in enumerate(j['captures']):
        im=Image.open(R/ref.removeprefix('res://')).convert('RGB');crop=im.crop((345,270,585,425));x=col*260;y=row*190;board.paste(crop,(x,y+25));d.text((x+5,y+4),Path(ref).stem,fill='white')
board.save(P/'native-berth-review.png')
note='''

## James shared sleep breathing cadence — October 1, 2026

All four selected sleeping directions had a 960 ms loop. james-sleep-cadence-v1
now gives all eight bare/helmet sleep states a shared 3600 ms visual cycle using
the same six source slots, exact existing pixels, alpha, grade, proportions,
pivots, depth and pillow anchors. No lying/get-up or fatigue/service timer edits.
The normal 10.4 s sleep window ends in the final neutral slot at 10.2–10.8 s,
preserving the get-up join. All 48 source poses inspected in paired boards;
before/after source-clock GIFs retain genuine selected motion.

192 package checks pass. Native checks cover all eight normal loaded states and
three visual cycles each, plus actual retained q0 North berth navigation and
lie/sleep/get-up in both gear modes, two fresh-scene midpoint disk Continues with
exact actor/player/pause/clock/pose, fixed sleeping contact and normal completion.
The initial fixture incorrectly required fatigue below20 from100; controller
relief is45. Failed run retained; corrected assertions verify actual55 and the
completion serial/event. No gameplay change to satisfy the test. Final native
count and engine/profile guard are in validate-evidence.json/validate-validation.json.
Strict profile delta remains last_session.json only, cause unproven; scratch
APPDATA and no rollback. Six native berth views reviewed, not every bunk layout
or actual locker/gear-change proof. Full James goal remains active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James shared sleep breathing cadence' in data:continue
    enc=note.encode('utf-8');new=enc.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+enc;tmp=path.with_name(path.name+'.james-sleep-cadence.tmp');tmp.write_bytes(new);os.replace(tmp,path)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James sleeping cadence polish

## Objective and acceptance
Full James animation/master/style/perspective/size/proportion/material consistency,
then full cross-family polish. Goal active; this cadence selected/native verified,
owner/full-set acceptance remains separate.

## Accepted decisions and constraints
Use existing genuine sleep poses, no part painting/mirroring, per-pose fitting,
interpolated or duplicate authored frames. All four facings and both gear modes
share 3600 ms visual cycle (six600 ms slots). Source art and metadata exact;
fatigue/service stages remain0.8/10.4/0.8 s. Final neutral starts10.2 s, preserving
get-up. North corrected rest source retained, no source-density downgrade.

## Current state
New bare/helmet sleep-only manifests load after North rest polish in grid_canvas.
ACTIVE_ASSETS records paths. Original48 frame files referenced by whole res://
paths; source byte hashes retained. All-source boards and original/revised GIFs.
New validate.gd/.uid fixture retains real core/recovered/wreck registry and strict
save validator, uses scratch APPDATA, actual retained q0 berth approaches and
fresh-scene disk Continue. Failed fatigue assertion archived before repair.

## Verification
192 package checks pass. Native evidence verifies eight normal loaded states,
three visual cycles each, two actual North berth lie/sleep/get-up journeys and
mid-sleep fresh-scene Continues, exact pause/clock/player/actor/pixels, fixed
contact, terminal neutral and normal45-point fatigue relief100->55/completion.
Actual count/terminal guard live in final JSON files. All48 source poses reviewed;
six berth views reviewed. Other bunk layouts/rotations/locker gear changes not
exercised. Strict profile delta last_session.json only, cause unproven; no rollback.

## Next action
Refresh selected inventory/rest comparison after timing override. Continue full
source-pose and motion review across family joins, masters/material/anatomy,
actual furniture/gear/travel contexts. Historical North water boots and West
water-death limb TODOs have selected later polish/proof; verify current sources
before treating them as still open. No generation live; final native process must
be terminal before running this recorder. Full objective remains active.
''',encoding='utf-8')
(P/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James restful breathing cadence</h1><p>Installed shared3600ms visual cycle across four directions and both gear modes, exact original source art. Native loader/berth/Continue checks pass; full-set polish and owner review remain.</p><img src="north-revised.gif"><img src="native-berth-review.png"><img src="all-source-poses.png">',encoding='utf-8')
print(json.dumps({'status':status,'packageChecks':v['checks'],'nativeChecks':n['checks'],'journeys':len(n['journeys']),'nativeFailures':n['failures'],'profileDelta':w['profileDelta']}))
