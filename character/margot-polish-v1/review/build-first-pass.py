"""Reproducible review pack. Authored images only, shared scale per source row."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
from extract import extract,DIRS,ROOT
REPO=ROOT.parents[1]
SCALE=.28
PIVOT=(92,172)

def hat(im):
    a=np.array(im).astype(int);r,g,b=a[:,:,:3].transpose(2,0,1)
    mask=(g>r)&(g>b+12)&(a[:,:,3]>128)
    y,x=np.where(mask)
    return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]

def anchor(im,d):
    a=np.array(im)[:,:,3]>128;y,x=np.where(a);bottom=y.max()+1
    near=(y>=bottom-12)
    if d=='west':near &= x<im.width*.58
    if d=='east':near &= x>im.width*.42
    return (float(np.median(x[near])) if near.any() else im.width/2,bottom)

def frame(im,d,scale,head_offset=None):
    # Paws remain at the registered ground plane; do not use tail height for scale.
    ax,ay=anchor(im,d)
    if head_offset is not None:
        h=hat(im);ax=(h[0]+h[2])/2+head_offset
    tile=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    tile.putalpha(tile.getchannel('A').point(lambda v:255 if v>=128 else 0))
    out=Image.new('RGBA',(184,184));out.alpha_composite(tile,(round(PIVOT[0]-ax*scale),round(PIVOT[1]-ay*scale)))
    return out

def main():
    motion=extract('locomotion-v1',8);sit=extract('sit-v1',6)
    corrected=extract('sit-v2',6)
    for d in ['south','north']:sit[d]=corrected[d]
    states=[];calibration={};clips={}
    def add(key,images,times,loop=True,provenance='authored'):
        files=[]
        for i,im in enumerate(images):
            rel=f'frames/{key}/{i:03}.png';p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p);files.append(rel)
        states.append(dict(id=key,frameFiles=files,frameDurationsMs=times,loop=loop,provenance=provenance));clips[key]=images
    for d in DIRS:
        h0,h1=hat(motion[d][0]),hat(sit[d][0]);ratio=(h0[2]-h0[0])/(h1[2]-h1[0]);s=SCALE*ratio
        calibration[d]={'motionScale':SCALE,'sitScale':s,'referenceBonnetWidths':[h0[2]-h0[0],h1[2]-h1[0]]}
        offset=anchor(motion[d][0],d)[0]-(h0[0]+h0[2])/2
        m=[frame(t,d,SCALE,offset) for t in motion[d]];a=[frame(t,d,s) for t in sit[d]]
        add('idle-'+d,[m[0],m[1],m[0]],[2200,130,700])
        add('walk-'+d,m[2:],[130]*6)
        # Exact idle and seated endpoints eliminate source-sheet swaps at joins.
        enter=[m[0],a[1],a[2],a[3]]
        add('sit-enter-'+d,enter,[170,200,220,190],False,'authored descent with locomotion idle endpoint')
        add('sit-'+d,[a[3],a[4],a[5],a[3]],[1600,160,650,700])
        add('sit-exit-'+d,enter[::-1],[190,220,200,170],False,'reversed authored descent')
    manifest=dict(character='margot-polish-v1',frameWidth=184,frameHeight=184,pivot=list(PIVOT),standingHeight=148,
      status='review-only',mirrored=False,states=states,calibration=calibration,
      sourceHashes={name:hashlib.sha256((ROOT/'sources'/name).read_bytes()).hexdigest() for name in ['locomotion-v1.png','sit-v1.png','sit-v2.png']})
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    # Freeze baseline used for the A/B comparison; leave active assets untouched.
    old=[]
    for pack in ['margot','margot-actions']:
        base=REPO/'character/animation-expansion-v5'/pack;m=json.loads((base/'manifest.json').read_text())
        for state in m['states']:
            if state['id'] not in clips:continue
            state=dict(state);paths=[]
            for i,path in enumerate(state['frameFiles']):
                rel=f'baseline/{state["id"]}/{i:03}.png';dest=ROOT/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(base/path,dest);paths.append(rel)
            state['frameFiles']=paths;old.append(state)
    (ROOT/'baseline.json').write_text(json.dumps(dict(states=old,frameWidth=92,frameHeight=92,pivot=[46,86]),indent=2),encoding='utf-8')
    board=Image.new('RGB',(960,520),'#1d2b31');draw=ImageDraw.Draw(board)
    for r,d in enumerate(DIRS):
        draw.text((12,r*130+6),d,fill='#dbe4e2')
        for c,im in enumerate([clips['idle-'+d][0]]+clips['walk-'+d]):
            crop=im.crop((40,88,144,180));large=crop.resize((104,92),Image.Resampling.NEAREST)
            board.paste(large,(c*132+24,r*130+28),large)
    board.save(ROOT/'review/motion-contact.png')
    print(f'Built {len(states)} clips, {sum(len(s["frameFiles"]) for s in states)} frame references; baseline preserved.')

if __name__=='__main__':main()
