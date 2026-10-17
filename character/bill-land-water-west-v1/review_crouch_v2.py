from pathlib import Path
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
import numpy as np
import json

P = Path(__file__).resolve().parent
raw = Image.open(P/'sources/crouch-canvas-v2.png').convert('RGBA')
a = np.array(raw)
components, _ = label(a[:,:,3] > 250)
counts = np.bincount(components.ravel())
mask = binary_dilation(components == np.argmax(counts[1:])+1, iterations=3) & (a[:,:,3] > 0)
a[~mask] = 0
im = Image.fromarray(a).resize((320,320), Image.Resampling.LANCZOS)
b = np.array(im)
yy, xx = np.indices(b.shape[:2])
boot = (b[:,:,3]>180) & (xx>=130) & (xx<205) & (yy>=190) & (yy<260)
assert boot.any()
sole = int(yy[boot].max())+1
dy = 224-sole
out = Image.new('RGBA',(320,320))
out.paste(im,(0,dy))
assert np.count_nonzero(np.array(out)[:,:,3]) == np.count_nonzero(b[:,:,3])
out.save(P/'sources/crouch-native-v2.png')
out.resize((1280,1280),Image.Resampling.NEAREST).save(P/'sources/reference-crouch-v2-4x.png')
names = ['exact idle','old crouch','new crouch candidate','compact lift']
files = ['reference-idle-native.png','crouch-native-v1.png','crouch-native-v2.png','lift-native-v2.png']
board = Image.new('RGB',(1280,360),'#182932')
d = ImageDraw.Draw(board)
for i,(name,file) in enumerate(zip(names,files)):
    pose = Image.open(P/'sources'/file).convert('RGBA')
    board.paste(pose,(i*320,25),pose)
    d.text((i*320+5,5),name,fill='white')
    d.line((i*320,249,i*320+319,249),fill='#6aa39e')
board.save(P/'crouch-v2-review.png')
record = {'generation':'exec-a2fb1022-f360-4646-a091-b57fe9f588bd','rawCanvas':raw.size,'wholeCanvasScale':320/raw.width,'translation':[0,dy],'soleBefore':sole,'soleRegistered':224,'paintedSupportPreserved':True,'visualAcceptance':'pending common-ruler review'}
(P/'crouch-v2-registration.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
