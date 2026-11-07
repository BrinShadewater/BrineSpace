"""Install a Tidal-only riser palette without changing shared engineering art."""
import json,hashlib,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/rooms/tidal-condenser/pack'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-10470a8c-99c3-438e-ae98-288f451c407d.png')
target=PACK/'riser.png';shutil.copyfile(raw,target)
source=ROOT/'assets/riser-departments-v1/engineering/source.png'
assert Image.open(target).size==Image.open(source).size
base=json.loads((ROOT/'assets/riser-departments-v1/registrations.json').read_text())['engineering']
entry=dict(base);entry.update(source='res://assets/rooms/tidal-condenser/pack/riser.png',sha256=hashlib.sha256(target.read_bytes()).hexdigest(),review='Tidal grey-blue panel and dull-brass pipe repaint; original face/cap rectangles retained')
p=ROOT/'assets/room-risers-v3/registrations.json';d=json.loads(p.read_text());d['tidal_condenser']=entry;p.write_text(json.dumps(d,indent=2)+'\n')
print('Tidal override installed; dimensions',Image.open(target).size)
