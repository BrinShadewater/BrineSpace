from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
source=R/'character/veld-side-foundation-v1/side-master-01.png'
reference=json.loads((source.parent/'extraction.json').read_bytes())
assert hashlib.sha256(source.read_bytes()).hexdigest()==reference['source_sha256']
im=Image.open(source).convert('RGBA');a=np.asarray(im);lab,n=ndimage.label(a[:,:,3]>=128)
box=next(x['sourceBox'] for x in reference['figures'] if x['direction']=='west');x0,y0,x1,y1=box
crop=im.crop(box);part=lab[y0:y1,x0:x1];labels,counts=np.unique(part[part>0],return_counts=True);component=int(labels[np.argmax(counts)])
crop.putalpha(Image.fromarray(np.where(part==component,255,0).astype('uint8')))
assert np.array_equal(np.asarray(crop)[:,:,:3],a[y0:y1,x0:x1,:3])
scale=148/crop.height;small=crop.resize((round(crop.width*scale),148),Image.Resampling.LANCZOS)
control=Image.new('RGBA',(184,184));control.alpha_composite(small,((184-small.width)//2,24))
assert np.array_equal(np.asarray(control),np.asarray(Image.open(source.parent/'west-standing.png').convert('RGBA')))
# Preserve the original high-resolution colour/detail on a whole square ruler.
size=round(256/scale);offset=[round((128-small.width/2)/scale),round(76/scale)]
plate=Image.new('RGBA',(size,size));plate.alpha_composite(crop,offset);plate.save(P/'original-high-source-input.png')
plate.resize((256,256),Image.Resampling.LANCZOS).save(P/'high-source-control-native.png')
record=dict(source=str(source.relative_to(R)).replace('\\','/'),sourceSHA256=hashlib.sha256(source.read_bytes()).hexdigest(),cropBox=box,sourceCropSize=crop.size,backgroundExtraction='Identical alpha128 connected-component extraction used by original foundation; crop RGB untouched.',plateSize=size,offset=offset,scale=scale,originalNativeRebuildPixelDifferences=0,inputSHA256=hashlib.sha256((P/'original-high-source-input.png').read_bytes()).hexdigest(),scope='High-detail appearance guide only; high square control resampling is not byte-identical native master.')
(P/'HIGH_SOURCE_INPUT.json').write_text(json.dumps(record,indent=2)+'\n')
prompt='''Edit this original high-detail West-facing Veld master into one complete standing scientific scanner interaction pose. Keep her original small head, warm matte skin, brown bun, face, charcoal cloth value and texture, suit panels, belt and side equipment, narrow proportions, legs, boots and their stance exactly as the master. Only lift and bend her arms naturally forward: both gloved hands hold a small dark handheld instrument just left of her lower chest, one supporting the underside, one operating its tiny cyan screen. Continuous sleeves connect to her original shoulders; shoulder patch stays on the same arm. The cyan screen must not cast light onto the figure. Keep original neutral dark fabric shadows and fold highlights; do not brighten the trousers, make the suit blue-grey, add sheen or smooth away details. Strict West left-facing profile, same camera and native body density. Same full square canvas with exactly the master's framing, head top and foot floor; no zoom, re-centering, raised feet, new stance or head enlargement. Original face, hair and lower body should remain unchanged in appearance. Return ONE entire sprite on transparent background, no extra poses, text, floor, shadow, guides or background. The high-resolution master is the only visual authority; do not redesign the character.'''
(P/'high-source-prompt.txt').write_text(prompt+'\n')
print(f'Original high-detail input {size} square; native master rebuild 0 pixel differences')
