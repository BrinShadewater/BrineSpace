from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent
im=Image.open(p/'midpoint.png').convert('RGBA');im.crop((88,152,168,232)).resize((640,640),Image.Resampling.NEAREST).save(p/'lower-target.png')
prompt='''EDIT TARGET: the supplied square crop of James carrying, containing hips/knees/shins/boots. Repair only the lower legs below the kneepads to restore original standing height. Preserve exact diagonal45degree orientation, existing two planted boots, muted graphite quilted trousers, worn silver shin straps/boot material and overall width. Current boot soles stop at86.25percent of crop height. The required ground baseline is90percent of crop height: extend the lower shin sections by exactly3/80 of this square canvas height, moving both complete existing boots vertically DOWN by3.75percent of canvas height (24pixels on supplied640 image). Same knee positions, same foot shapes and left/right separation, both boots flat at the new common baseline. Keep upper hips/thighs/kneepads exactly as supplied. No walking, stride, crossing, splaying feet, head or new objects. Do NOT move or scale the whole figure; this is a tiny lower-shin length correction only, keeping the fixed crop/composition, widths and material. Genuine transparent background; preserve empty margins, no floor/shadow, no text. Return one same square crop.'''
(p/'lower-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[p/'midpoint.png',p/'lower-target.png',p/'lower-prompt.txt',Path(__file__)]
(p/'lower-inputs.json').write_text(json.dumps({'preCallSha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':[88,152,168,232],'admissionRegion':[94,178,160,224],'targetSoleExclusive':224,'selected':False},indent=2)+'\n',encoding='utf-8')
print('Lower-shin correction target and bounded admission frozen; existing upper body protected.')
