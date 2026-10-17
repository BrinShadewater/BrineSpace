from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-east-inspect-body-grade-v24';d=json.loads((out/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/f).read_bytes()).hexdigest()==v for f,v in d['preCallSha256'].items())
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
study=raw.resize((184,184),Image.Resampling.LANCZOS);study.save(out/'native-material-study.png')
master=Image.open(r/d['masterFile']).convert('RGBA');base=Image.open(r/d['baseFile']).convert('RGBA')
board=Image.new('RGBA',(3*368,394),(48,59,63,255));draw=ImageDraw.Draw(board)
for i,(im,label) in enumerate([(master,'selected idle master'),(base,'normal inspect70'),(study,'generated material study')]):
    board.alpha_composite(im.resize((368,368),Image.Resampling.NEAREST),(i*368,26));draw.text((i*368+4,7),label,fill='white')
board.convert('RGB').save(out/'comparison.png')
a=np.array(base)[:,:,3]>=128;b=np.array(study)[:,:,3]>=128
(out/'review.json').write_text(json.dumps(dict(rawSha256=hashlib.sha256((out/'raw.png').read_bytes()).hexdigest(),sourceAlpha128MismatchPixels=int(np.count_nonzero(a!=b)),
    sourceAlpha128Bounds=base.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox(),studyAlpha128Bounds=study.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox(),
    visualReviewPending=True,sourceAcceptance=False,selected=False,normalChanged=False,
    scope='One generated color/material reference, native184 resize once. No original-pose/alpha protection, no full141-frame repair or runtime acceptance inferred.'),indent=2)+'\n')
print('Three-source material comparison prepared; no pose protection or normal adoption claimed.')
