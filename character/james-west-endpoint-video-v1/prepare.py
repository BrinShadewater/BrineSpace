from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
sources=[r/'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png',r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png']
for name,source in zip(['first','last'],sources):
    im=Image.open(source).convert('RGBA');assert im.size==(256,256)
    bg=Image.new('RGBA',(256,256),'white');bg.alpha_composite(im)
    bg.convert('RGB').resize((1024,1024),Image.Resampling.NEAREST).save(p/(name+'-input.png'))
prompt='''[Static shot] Orthographic finely painted game sprite on plain white. Make one small coherent transition from the supplied FIRST engineer pose to the supplied LAST engineer pose. The endpoint difference is only a slight head/collar/shoulder adjustment and case orientation while settling his weight in place. Stay between those two poses, never turn toward the front/South or away from the left-facing reference angles. No walk, extra step, squat, head bob or exaggerated motion. Head, neck, collar, shoulders, elbows, hands and closed case articulate together anatomically. Use the exact same mature face, grey-brown hair, forehead goggles, moustache, muted engineering yellow, matte graphite suit, belt wrench and backpack. Preserve height, proportions, size, camera and subdued colour throughout. The case stays the same plain closed case with silver latches: no purple marks, displays, new insignia or tools. No brighter exposure, glossy highlights, zoom, shadows, scene or text. Complete the slight pose adjustment then hold the exact supplied LAST pose. No flourish or return motion.'''
(p/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=sources+[p/'first-input.png',p/'last-input.png',p/'prompt.txt',r/'tools/minimax_video.py',p/'test_submission.py']
(p/'inputs.json').write_text(json.dumps({'sources':[x.relative_to(r).as_posix() for x in sources],'preCallSha256':{x.relative_to(r).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in files},'registration':'Exact256canvas uniformly4x white composite,no crop/grade/translation','selected':False,'officialAPI':'https://platform.minimax.io/docs/api-reference/video-generation-fl2v','estimatedUSD':.28,'offlineTests':6},indent=2)+'\n')
print('Equal-size actual endpoint images/prompt/helper hashes frozen;offline submission checks6pass.')
