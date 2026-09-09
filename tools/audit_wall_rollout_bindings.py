"""Read-only provenance and live-consumer audit for the original wall rollout."""
import hashlib,json,re
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def path(s):return ROOT/s.removeprefix('res://')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ledger=json.loads(path('assets/wall-room-rollout-v1/rollout.json').read_text())
 manifest=json.loads(path('rooms/full-wall-v1/manifest.json').read_text())
 floors=json.loads(path('rooms/floor-profiles-v1/rooms.json').read_text())
 grid=path('scripts/grid_canvas.gd').read_text();cards=path('scripts/room_card_art.gd').read_text()
 assert len(ledger['rooms'])==14
 records=[];versions=0;registrations=0
 for room in ledger['rooms']:
  rid=room['id'];entry=next(x for x in manifest if x['room']==rid)
  assert entry['view'] in grid,(rid,'grid binding')
  assert next(x for x in floors if x['id']==rid)['view']==entry['view']
  assert path(entry['view']).with_suffix('.gd.uid').exists()
  sources={}
  for src in room['sources']:
   p=path(src['source']);assert sha(p)==src['sha256'],p
   assert path(src['prompt']).read_text(encoding='utf-8').strip()
   with Image.open(p) as im:assert list(im.size)==src['dimensions'];im.verify()
   sources['res://'+src['source']]=src
   versions+=1
  folder=path('rooms/full-wall-v1/registrations');asset=entry['asset']
  regs=[folder/(asset+'.json')]
  if entry.get('split'):
   spec=json.loads(path('rooms/full-wall-v1/split-'+asset+'.json').read_text())
   assert len(spec['sections'])==2
   regs += [folder/(asset+'-'+direction+'-'+section+'.json') for direction in ['north','east','south','west'] for section in spec['sections']]
  else:regs += sorted(folder.glob('side-'+asset+'-*.json'))
  for p in regs:
   reg=json.loads(p.read_text());assert reg['source'] in sources,(rid,p,'unrecorded source')
   assert sources[reg['source']]['selected'],(rid,p,'unselected source')
   assert sha(path(reg['source']))==reg['sha256'],p
   assert reg['pieces'] and min(reg['region'][2:])>0
   registrations+=1
  card='res://assets/wall-room-rollout-v1/cards/'+rid+'.png'
  assert re.search(r'"'+rid+r'"\s*:\s*"'+re.escape(card)+r'"',cards),(rid,'card binding')
  with Image.open(path(card)) as im:im.verify()
  records.append(dict(room=rid,registration_count=len(regs),card_sha256=sha(path(card)),view=entry['view']))
 out=path('output/wall-rollout-final-bindings.json');out.write_text(json.dumps(dict(rooms=records,source_versions=versions,registrations=registrations),indent=2)+'\n')
 print(f'BINDINGS PASS: {len(records)} live rooms/cards, {registrations} registrations, {versions} immutable source versions')
if __name__=='__main__':main()
