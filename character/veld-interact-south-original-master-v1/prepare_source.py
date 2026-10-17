from pathlib import Path
import hashlib,json,shutil
from PIL import Image
P=Path(__file__).resolve().parent
R=P.parents[1]
original=R/'character/veld-idle-south-original-master-v1/original-idle-master.png'
assert not (P/'generation.json').exists()
for name in ['original-idle-master.png','prepared-idle-master.png']:
    shutil.copyfile(original,P/name)
im=Image.open(original).convert('RGBA')
assert im.size==(256,256)
bg=Image.new('RGB',(768,768),(12,18,24))
large=im.resize((768,768),Image.Resampling.NEAREST)
bg.paste(large,(0,0),large)
bg.save(P/'master-input.png')
prompt='A fixed-camera front-facing full-body game character animation. Keep this exact woman, her warm natural skin, dark brown hair, detailed matte charcoal quilted suit, blue arm patches, height, head size and proportions throughout. She stays facing directly toward the camera with feet planted in the exact reference stance. Perform ONE short scanner interaction: draw her small handheld scanner from the belt, hold it in front of her upper abdomen with both hands, look briefly down at its screen while operating it, then put it back and return to the exact starting relaxed standing pose. The scanner stays small and hands remain connected to the sleeves. No walking, turning, repeated gestures, body scaling or camera movement. Preserve the reference lighting and fine suit details, with no glow or changing colour grade. Start and finish in the supplied identical standing pose. Static flat dark background RGB 12,18,24.'
(P/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[original,P/'master-input.png',P/'prompt.txt']
(P/'INPUTS.json').write_text(json.dumps(dict(authority=original.relative_to(R).as_posix(),registration=dict(scale=1/3,offset=[0,0],standingHeight=148),method='Exact original native master enlarged uniformly 3x nearest onto dark background; identical first and last input. No appearance editing.',estimatedUSD=.28,billingVerified=False,bindings={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n',encoding='utf-8')
print('South original scanner inputs prepared; identical endpoints, fixed 148px ruler.')

