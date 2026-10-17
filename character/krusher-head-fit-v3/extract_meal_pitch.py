from pathlib import Path
from PIL import Image
import hashlib,json
P=Path(__file__).resolve().parent;raw=Image.open(P/'generated-meal-pitch.png').convert('RGBA');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
regions={ 'bare-south-deep':{'box':[205,164,633,705],'size':[24,30]},'bare-south-fully-bowed':{'box':[1169,212,1592,716],'size':[24,29]} }
for k,q in regions.items():
 im=raw.crop(q['box']).resize(q['size'],Image.Resampling.NEAREST);out=P/'sources'/f'{k}-native.png';im.save(out);q.update(source='generated-meal-pitch.png',sourceHash=sha(P/'generated-meal-pitch.png'),output=out.relative_to(P).as_posix(),outputHash=sha(out))
(P/'meal-pitch-extraction.json').write_text(json.dumps({'regions':regions,'method':'Whole isolated authored alpha components, preserved alpha and nearest native extraction; no generated suit or painted neck bridge.'},indent=2)+'\n')
print('Two South pitched source masters extracted')
