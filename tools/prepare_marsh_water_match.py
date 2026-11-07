"""Register swim/tread/launch poses at fixed scale and share exact endpoints."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-water-match-v1'
DIRECTIONS=('south','north','east','west')
def make(direction,palette,contract):
    path=BASE/'sources'/f'{direction}-sheet-01.png';source=Image.open(path).convert('RGBA');labels,_=label(np.asarray(source.getchannel('A'))>80);counts=np.bincount(labels.ravel())
    components=[i for i in range(1,len(counts)) if counts[i]>1000];assert len(components)==12,(direction,[(i,int(counts[i])) for i in components])
    items=[]
    for i in components:
        y,x=np.where(labels==i);items.append((i,(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))))
    items.sort(key=lambda p:(p[1][1]//(source.height//2),p[1][0]))
    idle=Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{direction}/000.png').convert('RGBA');height=idle.getbbox()[3]-idle.getbbox()[1];scale=height/(items[11][1][3]-items[11][1][1])
    keys=[('swim',i) for i in range(4)]+[('tread',i) for i in range(4)]+[('swim-start',i) for i in (1,2,3)]
    review=BASE/'review'/direction;review.mkdir(parents=True,exist_ok=True);poses=[];records=[]
    for i,(action,slot) in enumerate(keys):
        state=action+'-'+direction;info=contract['states'][state];runtime=(ROOT/info['files'][slot]).resolve();saved=BASE/'installation-backup'/runtime.relative_to(ROOT);old=Image.open(saved if saved.exists() else runtime).convert('RGBA');target=old.getbbox();canvas=tuple(info['canvas']);component,box=items[i];x0,y0,x1,y1=box
        data=np.asarray(source.crop(box)).copy();data[labels[y0:y1,x0:x1]!=component]=0;sprite=Image.fromarray(data,'RGBA');size=(round(sprite.width*scale),round(sprite.height*scale));position=(round((target[0]+target[2]-size[0])/2),target[3]-size[1])
        image=Image.new('RGBA',canvas);image.alpha_composite(sprite.resize(size,Image.Resampling.LANCZOS),position);data=np.asarray(image).copy();data[:,:,3]=np.where(data[:,:,3]>=80,255,0).astype(np.uint8);image=Image.fromarray(data,'RGBA');b=image.getbbox();assert min(b[0],b[1],canvas[0]-b[2],canvas[1]-b[3])>=2,(direction,i,b)
        unmapped=review/f'pose-{i:03}-unmapped.png';mapped=review/f'pose-{i:03}.png';image.save(unmapped)
        if mapped.exists():mapped.unlink()
        palette.map_file('marsh',unmapped,mapped);poses.append(Image.open(mapped).convert('RGBA'));records.append({'pose':i,'sourceBox':box,'scale':scale,'position':position,'inheritedBounds':target,'bounds':b})
    canvas=tuple(contract['states']['swim-start-'+direction]['canvas'])
    def pad(image):
        out=Image.new('RGBA',canvas);out.alpha_composite(image);return out
    start=[pad(poses[4]),*poses[8:11],pad(poses[0])]
    rows={'swim-'+direction:poses[:4],'tread-'+direction:poses[4:8],'swim-start-'+direction:start,'swim-stop-'+direction:list(reversed(start))}
    board=Image.new('RGB',(920,228*4),'#17212a');draw=ImageDraw.Draw(board)
    for r,(state,frames) in enumerate(rows.items()):
        folder=BASE/'frames'/state;folder.mkdir(parents=True,exist_ok=True)
        for i,image in enumerate(frames):image.save(folder/f'{i:03}.png');board.paste(image,(184*i,r*228+20),image);draw.text((184*i+3,r*228+3),state+' '+str(i),fill='white')
    board.save(review/'contact.png');images=[];durations=[]
    for a,repeats in [('tread',2),('swim-start',1),('swim',3),('swim-stop',1)]:
        state=a+'-'+direction
        for _ in range(repeats):
            for im,ms in zip(rows[state],contract['states'][state]['metadata']['frameDurationsMs']):
                bg=Image.new('RGB',(240,244),'#17212a');bg.paste(im,(28,20),im);images.append(bg);durations.append(ms)
    images[0].save(review/'chain.gif',save_all=True,append_images=images[1:],duration=durations,loop=0)
    return {'direction':direction,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'fixedScale':scale,'standingReferencePose':11,'poses':records,'registration':'Inherited projected pose center/lower extent, constant scale measured from standing source; no per-pose stretching','derivation':{'swim':[0,1,2,3],'tread':[4,5,6,7],'swim-start':[4,8,9,10,0],'swim-stop':[0,10,9,8,4]}}
def main():
    contract=json.loads((BASE/'contract.json').read_text());palette=palette_module();records=[make(d,palette,contract) for d in DIRECTIONS]
    for state,info in contract['states'].items():
        if not state.startswith('swim-turn-'):continue
        origin,destination=state.removeprefix('swim-turn-').split('-')
        folder=BASE/'frames'/state;folder.mkdir(parents=True,exist_ok=True)
        for index,direction in [(0,origin),(len(info['files'])-1,destination)]:
            image=Image.open(BASE/f'frames/swim-{direction}/000.png').convert('RGBA');out=Image.new('RGBA',tuple(info['canvas']));out.alpha_composite(image);out.save(folder/f'{index:03}.png')
    (BASE/'registration.json').write_text(json.dumps(records,indent=2)+'\n');print('Packaged 72 loop/launch/stop frames and 24 shared turn endpoints; turn interiors remain historical')
if __name__=='__main__':main()
