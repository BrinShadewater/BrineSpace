from pathlib import Path
from PIL import Image
import imageio.v2 as iio
import hashlib,json
p=Path(__file__).resolve().parent
reader=iio.get_reader(str(p/'source.mp4'));frames=[Image.fromarray(x[:,:,:3]) for x in reader];reader.close()
indices=[35,70,105,135];atlas=Image.new('RGB',(1280,1280),'white')
for j,i in enumerate(indices):
    atlas.paste(frames[i].resize((640,640),Image.Resampling.LANCZOS),((j%2)*640,(j//2)*640))
atlas.save(p/'rephase-target.png')
prompt='''Edit image 1 ONLY, a 2x2 equal-square-cell atlas containing FOUR different consecutive video poses of James. Image 2 is his exact original incoming upper-body master; image 3 is his exact outgoing upper-body master. They specify identity and matte palette, NOT replacement poses. Preserve the target's four distinct orientations in reading order: top-left, top-right, bottom-left, bottom-right. Preserve exact crop margins, size, positions, head silhouette, nose/ear/moustache geometry, goggles, neck/collar, shoulder pose, patch outline and badge symbol, backpack and visible hands. Do not redraw or copy a reference pose into a target cell. Keep the equal four-cell grid and original full margins. No independent fit, zoom, recentering, new pose, larger face, enlarged patch or added detail.

Make ONLY two corrections: (1) remove purple/magenta tint consistently across all four cells, matching the references' neutral MATTE graphite suit/collar/backpack, grey-brown hair, subdued warm skin and muted ochre-yellow patches; no exposure lift, orange skin, glossy shine or broad black shadows. (2) remove the plain white background to GENUINE TRANSPARENCY, retaining clean antialiased edges and all real grey hair/silver fittings. No white halo, checkerboard image, drop shadow or new backdrop. Maintain the source's progressive small profile-left to three-quarter-left head/neck/shoulder articulation. Colour consistency must not erase differences between poses. This is a colour and alpha edit, not anatomy generation. Output the complete square 2x2 atlas, transparent outside the four original upper-body silhouettes, no text or dividers.'''
(p/'rephase-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
names=['source.mp4','rephase-target.png','first-input.png','last-input.png','rephase-prompt.txt']
(p/'rephase-inputs.json').write_text(json.dumps({'indices':indices,'preCallSha256':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in names},'selected':False},indent=2)+'\n',encoding='utf-8')
print('Four source phases35/70/105/135 frozen; latest sample approaches true terminal141. No video regeneration.')
