from pathlib import Path
import json,hashlib,shutil
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];old=R/'character/james-interact-east-direct-v1'
ref=json.loads((old/'reference.json').read_text());master=R/ref['source'];assert hashlib.sha256(master.read_bytes()).hexdigest()==ref['sourceSha256']
current=Image.open(R/'character/james-inspect-material-continuity-v1/frames/bare/east/000.png').convert('RGBA');assert current.tobytes()==Image.open(master).convert('RGBA').tobytes()
shutil.copy2(old/'master-input.png',P/'master-input.png')
(P/'reference.json').write_text(json.dumps({'source':master.relative_to(R).as_posix(),'sourceSha256':ref['sourceSha256'],'masterInputSha256':hashlib.sha256((P/'master-input.png').read_bytes()).hexdigest(),'method':'Exact selected East idle master and prior approved green-screen4x input reused. No new identity or per-pose registration.','reason':'All-frame transition detail shows actual East belt wrench leaves belt and transforms into tablet in source8..24. Remake whole motion, retaining fixed wrench and separate rectangular tablet pouch.','productionInstalled':False},indent=2),encoding='utf-8')
print('Exact current East master/input and prompt preserved; one new source candidate.')
