"""Install the Command palette repaint while preserving its registered geometry."""
import json,hashlib,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'assets/command-owner-v2';PACK.mkdir(exist_ok=True)
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-9921f8de-eeea-4a80-aa5e-60dd268c5559.png')
dst=PACK/'riser.png';shutil.copyfile(raw,dst)
original=PACK/'riser-original-registration.json'
base=json.loads(original.read_text()) if original.exists() else json.loads((ROOT/'assets/room-risers-v2/registrations.json').read_text())['command_center']
assert list(Image.open(dst).size)==base['native_size']
entry=dict(base)
entry.update(source='res://assets/command-owner-v2/riser.png',sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),stage='Integrated; native review pending',review='Matte charcoal and muted red repaint; original geometry and architectural fittings retained')
entry.pop('card',None);entry.pop('card_sha256',None)
p=ROOT/'assets/room-risers-v2/registrations.json';d=json.loads(p.read_text());d['command_center']=entry;p.write_text(json.dumps(d,indent=2)+'\n')
p=ROOT/'assets/room-risers-v3/registrations.json';d=json.loads(p.read_text());d.pop('command_center',None);p.write_text(json.dumps(d,indent=2)+'\n')
(PACK/'riser-original-registration.json').write_text(json.dumps(base,indent=2)+'\n')
