from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;V=P/'continuous-video-v1';D=P/'whole-source-grade-edit-v1';D.mkdir(exist_ok=True)
atlas=Image.new('RGBA',(2048,1024));bindings={}
for i in range(32):
 path=V/f'full-clip-frames/{i+32:03}.png';im=Image.open(path).convert('RGBA');assert im.size==(256,256)
 atlas.alpha_composite(im,((i%8)*256,(i//8)*256));bindings[path.relative_to(P).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
atlas.save(D/'edit-target.png')
(D/'target-record.json').write_text(json.dumps({'grid':[8,4],'cellSize':[256,256],'sourceFrames':list(range(32,64)),'bindings':bindings,'scope':'Exact complete fixed-registration RGBA source frames pasted into32-cell atlas without resizing, RGB, alpha or anatomy edits. Built-in whole-source material edit target only.'},indent=2)+'\n',encoding='utf-8')
print('Exact32-frame complete-figure edit atlas saved,2048x1024.')
