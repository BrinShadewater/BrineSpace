from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-read-south-interrupt-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed'] and not v['realProfileChanges']
records=json.loads((O/'records.json').read_text())['records'];assert len(records)==16 and all(r['exact'] for r in records)
board=Image.new('RGB',(2048,4*280),'#202a30');draw=ImageDraw.Draw(board)
for index,record in enumerate(records):
 x=(index%4)*512;y=(index//4)*280
 for column,suffix in enumerate(['before','after']):
  im=Image.open(O/f"{record['name']}-{suffix}.png").convert('RGBA');board.paste(im,(x+column*256,y+24),im)
  draw.text((x+column*256+4,y+3),record['name']+' / '+suffix,fill='#e1e7eb')
board.save(P/'interrupt-contact.png')
board=Image.new('RGB',(1024,560),'#202a30');draw=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
 for column,suffix in enumerate(['save-source','restore-source','save-room','restore-room']):
  im=Image.open(O/f'{gear}-power-3.0-{suffix}.png').convert('RGBA')
  if column>1:im=im.crop((490,286,660,391)).resize((256,158),Image.Resampling.NEAREST)
  board.paste(im,(column*256,row*280+24),im);draw.text((column*256+4,row*280+3),gear+' / '+suffix,fill='#e1e7eb')
board.save(P/'interrupt-continue-contact.png')
title='Veld South interrupted tablet stow - October 1, 2026'
note='## Veld South interrupted tablet stow - October 1, 2026\n\nActual power/suspend guard previously changed the staged reader directly to rise:\n134checks/16failures,40.02sec, owner files unchanged. Source switch confirmed in\nall16draw/hold/tap/stow cases across both gears/triggers. Superseded, retained.\nAdded Veld-only finite-reader capability detection, exact current unique pose\nindex in existing tablet_exit_pose, corresponding partial reverse stow clock;\nheld variants retain current whole pose for first60ms before authored stow. Shared\nNPC guard invokes opt-in hook; legacy Veld loops and Bill controller unchanged.\nRenderer resolves saved unique pose from selected finite12s/6pose South reader.\nExisting snapshot field/range and timer schema retained; no new save schema.\n\nFinal183checks0failures,16actual power/suspend exits,16exact stow-to-rise joins,\n2actual disk/fresh-scene interrupted exits,97.42sec, engine0/no errors, scratch\nAPPDATA,2931non-log owner files unchanged. Actual current hand/face/body source,\nphysical sofa contact and paused interrupted Continue remain exact. Source and\nnative save/restore boards require separate visual review. Earlier134pass/39.17s\nverified exit dispatch only, before expanded joins/fresh Continue coverage.\nOrdinary finite reader Continue earlier128checks/6restores/219.49s remains its\noriginal pre-hook interval. No normal artwork selection, natural chooser,\nall-stage hazards, owner acceptance or full-set completion claim. Next adopt\ncoherent South family with real selected-loader contact/service proof, then\nNorth reading and remaining seated/rest/death/water cross-family polish.\n'
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md'),P/'HANDOFF.md']
for path in paths:
 raw=path.read_bytes()
 if title.encode() not in raw:path.write_bytes(note.encode()+b'\n'+raw if path.name=='CURRENT_STATUS.md' else raw+b'\n\n'+note.encode())
e=P/'evidence.json';data=json.loads(e.read_text())
files=[f for f in O.iterdir() if f.is_file()]+[P/'HANDOFF.md',P/'interrupt-contact.png',P/'interrupt-continue-contact.png',P/'record_interrupt.py',R/'scripts/bill_npc.gd',R/'scripts/veld_npc.gd',R/'scripts/grid_canvas.gd',R/'tests/test_veld_read_south_interrupt.gd',R/'tests/test_veld_read_south_interrupt.gd.uid',R/'tools/run_veld_read_south_interrupt.py']
for folder in O.glob('interval-before-*'):
 files += [f for f in folder.iterdir() if f.is_file() and f.name in ['native.log','validation.json','records.json','profile-before.json','profile-after.json']]
for f in files:data['bindings'][f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
data['interruptions']={'checks':183,'count':16,'diskRestores':2,'seconds':97.42,'scope':'actual power/suspend guards, exact first source and stow/rise joins, fresh-scene interrupted exits both gears; staged sources, prescribed sofa entry'}
data['scope']='staged same-body South reading, actual prescribed sofa route/service/render, ordinary and interrupted disk Continue; no normal selection/natural chooser/all hazards/owner acceptance'
e.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'interruptions':16,'nativeRestorePairs':2,'boundFiles':len(data['bindings'])}))
