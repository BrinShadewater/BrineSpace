"""Package personality actions, preserving all accepted locomotion and portrait files."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]/'character/companion-personality-v1'

def tiles(identity, cols):
    source=Image.open(ROOT/'sources'/f'{identity}.png').convert('RGBA')
    result=[]
    rgb=np.array(source)[:,:,:3].astype(int)
    ink=~((rgb[:,:,0]>rgb[:,:,1]+65)&(rgb[:,:,2]>rgb[:,:,1]+65))
    row_edges=[0]
    for row in range(1,4):
        start=round(row*source.height/4)-65
        counts=ink.sum(axis=1)[start:start+130]
        row_edges.append(start+int(np.median(np.where(counts==counts.min())[0])))
    row_edges.append(source.height)
    for row in range(4):
        strip=source.crop((0,row_edges[row],source.width,row_edges[row+1]))
        rgb=np.array(strip)[:,:,:3].astype(int)
        ink=~((rgb[:,:,0]>rgb[:,:,1]+65)&(rgb[:,:,2]>rgb[:,:,1]+65))
        edges=[0]
        for col in range(1,cols):
            start=round(col*source.width/cols)-40
            counts=ink.sum(axis=0)[start:start+80]
            edges.append(start+int(np.median(np.where(counts==counts.min())[0])))
        edges.append(source.width)
        cells=[]
        for col in range(cols):
            tile=strip.crop((edges[col],0,edges[col+1],strip.height))
            pixels=np.array(tile);rgb=pixels[:,:,:3].astype(int)
            pixels[(rgb[:,:,0]>rgb[:,:,1]+65)&(rgb[:,:,2]>rgb[:,:,1]+65),3]=0
            tile=Image.fromarray(pixels);box=tile.getbbox()
            assert box and box[0]>0 and box[1]>0 and box[2]<tile.width and box[3]<tile.height,(identity,row,col,box)
            cells.append(tile.crop(box))
        result.append(cells)
    return result

for identity in ['margot','river','josh']:
    pack=ROOT/identity;pack.mkdir(exist_ok=True)
    rows=tiles(identity,4 if identity=='margot' else 8)
    # One scale per character; crouches remain lower instead of being stretched.
    scale={'margot':34,'river':44,'josh':70}[identity]/rows[0][0].height
    states=[];previews=[]
    def clip(key, sources, duration=300, loop=True):
        files=[];frames=[]
        for index, source in enumerate(sources):
            tile=source.resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.NEAREST)
            assert tile.width<=92 and tile.height<=86,(identity,key,tile.size)
            canvas=Image.new('RGBA',(92,92));canvas.alpha_composite(tile,((92-tile.width)//2,86-tile.height))
            path=pack/'frames'/key/f'{index:03}.png';path.parent.mkdir(parents=True,exist_ok=True);canvas.save(path)
            files.append(path.relative_to(pack).as_posix());frames.append(canvas)
        states.append(dict(id=key,frameFiles=files,frameDurationsMs=[duration]*len(files),loop=loop))
        if '-enter-' not in key and '-exit-' not in key:previews.append((key,frames,duration))
    if identity=='margot':
        for action,row in [('sit',0),('groom',1),('nap',2),('pet',3)]:
            enter=rows[0][:2]+rows[2][:2] if action=='nap' else rows[0][:2]
            clip(action+'-enter-south',enter,200,False)
            clip(action+'-south',rows[row][2:] if action in ['sit','nap'] else rows[row],650 if action in ['sit','nap'] else 350)
            clip(action+'-exit-south',list(reversed(enter)),200,False)
    else:
        actions=['scan','inspect'] if identity=='river' else ['watch','turn']
        for row,direction in enumerate(['south','west','north','east']):
            for i,action in enumerate(actions):
                cells=rows[row][i*4:i*4+4]
                # North watch's third source turns the face 180 degrees; retain rear silhouette.
                if identity=='josh' and direction=='north' and action=='watch':cells=[cells[0],cells[1],cells[1],cells[3]]
                if identity=='josh' and action=='turn':cells=[cells[2],cells[0],cells[1],cells[3]]
                clip(action+'-'+direction,cells,300)
    (pack/'manifest.json').write_text(json.dumps(dict(character=identity,frameWidth=92,frameHeight=92,pivot=[46,86],states=states,mirrored=False,source='../sources/'+identity+'.png',sourceSha256=hashlib.sha256((ROOT/'sources'/f'{identity}.png').read_bytes()).hexdigest()),indent=2))
    # All action phases in a static contact sheet, plus per-action loops for review.
    contact=Image.new('RGBA',(92*4,92*len(previews)),(30,43,48,255))
    for row,(key,frames,duration) in enumerate(previews):
        loop=[]
        for col,frame in enumerate(frames):
            contact.alpha_composite(frame,(col*92,row*92))
            bg=Image.new('RGBA',(92,92),(30,43,48,255));bg.alpha_composite(frame)
            loop.append(bg.resize((276,276),Image.Resampling.NEAREST).convert('RGB'))
        loop[0].save(pack/(key+'.gif'),save_all=True,append_images=loop[1:],duration=duration,loop=0)
    contact.resize((736,184*len(previews)),Image.Resampling.NEAREST).save(pack/'contact.png')
    print(identity,len(states),'action clips')
