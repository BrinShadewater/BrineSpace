"""Package Marsh welding with fixed body scale and explicit planted supports."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
from prepare_marsh_carry_chain import palette_module
from prepare_marsh_maintenance_match import foot_center
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-welding-match-v1'
BARE=ROOT/'character/marsh-v2/frames/bare'
DIRECTIONS=('south','north','east','west')
def parts(source):
    labels,_=label(np.asarray(source.getchannel('A'))>80)
    counts=np.bincount(labels.ravel());result=[]
    for component in range(1,len(counts)):
        if counts[component]<10000:continue
        y,x=np.where(labels==component)
        result.append((component,(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))))
    multirow=len(result)>6
    result.sort(key=lambda p:(p[1][1]//(source.height//2) if multirow else 0,p[1][0]))
    return result,labels
def sole_center(source,box,y):
    # Last occupied segment on this measured support band is the planted right boot.
    a=np.asarray(source.getchannel('A'))[y-3:y,box[0]:box[2]]>80
    occupied=a.any(axis=0);edges=np.flatnonzero(np.diff(np.pad(occupied.astype(int),(1,1))))
    spans=[(int(x),int(z)) for x,z in zip(edges[::2],edges[1::2]) if z-x>=3]
    x,z=spans[-1];return box[0]+(x+z)/2

def make(direction,palette):
    revision='02' if direction=='west' else '01'
    path=BASE/'sources'/f'{direction}-sheet-{revision}.png';source=Image.open(path).convert('RGBA')
    items,labels=parts(source);assert len(items)==(12 if direction=='south' else 6),len(items)
    idlepath=BARE/f'idle-{direction}/000.png';idle=Image.open(idlepath).convert('RGBA')
    bounds=idle.getchannel('A').getbbox();first=items[0][1]
    scale=(bounds[3]-bounds[1])/(first[3]-first[1]);idle_x,idle_bottom=foot_center(idle)
    poses=[];records=[]
    source_support=[375,375,377,376,375,351,649,651,651,651,650,650]
    target_support=[172,172,172,171,171,169,169,169,169,169,169,169]
    review=BASE/'review'/direction;review.mkdir(parents=True,exist_ok=True)
    for i,(component,box) in enumerate(items):
        x0,y0,x1,y1=box;data=np.asarray(source.crop(box)).copy();data[labels[y0:y1,x0:x1]!=component]=0
        sprite=Image.fromarray(data,'RGBA');size=(round(sprite.width*scale),round(sprite.height*scale))
        if direction=='south' and i>0:
            sx=sole_center(source,box,source_support[i]);sy=source_support[i]
            # Registration uses the inherited planted boot, not the torch or bbox.
            tx=115.0;ty=target_support[i]
        else:
            sx=(x0+x1)/2;sy=y1
            if direction!='south':
                local_x,local_bottom=foot_center(sprite);sx=x0+local_x;sy=y0+local_bottom
            tx=idle_x;ty=idle_bottom
        position=(round(tx-(sx-x0)*scale),round(ty-(sy-y0)*scale))
        image=Image.new('RGBA',(184,237));image.alpha_composite(sprite.resize(size,Image.Resampling.LANCZOS),position)
        data=np.asarray(image).copy();data[:,:,3]=np.where(data[:,:,3]>=80,255,0).astype(np.uint8);image=Image.fromarray(data,'RGBA')
        b=image.getchannel('A').getbbox();assert min(b[0],b[1],184-b[2],237-b[3])>=2,(direction,i,b)
        unmapped=review/f'pose-{i:03}-unmapped.png';mapped=review/f'pose-{i:03}.png';image.save(unmapped)
        if mapped.exists():mapped.unlink()
        palette.map_file('marsh',unmapped,mapped);image=Image.open(mapped).convert('RGBA')
        poses.append(image);records.append({'pose':i,'sourceBox':box,'scale':scale,'sourceSupport':[sx,sy],'targetSupport':[tx,ty],'position':position,'bounds':b})
    standing=Image.new('RGBA',(184,237));standing.alpha_composite(idle,(0,0));poses[0]=standing
    if direction=='south':
        draw=poses[:6];work=[draw[-1],*poses[7:11],draw[-1]]
    else:
        draw=[poses[i] for i in [0,0,1,1,2,2]];work=[poses[i] for i in [2,2,3,3,4,2]]
    rows={'torch-draw-'+direction:draw,'weld-'+direction:work,'torch-stow-'+direction:list(reversed(draw))}
    board=Image.new('RGB',(184*6,267*3),'#17212a');labeler=ImageDraw.Draw(board)
    for row,(state,frames) in enumerate(rows.items()):
        folder=BASE/'frames'/state;folder.mkdir(parents=True,exist_ok=True)
        for i,image in enumerate(frames):
            image.save(folder/f'{i:03}.png');board.paste(image,(184*i,row*267+20),image);labeler.text((184*i+4,row*267+4),state+' '+str(i),fill='white')
    board.save(review/'contact.png')
    frames=[]
    for sample in range(140):
        t=sample*.05;state='torch-draw' if t<.9 else 'weld' if t<6.1 else 'torch-stow';elapsed=t if t<.9 else t-.9 if t<6.1 else t-6.1
        i=min(5,int((elapsed%.9 if state=='weld' else elapsed)/.15))
        image=rows[state+'-'+direction][i];canvas=Image.new('RGB',(240,265),'#17212a');canvas.paste(image,(28,10),image);frames.append(canvas)
    frames[0].save(review/'chain.gif',save_all=True,append_images=frames[1:],duration=50,loop=0)
    record={'direction':direction,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'fixedScale':scale,'poses':records,'registration':'Standing scale locked across every pose; south planted-right-boot support bands calibrated independently of tool tip','sharedEndpoints':'Exact idle; draw end equals work first/last and stow first; stow reverses draw'}
    (review/'registration.json').write_text(json.dumps(record,indent=2)+'\n');return record
if __name__=='__main__':
    palette=palette_module();records=[make(d,palette) for d in DIRECTIONS]
    (BASE/'registration.json').write_text(json.dumps(records,indent=2)+'\n');print('Packaged 72 welding frames; exact idle and shared joins; fixed body scale')
