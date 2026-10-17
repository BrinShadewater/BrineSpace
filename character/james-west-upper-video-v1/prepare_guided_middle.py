from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
source=r/'character/james-cargo-turn-south-west-v1/frames/bare/carry-turn-south-west/004.png'
im=Image.open(source).convert('RGBA').crop((96,56,176,136)).resize((640,640),Image.Resampling.LANCZOS)
im.save(p/'guided-middle-input.png')
prompt='''Edit IMAGE 1 only: this is an existing James intermediate turning pose and is the EXACT POSE/FRAMING TARGET. Image 2 is the outgoing West master for material and facial identity only, NOT a replacement pose. Preserve image 1's intermediate left-facing head angle, nose/ear/eye positions, head scale/crown position, neck/collar angle, shoulder/backpack silhouette, fixed original square margins and hand positions. Do not copy image 2's orientation or recenter/resize the sprite. This must remain the same distinct intermediate pose as image 1. No nod, head translation, pose rotation or detached head overlay.

Correct the target's finish to match the original West master: same subdued matte neutral graphite cloth, grey-brown hair, restrained natural warm skin, muted engineering ochre patches, worn grey fittings. Preserve original patch symbol and identity, goggle shape, mature moustached face, fine painted game sprite detail density. No purple/magenta cast, enlarged face/badge, exposure lift, glossy shine, black shadow expansion or invented detail. Retain GENUINE TRANSPARENCY with clean antialiased edges, preserving grey hair and silver fittings; no halo/checkerboard/backdrop/text. Keep the entire original square target crop unchanged in scale and registration. ONE coherent head/collar/shoulder/backpack upper pose only, preserving the target anatomy; this is master material/identity consistency work.'''
(p/'guided-middle-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
names=['guided-middle-input.png','last-input.png','guided-middle-prompt.txt']
(p/'guided-middle-inputs.json').write_text(json.dumps({'source':source.relative_to(r).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop':[96,56,176,136],'uniformEnlargement':8,'preCallSha256':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in names},'selected':False},indent=2)+'\n',encoding='utf-8')
print('Existing phase4 pose cropped at common80 registration,8x;material-only target/reference hashes frozen.')
