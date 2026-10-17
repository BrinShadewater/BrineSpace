from pathlib import Path
import json,hashlib
from PIL import Image,ImageSequence
P=Path(__file__).resolve().parent;R=P.parents[1]
m=json.loads((P/'manifest.json').read_text());s=json.loads((P/'selection.json').read_text())
assert s['sourceSha256']==hashlib.sha256((P/'source.png').read_bytes()).hexdigest()
assert len(m['states'])==7
refs=0
for state in m['states']:
    assert len(state['frameFiles'])==len(state['frameDurationsMs'])
    for f in state['frameFiles']:
        Image.open(R/f.removeprefix('res://') if f.startswith('res://') else P/f).verify();refs+=1
gif=Image.open(P/'native-course-review.gif');durations=[x.info.get('duration',0) for x in ImageSequence.Iterator(gif)]
assert sum(durations)==9000
result={'states':7,'imageReferences':refs,'sourceHashExact':True,'previewFrames':len(durations),'gifMilliseconds':sum(durations),'sourceClockMilliseconds':9000,'scope':'Selection references and source-event preview; GIF centisecond quantization. Native evidence is in selection.json.'}
(P/'selection-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
