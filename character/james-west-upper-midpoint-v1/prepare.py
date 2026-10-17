from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
sources=[r/'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png',r/'character/james-cargo-return-bridges-v1/frames-v9/bare/001.png',r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png']
hashes={}
for name,source in zip(['entry','target','exit'],sources):
    im=Image.open(source).convert('RGBA');assert im.size==(256,256)
    im.crop((96,56,176,136)).resize((640,640),Image.Resampling.NEAREST).save(p/(name+'.png'))
    hashes[source.relative_to(r).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
prompt='''Use case: precise-object-edit. Edit image1, the target upper-body crop, into ONE midpoint pose of James settling from image2 (actual incoming profile-left pose) to image3 (actual outgoing slightly three-quarter-left pose). Image2 and image3 are immutable identity, size, perspective and matte material references. Output a SINGLE transparent640square crop with exactly the same framing and margins as image1. This is a very small shoulder/collar and gaze adjustment, about halfway between the two endpoints, not a new turn or nod.

Maintain the same mature man, grey-brown hair, forehead goggles, moustache, facial proportions, graphite matte suit, muted ochre yellow shoulder and original equipment/insignia. Match the native painted detail density of the endpoints; no polished portrait rendering, larger face, pink/purple skin, warm grade or shiny highlights. The crop represents original native80square from(96,56)..(176,136), enlarged8x for editing. Crown should sit at y20native/160output; same head width/height and collar attachment as endpoints. Preserve overall placement: no translation, zoom, tight crop or vertical head movement. Redraw head, collar and upper shoulder together as a coherent anatomical halfway orientation. Keep original lower crop portion below y54native/432output and backpack shape stable. No text, sheet, extra pose, border or background.'''
(p/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
for name in ['entry.png','target.png','exit.png','prompt.txt']:
    hashes[(p/name).relative_to(r).as_posix()]=hashlib.sha256((p/name).read_bytes()).hexdigest()
(p/'inputs.json').write_text(json.dumps({'sources':[x.relative_to(r).as_posix() for x in sources],'preCallSha256':hashes,'crop':[96,56,176,136],'selected':False},indent=2)+'\n')
print('Single midpoint target and exact endpoint references saved;input hashes frozen.')
