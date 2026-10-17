from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-coherent-video-v328';o.mkdir(exist_ok=True)
sources=[r/'character/james-cargo-half-turns-v1/frames/bare/carry-turn-south-north/010.png',r/'character/james-cargo-material-joined-v1/frames/bare/unload-north/005.png']
for source,name in zip(sources,['first.png','last.png']):
    im=Image.open(source).convert('RGBA');bg=Image.new('RGB',im.size,(48,59,64));bg.paste(im,(0,0),im);bg.resize((768,768),Image.Resampling.NEAREST).save(o/name)
prompt='''Fixed camera game sprite animation. The engineer faces directly away throughout. He gently bends his hips and knees a little, lowers the case carried in front of him onto the floor just ahead of his boots, releases it, and rises smoothly to the exact final standing pose. Both boots stay planted in the same narrow stance; knees stay above the boots without spreading sideways. Keep the backpack, suit, belt wrench, head proportions and matte graphite/yellow materials consistent. The wrench stays on his belt. The case ends on the floor in front of him and is partly visible between his legs from behind. Smooth continuous controlled bend and rise, no deep squat, extra gesture, rotation, step or camera motion. Preserve original character scale, floor contact, flat dark background and lighting throughout.'''
(o/'prompt.txt').write_text(prompt)
(o/'inputs.json').write_text(json.dumps(dict(sources=[dict(path=str(f.relative_to(r)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sources],firstSha256=hashlib.sha256((o/'first.png').read_bytes()).hexdigest(),lastSha256=hashlib.sha256((o/'last.png').read_bytes()).hexdigest(),wholeSourceScale=3,background=[48,59,64],promptSha256=hashlib.sha256(prompt.encode()).hexdigest(),normalChanged=False,originalMasterAuthority='character/branforth-west-direct-v2/master-input.png'),indent=2)+'\n')
print('Prepared exact whole-source first/last references; equal768 canvases; no source pose fitting.')
