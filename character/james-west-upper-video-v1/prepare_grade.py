from pathlib import Path
from PIL import Image
import imageio.v2 as iio
import hashlib,json
p=Path(__file__).resolve().parent
reader=iio.get_reader(str(p/'source.mp4'));frames=[Image.fromarray(x[:,:,:3]) for x in reader];reader.close()
indices=[28,56,84,112];atlas=Image.new('RGB',(1280,1280),'white')
for j,i in enumerate(indices):
    crop=frames[i].resize((640,640),Image.Resampling.LANCZOS);crop.save(p/('grade-input-%03d.png'%i))
    atlas.paste(crop,((j%2)*640,(j//2)*640))
atlas.save(p/'grade-target.png')
prompt='''Use case: lighting-weather colour correction. Edit image1 ONLY: a2x2 equal-cell atlas of FOUR consecutive James upper-body poses, order top-left,top-right,bottom-left,bottom-right. Image2 and image3 are exact incoming/outgoing palette and matte material masters. Keep this EXACT2x2 grid, identical square crop framing, pixel positions, head size, anatomy, face identity and FOUR DIFFERENT pose orientations. This is COLOUR GRADING ONLY, not redrawing poses or changing geometric placement. Preserve every silhouette, feature, seam, shoulder patch symbol and backpack shape. Keep full original margins; do not zoom or independently crop any cell.

Remove the temporal purple/magenta cast from hair, suit, collar and silver cuffs, especially lower cells. Match ALL four cells to the SAME neutral matte graphite fabric, grey-brown hair, warm natural skin and subdued muted engineering ochre-yellow of endpoint references. No purple hair/fabric, glossy highlights, exposure lift, bright yellow, black shadow expansion or new details. Do not make faces larger/sharper or redesign insignia. Original source movement must remain unchanged; ONLY uniform consistent endpoint-matched colour/material appearance. Keep existing plain white background and full2x2 layout, no alpha checkerboard, text, dividers, new character, tools or poses.'''
(p/'grade-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
names=['source.mp4','grade-target.png','first-input.png','last-input.png','grade-prompt.txt']
(p/'grade-inputs.json').write_text(json.dumps({'indices':indices,'preCallSha256':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in names},'selected':False},indent=2)+'\n')
print('Four true video poses28/56/84/112 assembled at common scale;grade-only prompt and hashes frozen.')
