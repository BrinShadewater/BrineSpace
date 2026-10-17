from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-normal-motion-v1';checks=0
for gear in ['bare','helmet']:
    for prop in ['neutral','tablet']:
        name=gear+'-'+prop;movie=Image.open(P/(name+'-native-motion.png'));assert movie.n_frames==49;checks+=1
        for tick in range(49):
            movie.seek(tick);native=Image.open(O/(name+'-tick-%02d-room.png'%tick)).convert('RGB').crop((490,286,660,424))
            assert np.array_equal(np.array(movie.convert('RGB').crop((266,42,436,180))),np.array(native));checks+=1
path=P/'motion-review-evidence.json';data=json.loads(path.read_text());data['losslessDecodedNativeChecks']=checks
data['visualReview']='all4contact-sheets/all196native-presentations-reviewed'
data['visualCriteria']=['complete sampled native finite sequences visible against sofa and floor','helmet attached at every recorded pitch','matte head/suit colours and body ruler compared with reviewed paired sources/master','exact source/native room pixels retained in APNG']
data['visualLimits']='All 30fps native frames reviewed as contact sheets; previews available for playback. This does not certify natural world cadence, traffic, hazards, title/new-process Continue or final owner acceptance.'
path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'reviewedNativeFrames':196}))
