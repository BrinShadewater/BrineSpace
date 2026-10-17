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

def frame(im,d,scale,head_offset=None,swim=False):
    # Paws remain at the registered ground plane; do not use tail height for scale.
    ax,ay=anchor(im,d)
    if head_offset is not None:
        h=hat(im);ax=(h[0]+h[2])/2+head_offset
    if swim:
        h=hat(im);ax=(h[0]+h[2])/2;ay=h[3]+42/scale
    tile=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    tile.putalpha(tile.getchannel('A').point(lambda v:255 if v>=128 else 0))
    out=Image.new('RGBA',(184,184));out.alpha_composite(tile,(round(PIVOT[0]-ax*scale),round(PIVOT[1]-ay*scale)))
    return out

def main():
    motion=extract('locomotion-v1',8);sit=extract('sit-v1',6)
    sit['south']=extract('sit-v3',6)['south']
    sit['north']=extract('sit-north-v4',6,['north'])['north']
    groom=extract('groom-v1',6);nap=extract('nap-v1',6)
    extras=extract('extras-v1',8);swim=extract('swim-v1',6)
    pet=extract('pet-v1',6,['south'])
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
        def calibrated(name,tiles,reference=0,water=False):
            h=hat(tiles[reference]);factor=SCALE*(h0[2]-h0[0])/(h[2]-h[0])
            calibration[d][name+'Scale']=factor
            return [frame(t,d,factor,swim=water) for t in tiles]
        def action_chain(name,entry,loop,exit,loop_ms):
            add(name+'-enter-'+d,entry,[180]*len(entry),False,'shared idle/sit endpoints plus authored action onset')
            add(name+'-'+d,loop,[loop_ms]*len(loop))
            add(name+'-exit-'+d,exit,[180]*len(exit),False,'authored recovery and reversed sit descent')
        g=calibrated('groom',groom[d]);n=calibrated('nap',nap[d]);e=calibrated('extras',extras[d]);w=calibrated('swim',swim[d],water=True)
        # Use exact accepted sitting pixels before/after each seated action.
        action_chain('groom',enter+[g[1]],[g[1],g[2],g[3],g[4],g[3],g[2],g[1]],
                     [g[1],a[3]]+enter[-2::-1],220)
        action_chain('nap',enter+[n[1],n[2],n[3]],[n[3],n[4],n[5],n[4],n[3]],
                     [n[3],n[2],n[1],a[3]]+enter[-2::-1],850)
        add('stretch-'+d,[m[0],e[1],e[2],e[2],e[3],m[0]],[180,240,420,420,300,200],False,'authored stretch with shared idle endpoints')
        action_chain('yawn',enter+[e[5]],[e[5],e[6],e[6],e[7],a[3]],
                     [a[3]]+enter[-2::-1],260)
        add('swim-'+d,w[:4],[180]*4)
        add('swim-idle-'+d,w[4:],[350,350])
        for state in states:
            if state['id'].startswith('swim-') and state['id'].endswith('-'+d):
                state.update(water=True,surfaceLine=148)
        if d=='south':
            p=calibrated('pet',pet[d])
            action_chain('pet',enter+[p[1]],[p[1],p[2],p[3],p[4],p[3],p[2],p[1]],
                         [p[1],a[3]]+enter[-2::-1],400)
    manifest=dict(character='margot-polish-v1',frameWidth=184,frameHeight=184,pivot=list(PIVOT),standingHeight=148,
      status='installed-source',mirrored=False,states=states,calibration=calibration,
      sourceHashes={name:hashlib.sha256((ROOT/'sources'/name).read_bytes()).hexdigest() for name in ['locomotion-v1.png','sit-v1.png','sit-v3.png','sit-north-v4.png','groom-v1.png','nap-v1.png','extras-v1.png','pet-v1.png','swim-v1.png']})
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    for kind in ['locomotion','actions','water']:
        selected=[s for s in states if (s['id'].startswith('swim-') if kind=='water' else s['id'].startswith(('idle-','walk-')) if kind=='locomotion' else not s['id'].startswith(('idle-','walk-','swim-')))]
        pack={k:v for k,v in manifest.items() if k!='states'}
        pack['strideDistanceCells']={'walk':.07}
        pack['states']=[dict(s,frameFiles=['../../'+p for p in s['frameFiles']]) for s in selected]
        dest=ROOT/'packs'/kind;dest.mkdir(parents=True,exist_ok=True)
        (dest/'manifest.json').write_text(json.dumps(pack,indent=2),encoding='utf-8')
    bounds={}
    for d in DIRS:
        boxes=[im.getbbox() for key,images in clips.items() if key.startswith('swim-') and key.endswith('-'+d) for im in images]
        bounds[d]=[(min(b[0] for b in boxes)-92)*65.28/148,(min(b[1] for b in boxes)-172)*65.28/148,
                   (max(b[2] for b in boxes)-92)*65.28/148,(max(b[3] for b in boxes)-172)*65.28/148]
    (ROOT/'clearance.json').write_text(json.dumps({'bare':bounds,'helmet':bounds},indent=2),encoding='utf-8')
    # Freeze baseline used for the A/B comparison; leave active assets untouched.
    old=[]
    for folder in ['animation-expansion-v5/margot','animation-expansion-v5/margot-actions','companion-water-v1/margot']:
        base=REPO/'character'/folder;m=json.loads((base/'manifest.json').read_text())
        for state in m['states']:
            if state['id'] not in clips:continue
            state=dict(state);paths=[]
            for i,path in enumerate(state['frameFiles']):
                rel=f'baseline/{state["id"]}/{i:03}.png';dest=ROOT/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(base/path,dest);paths.append(rel)
            state['frameFiles']=paths;state['sourcePack']=folder;old.append(state)
    (ROOT/'baseline.json').write_text(json.dumps(dict(states=old,frameWidth=92,frameHeight=92,pivot=[46,86]),indent=2),encoding='utf-8')
    board=Image.new('RGB',(960,520),'#1d2b31');draw=ImageDraw.Draw(board)
    for r,d in enumerate(DIRS):
        draw.text((12,r*130+6),d,fill='#dbe4e2')
        for c,im in enumerate([clips['idle-'+d][0]]+clips['walk-'+d]):
            crop=im.crop((40,88,144,180));large=crop.resize((104,92),Image.Resampling.NEAREST)
            board.paste(large,(c*132+24,r*130+28),large)
    board.save(ROOT/'review/motion-contact.png')
    board=Image.new('RGB',(1100,560),'#1d2b31');draw=ImageDraw.Draw(board)
    for j,d in enumerate(DIRS):
        draw.text((8,j*140+8),d,fill='white')
        for i,key in enumerate(['sit','groom','nap','stretch','yawn','swim']):
            row=clips[key+'-'+d];im=row[min(2,len(row)-1)].crop((30,85,154,182))
            board.paste(im,(70+i*168,j*140+27),im);draw.text((70+i*168,j*140+10),key,fill='#c7d6d9')
    board.save(ROOT/'review/all-actions-contact.png')
    print(f'Built {len(states)} clips, {sum(len(s["frameFiles"]) for s in states)} frame references; baseline preserved.')

if __name__=='__main__':main()
