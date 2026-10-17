"""Check material grade and explicitly scoped hand/pacing polish."""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent


def main():
    before = json.loads((HERE/'review-before-helmet-cadence/manifest.json').read_text())
    after = json.loads((HERE/'manifest.json').read_text())
    polish = json.loads((HERE/'polish-settings.json').read_text())
    registration = json.loads((HERE/'source-registration.json').read_text())
    checks = 0
    changed = 0
    lookup = {s['id']:s for s in after['states']}
    for a,b in zip(before['states'],after['states'],strict=True):
        assert b['frameDurationsMs']==polish['frameDurationsMs'][b['id']]
        checks+=1
        for index,(old,new) in enumerate(zip(a['frameFiles'],b['frameFiles'],strict=True)):
            x=np.asarray(Image.open(HERE/'review-before-helmet-cadence'/old))
            y=np.asarray(Image.open(HERE/new))
            assert x.shape==y.shape==(256,256,4)
            assert np.array_equal(x[:,:,3],y[:,:,3]),new
            if b['id']=='interact-west' and index in (1,2,3,4):
                record=registration['frames'][index]
                x0,y0,x1,y1=record['sourceBox']
                px,py=record['position']
                sy=round((y1-y0)*registration['scaleY'])/(y1-y0)
                bottom=int(np.ceil(py+52+71*sy))+4
                assert np.array_equal(x[bottom:],y[bottom:]),new
                assert np.any(x[:bottom,:,:3]!=y[:bottom,:,:3]),new
                checks+=1
            else:
                assert np.array_equal(x,y),new
            changed+=int(not np.array_equal(x,y))
            checks+=3
    def frame(key,index):
        return Image.open(HERE/lookup[key]['frameFiles'][index]).convert('RGBA')
    idle=Image.new('RGBA',(256,256))
    idle.alpha_composite(Image.open(HERE.parent/'bill-shared-helmet-runtime-v2/frames/idle-west/000.png').convert('RGBA'),(36,52))
    for key,i in [('interact-west',0),('interact-west',5),('kneel-west',0),('stand-west',5)]:
        assert frame(key,i).tobytes()==idle.tobytes()
        checks+=1
    for a,b in [('kneel-west','repair-west'),('repair-west','stand-west')]:
        assert frame(a,5).tobytes()==frame(b,0).tobytes()
        checks+=1
    a=json.loads((HERE/'review-before-grade/source-registration.json').read_text())
    b=json.loads((HERE/'source-registration.json').read_text())
    a.pop('grade'); b.pop('grade')
    assert a==b
    assert b['sourceSha256']==hashlib.sha256((HERE/'sources/actions.png').read_bytes()).hexdigest()
    checks+=2
    report={'checks':checks,'failures':0,'changedRgbFrames':changed,'handCleanupFrames':[1,2,3],'alphaAndNonHelmetPixelsPreserved':True,'timingMatchesPolishSettings':True,'sourceAndRegistrationPreserved':True,'ownerAcceptance':'pending'}
    (HERE/'grade-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
    review=Image.new('RGB',(840,420))
    draw=ImageDraw.Draw(review)
    for row,bg in enumerate([(30,43,53),(176,182,178)]):
        draw.rectangle((0,row*210,840,(row+1)*210),fill=bg)
        for col,(root,rel,name) in enumerate([
            (HERE.parent,'bill-shared-helmet-runtime-v2/frames/idle-west/000.png','Accepted idle'),
            (HERE/'review-before-helmet-cadence','frames/interact-west/002.png','Before helmet'),
            (HERE,'frames/interact-west/002.png','Graded helmet'),
            (HERE,'frames/repair-west/002.png','Repair'),
        ]):
            im=Image.open(root/rel).convert('RGBA')
            if im.size==(256,256): im=im.crop((36,52,220,236))
            draw.text((col*210+8,row*210+8),name,fill='white' if row==0 else 'black')
            for j,height in enumerate([82,54,27]):
                factor=height/152
                small=im.resize((round(184*factor),round(184*factor)),Image.Resampling.BILINEAR)
                review.paste(small,(col*210+j*65+3,row*210+150-round(175*factor)),small)
    review.save(HERE/'gameplay-grade-review.png')


if __name__=='__main__':main()
