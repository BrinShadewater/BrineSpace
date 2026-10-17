from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path('character/james-west-carry-walk-keys-v1');o=p/'knee-protection-phase30-v142';o.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
roi=(108,157,127,183)
inputs={}; changed={}
for mode in ['bare','helmet']:
    original=p/f'master-head-review-v16/{mode}-030.png';prior=p/f'local-material-phase30-v138/{mode}-head-protected.png'
    base=np.array(Image.open(original).convert('RGBA'));candidate=np.array(Image.open(prior).convert('RGBA'));fixed=candidate.copy()
    x0,y0,x1,y1=roi;fixed[y0:y1,x0:x1]=base[y0:y1,x0:x1]
    assert np.array_equal(fixed[:,:,3],base[:,:,3])
    assert np.array_equal(fixed[y0:y1,x0:x1],base[y0:y1,x0:x1])
    outside=np.ones((256,256),bool);outside[y0:y1,x0:x1]=False
    assert np.array_equal(fixed[outside],candidate[outside])
    Image.fromarray(fixed).save(o/f'{mode}-head-protected.png')
    inputs[str(original)]=sha(original);inputs[str(prior)]=sha(prior)
    changed[mode]=int(np.any(fixed!=candidate,axis=2).sum())
board=Image.new('RGBA',(768,600),(47,58,63,255));draw=ImageDraw.Draw(board)
for col,(name,f) in enumerate([('Original30',p/'master-head-review-v16/bare-030.png'),('Prior V138',p/'local-material-phase30-v138/bare-head-protected.png'),('Protected knee V142',o/'bare-head-protected.png')]):
    im=Image.open(f).convert('RGBA');board.alpha_composite(im,(col*256,25));draw.text((col*256+5,5),name,fill='white')
    board.alpha_composite(im.crop((100,150,145,200)).resize((225,250),Image.Resampling.NEAREST),(col*256+15,320))
board.save(o/'knee-after-review.png')
(o/'package-review.json').write_text(json.dumps(dict(sourceSha256=inputs,retainedOriginalKneeRectangle=roi,changedPixelsFromV138=changed,alphaExact=True,allOutsideKneeExactToV138=True,operation='Restore original same-phase knee fitting and surrounding buffer; reuse V138 authored material everywhere else. No new generation.',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
print(json.dumps(changed))
