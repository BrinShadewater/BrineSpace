"""Private South pickup02 substitution; compare complete same-direction families."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=read(B/'cardinal01-cross-review/family-manifest.json');new=read(B/'pickup-south-02-unselected/manifest.json')
for k in ['frameWidth','frameHeight','pivot','standingHeight','textureFilter']:assert old[k]==new[k]
family=old.copy();family['revision']='marsh-eight-direction-water-transitions-02-staged'
family['sources']=['pickup-south-02' if n=='pickup-south-01' else n for n in old['sources']]
family['states']=[new['states'][0] if s['id']=='swim-pickup-south' else s for s in old['states']]
O=B/'cardinal02-cross-review';O.mkdir(exist_ok=True);(O/'family-manifest.json').write_text(json.dumps(family,indent=2)+'\n')
combined=read(B/'combined03-cross-review/manifest-list.json')
combined['manifests']=[n.replace('cardinal01-cross-review','cardinal02-cross-review') for n in combined['manifests']]
O=B/'combined04-cross-review';O.mkdir(exist_ok=True);(O/'manifest-list.json').write_text(json.dumps(combined,indent=2)+'\n')
s=(ROOT/'tools/review_marsh_water_transition_world03.gd').read_text().replace('water-transition-world-03','water-transition-world-06').replace('WORLD03','WORLD06').replace('cardinal01-cross-review','cardinal02-cross-review')
p=ROOT/'tools/review_marsh_water_transition_world06.gd';p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://ck9v2pm7nh4q\n')
f=(ROOT/'tools/fingerprint_marsh_water_transition_world03.py').read_text().replace('water_transition_world03','water_transition_world06')
(ROOT/'tools/fingerprint_marsh_water_transition_world06.py').write_text(f)
O=B/'south02-cross-review';O.mkdir(exist_ok=True)
board=Image.new('RGB',(1792,476),'#293b40')
for row,rev in enumerate(['01','02']):board.paste(Image.open(B/f'pickup-south-{rev}-unselected/whole-transition-comparison.png'),(0,row*238))
board.save(O/'pickup-revisions.png')
states={s['id']:s for n in combined['manifests'] for s in read(ROOT/n)['states']}
resolve=lambda n:ROOT/n.removeprefix('res://')
master=ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png'
rows=[[(master,'OWN MASTER'),(resolve(states['swim-pickup-south']['frameFiles'][3]),'PICKUP launch'),(resolve(states['swim-pickup-south']['frameFiles'][4]),'PICKUP late')]+[(resolve(states['swim-carry-south']['frameFiles'][i]),f'SWIM {i}') for i in range(4)]+[(resolve(states['cargo-drain-south']['frameFiles'][1]),'DRAIN first')],[(resolve(n),f'DRAIN {i}') for i,n in enumerate(states['cargo-drain-south']['frameFiles'])]+[(resolve(states['unload-south']['frameFiles'][3]),'UNLOAD final'),(master,'OWN MASTER')]]
records=[]
for row,items in enumerate(rows):
    board=Image.new('RGB',(1792,238),'#293b40');d=ImageDraw.Draw(board)
    for col,(p,label) in enumerate(items):
        im=Image.open(p).convert('RGBA');assert im.size in [(184,184),(224,208)];offset=20 if im.width==184 else 0
        board.paste(im,(224*col+offset,25),im);d.text((224*col+4,5),label,fill='white')
        records.append({'row':row,'column':col,'source':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'wholeTranslation':[offset,0],'operations':'Exact whole source pixels;dry184p92 padded20x to224p112,noresize'})
    board.save(O/f'south-family-{row:02}.png')
(O/'sources.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'records':records},indent=2)+'\n')
assert len(states)==48 and sum(len(s['frameFiles']) for s in states.values())==272
print('South02 private family/list/q1fixture and exact whole cross-family boards prepared;48states/272slots.')
