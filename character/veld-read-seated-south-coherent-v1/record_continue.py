from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-read-south-continue-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed'] and not v['realProfileChanges']
records=json.loads((O/'records.json').read_text())['records']
board=Image.new('RGB',(1024,6*280),'#202a30');draw=ImageDraw.Draw(board)
for row,record in enumerate(records):
 name=record['name']
 for column,suffix in enumerate(['before-source','after-source','before-room','after-room']):
  im=Image.open(O/f'{name}-{suffix}.png').convert('RGBA')
  if column>1:im=im.crop((490,286,660,391)).resize((256,158),Image.Resampling.NEAREST)
  board.paste(im,(column*256,row*280+24),im)
  draw.text((column*256+4,row*280+3),name+' / '+suffix,fill='#e1e7eb')
board.save(P/'continue-contact.png')
title='Veld South tablet fresh Continue - October 1, 2026'
note='## Veld South tablet fresh Continue - October 1, 2026\n\nActual twelve-second reading advances through normal observation service timer;\nstaged bare/helmet paired loader in prescribed real sofa contact. Actual disk\nwrite/read and fresh main-scene staged Continue at draw.2s/hold3s/stow11.8s:\n128checks0failures,6restores,219.49s engine0/no errors, scratch APPDATA,2931non-log\nowner files unchanged. Exact whole displayed source, gear/action clock, physical\nfoot/contact and paused pose retained. No reading-clock patch needed: existing\nplayer checkpoint preserves the finite clip. Continue source/native paired board\nreview required independently of checks. Not natural chooser or early service exit\nproof. Full goal active/incomplete, sources remain unselected.\n'
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 data=path.read_bytes()
 if title.encode() not in data:path.write_bytes((note.encode()+b'\n'+data) if path.name=='CURRENT_STATUS.md' else data+b'\n\n'+note.encode())
h=P/'HANDOFF.md';data=h.read_bytes()
if title.encode() not in data:h.write_bytes(data+b'\n\n'+note.encode())
e=P/'evidence.json';data=json.loads(e.read_text());files=[f for f in O.iterdir() if f.is_file()]+[P/'continue-contact.png',P/'HANDOFF.md',P/'record_continue.py',R/'tests/test_veld_read_south_continue.gd',R/'tests/test_veld_read_south_continue.gd.uid',R/'tools/run_veld_read_south_continue.py']
for f in files:data['bindings'][f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
data['freshContinue']={'checks':128,'restores':6,'seconds':219.49,'scope':'actual disk/fresh-scene draw/hold/stow both gears, prescribed contact and staged sources'}
e.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'boardSamples':len(records)*4,'boundFiles':len(data['bindings'])}))
