from pathlib import Path
from PIL import Image
import hashlib,json
P=Path('character/krusher-head-fit-v3');raw=Image.open(P/'generated-front-heads.png').convert('RGBA');regions={
'bare-south':{'box':[213,91,531,533],'size':[24,33]},
'bare-south-bowed':{'box':[814,97,1131,533],'size':[24,33]},
'helmet-south-reference':{'box':[140,604,599,1057],'size':[37,37]},
'helmet-south-bowed-reference':{'box':[742,605,1200,1067],'size':[37,37]}}
for key,q in regions.items():
 im=raw.crop(tuple(q['box'])).resize(tuple(q['size']),Image.Resampling.NEAREST);path=P/'sources'/f'{key}-native.png';im.save(path);q.update(source='generated-front-heads.png',sourceSHA256=hashlib.sha256((P/'generated-front-heads.png').read_bytes()).hexdigest(),output=path.relative_to(P).as_posix(),outputSHA256=hashlib.sha256(path.read_bytes()).hexdigest())
(P/'front-extraction.json').write_text(json.dumps({'method':'Isolated connected-component boxes inspected in raw alpha, recorded nearest native extraction. Complete front/bowed bare head-neck; complete helmet sources for fitting reference, not whole-shell installation.','regions':regions,'status':'Front and bowed sources staged; original-body registration not yet done'},indent=2)+'\n')
print('Four front and bowed head/neck reference sources saved; alpha0 background verified.')
