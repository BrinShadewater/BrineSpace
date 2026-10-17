"""Register eight authored poses per direction into Marsh's seated action chain."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from prepare_marsh_welding_match import parts
from prepare_marsh_maintenance_match import foot_center
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-seated-match-v1';BARE=ROOT/'character/marsh-v2/frames/bare'
DIRECTIONS=('south','north','east','west')
def make(direction,palette):
    sourcepath=BASE/'sources'/f'{direction}-sheet-01.png';source=Image.open(sourcepath).convert('RGBA');items,labels=parts(source);assert len(items)==8
    idlepath=BARE/f'idle-{direction}/000.png';idle=Image.open(idlepath).convert('RGBA');box=idle.getchannel('A').getbbox();first=items[0][1];scale=(box[3]-box[1])/(first[3]-first[1]);tx,ty=foot_center(idle)
    review=BASE/'review'/direction;review.mkdir(parents=True,exist_ok=True);poses=[];records=[]
    for i,(component,box) in enumerate(items):
        x0,y0,x1,y1=box;data=np.asarray(source.crop(box)).copy();data[labels[y0:y1,x0:x1]!=component]=0;sprite=Image.fromarray(data,'RGBA');sx,sy=foot_center(sprite)
        size=(round(sprite.width*scale),round(sprite.height*scale));position=(round(tx-sx*scale),round(ty-sy*scale))
        image=Image.new('RGBA',(184,184));image.alpha_composite(sprite.resize(size,Image.Resampling.LANCZOS),position);data=np.asarray(image).copy();data[:,:,3]=np.where(data[:,:,3]>=80,255,0).astype(np.uint8);image=Image.fromarray(data,'RGBA');bounds=image.getchannel('A').getbbox();assert min(bounds[0],bounds[1],184-bounds[2],184-bounds[3])>=2,(direction,i,bounds)
        unmapped=review/f'pose-{i:03}-unmapped.png';mapped=review/f'pose-{i:03}.png';image.save(unmapped)
        if mapped.exists():mapped.unlink()
        palette.map_file('marsh',unmapped,mapped);poses.append(Image.open(mapped).convert('RGBA'));records.append({'pose':i,'sourceBox':box,'scale':scale,'footCenter':sx,'sourceSole':sy,'targetSupport':[tx,ty],'position':position,'bounds':bounds})
    poses[0]=idle;rows={'sit-down-'+direction:poses[:4],'sit-idle-'+direction:[poses[3],poses[4]],'read-seated-'+direction:poses[5:8],'sit-rise-'+direction:list(reversed(poses[:4]))}
    contact=Image.new('RGB',(184*4,205*4),'#17212a');draw=ImageDraw.Draw(contact)
    for r,(state,row) in enumerate(rows.items()):
        folder=BASE/'frames'/state;folder.mkdir(parents=True,exist_ok=True)
        for i,image in enumerate(row):
            image.save(folder/f'{i:03}.png');contact.paste(image,(184*i,205*r+20),image);draw.text((184*i+3,205*r+3),state+' '+str(i),fill='white')
    contact.save(review/'contact.png')
    pack=json.loads((ROOT/'character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json').read_text());timing={s['id']:s for s in pack['states']}
    animation=[];durations=[]
    for action,repeats in [('sit-down',1),('sit-idle',2),('read-seated',2),('sit-rise',1)]:
        state=action+'-'+direction
        for repeat in range(repeats):
            for image,ms in zip(rows[state],timing[state]['frameDurationsMs']):
                canvas=Image.new('RGB',(240,210),'#17212a');canvas.paste(image,(28,12),image);animation.append(canvas);durations.append(ms)
    animation[0].save(review/'chain.gif',save_all=True,append_images=animation[1:],duration=durations,loop=0)
    record={'direction':direction,'source':sourcepath.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'fixedScale':scale,'poses':records,'registration':'Boot center/sole at active idle support; fixed body scale throughout sitting and reading','derivation':{'sit-down':[0,1,2,3],'sit-idle':[3,4],'read-seated':[5,6,7],'sit-rise':[3,2,1,0]}}
    (review/'registration.json').write_text(json.dumps(record,indent=2)+'\n');return record
if __name__=='__main__':
    palette=palette_module();records=[make(d,palette) for d in DIRECTIONS];(BASE/'registration.json').write_text(json.dumps(records,indent=2)+'\n');print('Packaged 52 seated frames with exact idle and seat joins')
