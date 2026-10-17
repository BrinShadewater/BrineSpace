"""Register authored rescue containers and composite existing robot reboot artwork.

No repainting: source alpha, fixed chassis anchors, downsampling, existing poses.
"""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
ROBOTS=ROOT.parent/'robot-polish-v1'
PIVOT=(160,280)
# Interior apertures in registered export coordinates. These masks describe the
# authored door/lid occlusion; robot pixels themselves are never repainted.
APERTURES={
    'josh':[[],[(157,127),(162,127),(162,259),(157,259)],[(148,126),(173,126),(173,264),(148,264)],
            [(106,127),(215,127),(215,260),(106,260)],[(106,127),(215,127),(215,265),(106,265)],
            [(105,127),(216,127),(216,275),(105,275)],[(103,126),(217,126),(217,282),(103,282)],None],
    'river':[[],[(108,194),(211,194),(211,202),(108,202)],[(111,187),(208,187),(208,200),(111,200)],
             [(112,181),(207,181),(207,199),(112,199)],[(114,175),(206,175),(207,240),(113,240)],
             [(113,172),(207,172),(207,255),(113,255)],[(111,171),(209,171),(209,264),(111,264)],None]
}

def main():
    records={}
    board=Image.new('RGB',(2560,880),'#202b33')
    for row,who in enumerate(['river','josh']):
        source=Image.open(ROOT/'sources'/f'{who}-opening-v2.png').convert('RGBA')
        # Stationary caster/chassis contacts, not the moving door/ramp bounds.
        anchors=[(x,y) for y in ([374,814] if who=='river' else [376,820]) for x in [222,664,1108,1552]]
        scale=148/310 if who=='river' else 188/310
        frames=[]
        for col,(ax,ay) in enumerate(anchors):
            c,r=col%4,col//4
            box=(round(c*source.width/4),round(r*source.height/2),round((c+1)*source.width/4),round((r+1)*source.height/2))
            tile=source.crop(box)
            a=np.array(tile);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
            tile=Image.fromarray(a)
            tile=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS)
            tile.putalpha(tile.getchannel('A').point(lambda v:255 if v>=128 else 0))
            im=Image.new('RGBA',(320,440))
            im.alpha_composite(tile,(round(160-(ax-box[0])*scale),round(280-(ay-box[1])*scale)))
            frames.append(im)
        manifest=json.loads((ROBOTS/who/'manifest.json').read_text())
        states={s['id']:s for s in manifest['states']}
        key='powerdown-exit-south' if who=='josh' else 'boot-south'
        robotfiles=states[key]['frameFiles']
        occupied=[]
        for f in robotfiles:
            im=frames[-1].copy()
            robot=Image.open(ROBOTS/f).convert('RGBA')
            foot=278 if who=='josh' else 262
            im.alpha_composite(robot,(160-92,foot-172))
            occupied.append(im)
        inside=Image.new('RGBA',(320,440))
        inside.alpha_composite(Image.open(ROBOTS/robotfiles[0]).convert('RGBA'),(68,(278 if who=='josh' else 262)-172))
        revealed=[];visible=[]
        for i,base in enumerate(frames):
            layer=inside.copy();polygon=APERTURES[who][i]
            if polygon is not None:
                mask=Image.new('L',base.size)
                if polygon:ImageDraw.Draw(mask).polygon(polygon,fill=255)
                layer.putalpha(Image.fromarray(np.minimum(np.array(layer.getchannel('A')),np.array(mask))))
            im=base.copy();im.alpha_composite(layer);revealed.append(im)
            visible.append(int(np.count_nonzero(np.array(layer.getchannel('A')))))
            board.paste(im,(i*320,row*440),im)
        assert visible[0]==0 and all(v>0 for v in visible[2:]),(who,visible)
        assert revealed[-1].tobytes()==occupied[0].tobytes(),who
        # Closed, unlatch, half-open, full-open; reboot; empty recovered container.
        exported=[]
        for group,images in [('opening-occupied',revealed),('reboot',occupied)]:
            for i,im in enumerate(images):
                p=ROOT/who/f'{group}-{i:02}.png';p.parent.mkdir(exist_ok=True)
                im.save(p);exported.append(str(p.relative_to(ROOT)).replace('\\','/'))
        empty=ROOT/who/'empty-open.png';frames[-1].save(empty)
        records[who]={'opening':exported[:8],'reboot':exported[8:],'empty':f'{who}/empty-open.png','revealedPixels':visible,'apertures':APERTURES[who],'scale':scale,'anchors':anchors,'openingDurationsMs':[100,110,110,120,130,150,180,300]}
    (ROOT/'manifest.json').write_text(json.dumps({'canvas':[320,440],'pivot':PIVOT,'standingHeight':148,'durationSeconds':8,'containers':records},indent=2))
    board.save(ROOT/'review/contact.png')
    report={'sourceSha256':{who:hashlib.sha256((ROOT/'sources'/f'{who}-opening-v2.png').read_bytes()).hexdigest() for who in records},'frameCount':sum(len(v['opening'])+len(v['reboot']) for v in records.values()),'pixelDensity':148/(384*.17)}
    for p in ROOT.glob('*/*.png'):
        if p.parent.name not in records:continue
        im=Image.open(p);a=np.array(im)[:,:,3];assert set(np.unique(a))<={0,255}
        b=im.getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<320 and b[3]<440,(p,b)
    (ROOT/'review/build.json').write_text(json.dumps(report,indent=2));print(report)

if __name__=='__main__':main()
