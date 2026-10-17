from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent
Image.open(p/'candidate.png').convert('RGBA').crop((96,56,176,136)).resize((640,640),Image.Resampling.NEAREST).save(p/'midpoint-reference.png')
base='''Edit image1 (new James midpoint) to ONE adjacent pose, preserving its exact transparent square framing, mature face identity, grey-brown hair, forehead goggles, moustache, head/collar size and muted matte charcoal/ochre material. Image2 is exact incoming profile-left endpoint; image3 is exact outgoing slightly three-quarter-left endpoint. This is a very small upper shoulder/collar and gaze change, no head nod, vertical translation or new turn. The midpoint is the shared size/identity anchor, do not independently redesign him. Native80square crop from global(96,56)..(176,136), enlarged8x, crown at nativey20. Keep original margins and scale, no zoom/crop, no larger warmer/purple face, no shine, no emblem redesign. Preserve backpack and lower crop below y54native. Output ONE transparent square pose only, no text or atlas.
'''
for name,phase in [('early','Produce the EARLY pose,25percent from incoming to outgoing, halfway between incoming endpoint and midpoint. Turn very slightly less toward viewer than image1.'),('late','Produce the LATE pose,75percent from incoming to outgoing, halfway between midpoint and outgoing endpoint. Turn very slightly more toward viewer than image1.')]:
    (p/(name+'-prompt.txt')).write_text(base+phase+'\n',encoding='utf-8')
files=['midpoint-reference.png','entry.png','exit.png','early-prompt.txt','late-prompt.txt','raw.png','candidate.png']
(p/'adjacent-inputs.json').write_text(json.dumps({n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in files},indent=2)+'\n')
print('Adjacent-pose prompts and exact midpoint references frozen.')
