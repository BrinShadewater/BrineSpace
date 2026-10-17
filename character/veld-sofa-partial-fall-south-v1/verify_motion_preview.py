from pathlib import Path
import json
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-partial-south-motion-v1'
d=json.loads((P/'motion-review-evidence.json').read_text());checks=0
assert len(d['clips'])==24
for filename in d['clips']:
    name=filename.removesuffix('-native-motion.png');im=Image.open(P/filename)
    assert im.n_frames==49 and im.size==(446,300);checks+=1
    elapsed=0
    for tick in range(49):
        im.seek(tick);native=Image.open(O/(name+'-tick-%02d-room.png'%tick)).convert('RGB').crop((490,286,660,424))
        assert im.convert('RGB').crop((266,42,436,180)).tobytes()==native.tobytes();checks+=1
        duration=im.info['duration'];expected=33 if tick%3!=2 else 34
        assert duration==(expected if tick<48 else 800);checks+=1
        if tick<48:elapsed+=duration
    assert elapsed==1600;checks+=1
(P/'motion-preview-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'clips':24,'decodedNativeFrames':1176,'color':'exact RGB native crops, lossless APNG','timing':'48intervals1600ms,800msviewerterminalhold;repeat is viewerreset'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'decodedNativeFrames':1176}))
