from pathlib import Path
import json,hashlib
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1]
path=r/'character/james-cargo-return-bridges-v1/bare-joined-manifest-v9.json';m=json.loads(path.read_bytes());s=m['states'][0]
sources=[r/file[6:] if file.startswith('res://') else path.parent/file for file in s['frameFiles']]
box=(96,56,176,136);atlas=Image.new('RGBA',(1280,1280));hashes={}
for i,source in enumerate(sources):
    im=Image.open(source).convert('RGBA');assert im.size==(256,256)
    crop=im.crop(box).resize((640,640),Image.Resampling.NEAREST)
    if i in [0,5]:crop.save(p/('entry.png' if i==0 else 'exit.png'))
    else:atlas.alpha_composite(crop,(((i-1)%2)*640,((i-1)//2)*640))
    hashes[source.relative_to(r).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
atlas.save(p/'target-atlas.png')
prompt='''Edit the FIRST transparent2x2 atlas only. It contains the FOUR consecutive intermediate upper-body crops of James between the SECOND reference (actual carry-turn entry) and THIRD reference (actual unload-ready/walking-carry exit). Keep the same2x2 equal-cell atlas, complete80-square framing in every cell, transparent background and identical scale/position. Read temporal order top-left, top-right, bottom-left, bottom-right. The originals currently switch head/collar orientation abruptly between the middle two cells. Redraw all FOUR heads/collars/upper shoulders TOGETHER into a coherent sequence of small evenly distributed orientation changes from entry to exit. This is a slight profile-left to three-quarter-left settling movement, never a full turn or a head nod.

Use the endpoint references as exact identity/style/size masters: same mature grey-brown-haired man, goggles on forehead, moustache, neutral skin, matte charcoal fabric, muted yellow patches and original emblem/backpack equipment. Keep crown at approximately20crop-pixels, collar and shoulder attachment consistent. Do not enlarge his face, invent insignia, warm the grade, turn purple, add shine, move his head vertically, or alter perspective. Preserve the source chest/shoulder structure and material; head, neck/collar and shoulder articulation must advance smoothly and anatomically rather than switching as one pasted rectangle. Preserve all margins and physical registration: every cell80square, crop corresponds to native global(96,56)..(176,136); no tight crops, no independent scale fitting, no cell placement shifts. Keep source pixels below crop y54 unchanged where possible; lower body/case/hands will remain original in final packaging. Four crops of the SAME man with smooth progressive pose only, no labels, dividers, duplicate unrelated faces or extra equipment.'''
(p/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
for name in ['prompt.txt','target-atlas.png','entry.png','exit.png']:
    hashes[(p/name).relative_to(r).as_posix()]=hashlib.sha256((p/name).read_bytes()).hexdigest()
(p/'inputs.json').write_text(json.dumps({'sources':[x.relative_to(r).as_posix() for x in sources],'crop':box,'preCallSha256':hashes,'selected':False},indent=2)+'\n')
print('Four upper intermediates assembled without source changes; endpoints/prompt/pre-call hashes saved.')
