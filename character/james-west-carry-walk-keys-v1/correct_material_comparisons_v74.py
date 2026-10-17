from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'comparison-corrections-v74';out.mkdir(exist_ok=True)
spec=[(1,66),(12,51),(22,64),(23,58),(24,52),(25,59),(26,65),(36,53),(47,67),(48,55)]
master=Image.open(r/'character/james-west-master-carry-v1/registered-original-master.png').convert('RGBA')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();records=[]
for group in range(2):
    summary=Image.new('RGBA',(768,1400),(47,58,63,255));draw=ImageDraw.Draw(summary)
    for row,(phase,version) in enumerate(spec[group*5:group*5+5]):
        folder=p/f'master-material-phase{phase}-v{version}'
        paired=Image.new('RGBA',(768,560),(47,58,63,255));pd=ImageDraw.Draw(paired)
        for gear,mode in enumerate(['bare','helmet']):
            for col,(label,f) in enumerate([('actual before',p/f'master-head-review-v16/{mode}-{phase:03d}.png'),('protected candidate',folder/f'{mode}-head-protected.png'),('carry reference',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png' if mode=='bare' else r/'character/james-carry-authored-helmet-v1/frames/004.png')]):
                im=Image.open(f).convert('RGBA');paired.alpha_composite(im,(col*256,gear*280+24));pd.text((col*256+5,gear*280+5),f'{mode} phase{phase} {label}',fill='white')
                if col==0:
                    baseline=Image.new('RGBA',(256,256),(47,58,63,255));baseline.alpha_composite(im)
                    assert np.array_equal(np.asarray(baseline),np.asarray(paired.crop((0,gear*280+24,256,gear*280+280))))
        dest=folder/'paired-protected-review-index-corrected.png';paired.save(dest)
        before=Image.open(p/f'master-head-review-v16/bare-{phase:03d}.png').convert('RGBA')
        candidate=Image.open(folder/'bare-head-protected.png').convert('RGBA')
        for col,(label,im) in enumerate([('actual before',before),('protected candidate',candidate),('original master',master)]):
            summary.alpha_composite(im,(col*256,row*280+24));draw.text((col*256+5,row*280+5),f'phase{phase} {label}',fill='white')
        records.append(dict(phase=phase,version=version,correctedBoard=dest.relative_to(r).as_posix(),correctedSha256=sha(dest),historicalBoardSha256=sha(folder/'paired-protected-review.png'),baselineBothGearsPixelVerified=True,sourceSha256={m:sha(folder/f'{m}-head-protected.png') for m in ['bare','helmet']},sourceAcceptance=False))
    summary.save(out/f'master-comparisons-{group}.png')
(out/'inputs.json').write_text(json.dumps(dict(records=records,originalMasterSha256=sha(r/'character/james-west-master-carry-v1/registered-original-master.png'),normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
print('Ten corrected paired comparisons; twenty matching baseline crops pixel-verified. Original boards and source art retained.')
