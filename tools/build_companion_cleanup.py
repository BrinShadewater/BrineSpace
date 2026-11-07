"""Repair source extraction without painting or inventing animation frames."""
from pathlib import Path
from collections import deque
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
import build_sprite_polish as pack

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/companion-cleanup-v3'
pack.OUT=OUT

def clean(image,white=False):
    a=np.array(image.convert('RGBA'));rgb=a[:,:,:3].astype(int)
    if white:
        # Only neutral background reachable from tile edges. Internal ivory
        # highlights are subject pixels, not an arbitrary white color key.
        candidate=(rgb.min(axis=2)>205)&(rgb.max(axis=2)-rgb.min(axis=2)<18)
        h,w=candidate.shape;mask=np.zeros((h,w),bool)
        q=deque([(y,x) for y in range(h) for x in [0,w-1]]+[(y,x) for x in range(w) for y in [0,h-1]])
        while q:
            y,x=q.popleft()
            if y<0 or x<0 or y>=h or x>=w or mask[y,x] or not candidate[y,x]:continue
            mask[y,x]=True;q.extend([(y-1,x),(y+1,x),(y,x-1),(y,x+1)])
    else:mask=(rgb[:,:,0]>rgb[:,:,1]+55)&(rgb[:,:,2]>rgb[:,:,1]+55)
    a[mask]=0
    return Image.fromarray(a)

def rows(path,nrows,cols,white=False,gutter_fraction=.2,strict_padding=True):
    image=Image.open(path).convert('RGBA');a=np.array(image);rgb=a[:,:,:3].astype(int)
    ink=(rgb.min(axis=2)<180) if white else ~((rgb[:,:,0]>rgb[:,:,1]+55)&(rgb[:,:,2]>rgb[:,:,1]+55))
    def edges(counts,n):
        result=[0];length=len(counts)
        for i in range(1,n):
            start=round(i*length/n)-int(length/n*gutter_fraction);end=round(i*length/n)+int(length/n*gutter_fraction)
            sample=counts[start:end];result.append(start+int(np.median(np.where(sample==sample.min())[0])))
        return result+[length]
    ys=edges(ink.sum(axis=1),nrows);result=[]
    for row in range(nrows):
        xs=edges(ink[ys[row]:ys[row+1]].sum(axis=0),cols);tiles=[]
        for col in range(cols):
            tile=clean(image.crop((xs[col],ys[row],xs[col+1],ys[row+1])),white)
            box=tile.getbbox();assert box and (not strict_padding or (box[0]>0 and box[1]>0 and box[2]<tile.width and box[3]<tile.height)),(path,row,col,box)
            tiles.append(tile.crop(box))
        result.append(tiles)
    return result

def frame(tile,scale):
    tile=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX)
    tile.putalpha(tile.getchannel('A').point(lambda a:255 if a>=128 else 0))
    out=Image.new('RGBA',(92,92));out.alpha_composite(tile,((92-tile.width)//2,86-tile.height));return out

def build(identity):
    base,_=pack.read_pack(ROOT/f'character/sprite-polish-v2/{identity}/manifest.json')
    actions,_=pack.read_pack(ROOT/f'character/sprite-polish-v2/{identity}-actions/manifest.json')
    clips={};sources=[]
    sets=[('motion.png',['south','west','north','east'],True)] if identity!='margot' else [('south.png',['south'],False),('other-directions.png',['west','north','east'],False)]
    for filename,directions,white in sets:
        path=ROOT/f'character/{identity}-v1/sources/{filename}';sources.append(path)
        sheet=rows(path,len(directions),6,white)
        for d,tiles in zip(directions,sheet):
            height=44 if identity=='river' else 70 if identity=='josh' else 34 if d=='south' else 28
            scale=height/max(t.height for t in tiles)
            clips['idle-'+d]=[frame(t,scale) for t in tiles[:2]]
            clips['walk-'+d]=[frame(t,scale) for t in tiles[2:]]
    path=ROOT/f'character/companion-personality-v1/sources/{identity}.png';sources.append(path)
    sheet=rows(path,4,4 if identity=='margot' else 8)
    scale={'margot':34,'river':44,'josh':70}[identity]/sheet[0][0].height
    poses={}
    if identity=='margot':
        for action,row in [('sit',0),('groom',1),('nap',2),('pet',3)]:
            entry=sheet[0][:2]+sheet[2][:2] if action=='nap' else sheet[0][:2]
            loop=sheet[row][2:] if action in ['sit','nap'] else sheet[row]
            for key,tiles in [(action+'-enter-south',entry),(action+'-south',loop),(action+'-exit-south',list(reversed(entry)))]:poses[key]=[frame(t,scale) for t in tiles]
    else:
        for row,d in enumerate(['south','west','north','east']):
            for i,action in enumerate(['scan','inspect'] if identity=='river' else ['watch','turn']):
                tiles=sheet[row][i*4:i*4+4]
                if identity=='josh' and d=='north' and action=='watch':tiles=[tiles[0],tiles[1],tiles[1],tiles[3]]
                if identity=='josh' and action=='turn':tiles=[tiles[2],tiles[0],tiles[1],tiles[3]]
                key=action+'-'+d;poses[key]=[frame(t,scale) for t in tiles]
                poses[action+'-enter-'+d]=[clips['idle-'+d][0].copy(),poses[key][0].copy()]
                poses[action+'-exit-'+d]=[poses[key][-1].copy(),clips['idle-'+d][0].copy()]
    combined={**clips,**poses};pack.quantize(combined)
    for manifest in [base,actions]:manifest['extraction']='Border-connected neutral background removal for robots; magenta key for cat/actions; BOX downsample before binary alpha and shared palette.'
    pack.save_pack(identity,base,{k:combined[k] for k in clips})
    pack.save_pack(identity+'-actions',actions,{k:combined[k] for k in poses})
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}

def review():
    html=['<!doctype html><meta charset="utf-8"><title>Companion extraction repair</title><style>body{background:#18242a;color:#ddd;font:16px system-ui;padding:24px}img{image-rendering:pixelated;max-width:100%}</style><h1>Companion extraction repair</h1><p>Before (left) / corrected (right). Original timing; four directions. White interiors preserved, source detail area-downsampled.</p>']
    for identity in ['river','josh','margot']:
        for suffix in ['', '-actions']:
            m,new=pack.read_pack(OUT/(identity+suffix)/'manifest.json');_,old=pack.read_pack(ROOT/f'character/sprite-polish-v2/{identity+suffix}/manifest.json')
            for s in m['states']:
                if '-enter-' in s['id'] or '-exit-' in s['id']:continue
                key=s['id'];frames=[]
                for i,im in enumerate(new[key]):
                    bg=Image.new('RGBA',(184,92),(24,36,42,255));bg.alpha_composite(old[key][i],(0,0));bg.alpha_composite(im,(92,0))
                    frames.append(bg.resize((552,276),Image.Resampling.NEAREST).convert('RGB'))
                rel=f'{identity}-{key}.gif';frames[0].save(OUT/rel,save_all=True,append_images=frames[1:],duration=s['frameDurationsMs'],loop=0,disposal=2)
                frames[0].save(OUT/f'{identity}-{key}.png')
                html.append(f'<h3>{identity} / {key}</h3><img src="{rel}">')
    (OUT/'review.html').write_text(''.join(html))

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True);sources={}
    for identity in ['river','josh','margot']:sources.update(build(identity))
    review();(OUT/'build-report.json').write_text(json.dumps({'packs':pack.REPORT,'sources':sources},indent=2));print(json.dumps(pack.REPORT))
