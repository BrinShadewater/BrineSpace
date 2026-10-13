"""Normal q2 South drain04 study with original metadata and whole revision boards."""
from pathlib import Path
import json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1';read=lambda p:json.loads(p.read_text())
old=read(B/'cardinal02-cross-review/family-manifest.json');new=read(B/'drain-south-04-unselected/manifest.json')
for k in ['frameWidth','frameHeight','pivot','standingHeight','textureFilter']:assert old[k]==new[k]
family=old.copy();family['revision']='marsh-cardinal-water-transitions-03-staged'
family['sources']=['drain-south-04' if n=='drain-south-01' else n for n in old['sources']]
family['states']=[new['states'][0] if s['id']=='cargo-drain-south' else s for s in old['states']]
O=B/'cardinal03-cross-review';O.mkdir(exist_ok=True);(O/'family-manifest.json').write_text(json.dumps(family,indent=2)+'\n')
combined=read(B/'combined04-cross-review/manifest-list.json');combined['manifests']=[n.replace('cardinal02-cross-review','cardinal03-cross-review') for n in combined['manifests']]
O=B/'combined05-cross-review';O.mkdir(exist_ok=True);(O/'manifest-list.json').write_text(json.dumps(combined,indent=2)+'\n')
s=(ROOT/'tools/review_marsh_water_transition_world06.gd').read_text().replace('water-transition-world-06','water-transition-world-07').replace('WORLD06','WORLD07').replace('cardinal02-cross-review','cardinal03-cross-review')
for a,b in [('Vector2i(21,20);var target:=Vector2i(24,21)','Vector2i(20,21);var target:=Vector2i(19,24)'),('for y in range(20,22):','for y in range(21,25):'),('for x in range(21,25):','for x in [19,20]:'),('game.occupied[home].rotation=1','game.occupied[home].rotation=2'),('key=="swim-carry-north"','key=="swim-carry-east"'),('all six north timing slots','all six east timing slots'),('dispatched q1','dispatched q2 Southdrain04'),('return/north staged loop','return/east staged loop')]:s=s.replace(a,b)
p=ROOT/'tools/review_marsh_water_transition_world07.gd';p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://dm8p3nq6vh4k\n')
f=(ROOT/'tools/fingerprint_marsh_water_transition_world06.py').read_text().replace('water_transition_world06','water_transition_world07');(ROOT/'tools/fingerprint_marsh_water_transition_world07.py').write_text(f)
O=B/'drain-south04-cross-review';O.mkdir(exist_ok=True)
for page,revs in enumerate([['01','02'],['03','04']]):
    board=Image.new('RGB',(1792,476),'#293b40')
    for row,rev in enumerate(revs):board.paste(Image.open(B/f'drain-south-{rev}-unselected/whole-transition-comparison.png'),(0,row*238))
    board.save(O/f'revisions-{page:02}.png')
states={s['id']:s for n in combined['manifests'] for s in read(ROOT/n)['states']};assert len(states)==48 and sum(len(s['frameFiles']) for s in states.values())==272
print('q2 Southdrain04 private study prepared;48states/272slots, original metadata retained.')
