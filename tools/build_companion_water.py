"""Package separate authored companion water clips without touching dry packs."""
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
import build_sprite_polish as pack
import build_companion_cleanup as clean
OUT=pack.ROOT/'character/companion-water-v1';pack.OUT=OUT
DIRS=['south','west','north','east']
html=['<!doctype html><meta charset="utf-8"><title>Companion swimming and floating</title><style>body{background:#18242a;color:#ddd;font:16px system-ui;padding:24px}img{image-rendering:pixelated}figure{display:inline-block}</style><h1>Companion swimming and floating</h1><p>Four directions; movement and stationary paddling/bobbing. Engine supplies water tint and wakes.</p>']
report={}
for identity in ['margot','river']:
    source=OUT/'sources'/f'{identity}.png';rows=clean.rows(source,4,6,gutter_fraction=.35)
    clips={};manifest={'character':identity,'states':[],'source':'../sources/'+identity+'.png'}
    for d,tiles in zip(DIRS,rows):
        scale=.14 if identity=='margot' else 44/max(t.height for t in tiles)
        frames=[]
        for tile in tiles:
            if identity=='margot':
                a=np.array(tile).astype(int);mask=(a[:,:,1]>a[:,:,0]+10)&(a[:,:,1]>a[:,:,2]+15)&(a[:,:,3]>0)
                yy,xx=np.where(mask);assert len(xx)>20
                anchor=((xx.min()+xx.max())/2,(yy.min()+yy.max())/2)
                goal={'south':(46,64),'north':(46,66),'west':(34,66),'east':(58,66)}[d]
                small=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX)
                small.putalpha(small.getchannel('A').point(lambda a:255 if a>=128 else 0))
                im=Image.new('RGBA',(92,92));im.alpha_composite(small,(round(goal[0]-anchor[0]*scale),round(goal[1]-anchor[1]*scale)))
            else:im=clean.frame(tile,scale)
            frames.append(im)
        for name,indices,ms in [('swim' if identity=='margot' else 'float',range(4),180),('swim-idle' if identity=='margot' else 'float-idle',range(4,6),450)]:
            key=name+'-'+d;clips[key]=[frames[i] for i in indices]
            manifest['states'].append({'id':key,'loop':True,'water':True,'frameDurationsMs':[ms]*len(clips[key])})
    pack.quantize(clips);pack.save_pack(identity,manifest,clips)
    envelope={}
    for d in DIRS:
        boxes=[im.getbbox() for key,frames in clips.items() if key.endswith('-'+d) for im in frames]
        if identity=='river':
            # River remains upright. His lower floating chassis occupies floor
            # space; the head projects above it just as in dry upright movement.
            # Keep the full horizontal width, with the waterline at source y=70.
            boxes=[(b[0],max(70,b[1]),b[2],b[3]) for b in boxes]
        envelope[d]=[min(b[0]-46 for b in boxes)*.8821621622,min(b[1]-86 for b in boxes)*.8821621622,max(b[2]-46 for b in boxes)*.8821621622,max(b[3]-86 for b in boxes)*.8821621622]
    (OUT/identity/'clearance.json').write_text(json.dumps({'bare':envelope,'helmet':envelope},indent=2))
    for state in manifest['states']:
        key=state['id'];frames=[]
        for im in clips[key]:
            bg=Image.new('RGBA',(92,92),'#18242a');bg.alpha_composite(im);frames.append(bg.resize((276,276),Image.Resampling.NEAREST).convert('RGB'))
        name=identity+'-'+key+'.gif';frames[0].save(OUT/name,save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=2)
        html.append(f'<figure><img src="{name}"><figcaption>{identity} {key}</figcaption></figure>')
    report[identity]={'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'registration':'Margot bonnet center (17px head-width calibration), scale .14; River 44px chassis height and base contact 86. No mirroring.','pack':pack.REPORT[identity]}
(OUT/'review.html').write_text(''.join(html));(OUT/'build-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(pack.REPORT))
