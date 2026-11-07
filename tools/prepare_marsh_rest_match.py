"""Register authored generic rest poses at one body scale; preserve exact joins."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from prepare_marsh_welding_match import parts
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-rest-match-v1';BARE=ROOT/'character/marsh-v2/frames/bare'
DIRECTIONS=('south','north','east','west')
def make(direction,palette):
    sourcepath=BASE/'sources'/f'{direction}-sheet-01.png'
    source=Image.open(sourcepath).convert('RGBA');items,labels=parts(source);assert len(items)==8,(direction,len(items))
    idle=Image.open(BARE/f'idle-{direction}/000.png').convert('RGBA')
    b=idle.getchannel('A').getbbox();first=items[0][1];scale=(b[3]-b[1])/(first[3]-first[1])
    review=BASE/'review'/direction;review.mkdir(parents=True,exist_ok=True);poses=[];records=[]
    for i,(component,box) in enumerate(items):
        x0,y0,x1,y1=box;data=np.asarray(source.crop(box)).copy();data[labels[y0:y1,x0:x1]!=component]=0
        sprite=Image.fromarray(data,'RGBA');size=(round(sprite.width*scale),round(sprite.height*scale))
        position=(92-size[0]//2,172-size[1])
        image=Image.new('RGBA',(184,184));image.alpha_composite(sprite.resize(size,Image.Resampling.LANCZOS),position)
        data=np.asarray(image).copy();data[:,:,3]=np.where(data[:,:,3]>=80,255,0).astype(np.uint8);image=Image.fromarray(data,'RGBA')
        bounds=image.getchannel('A').getbbox();assert min(bounds[0],bounds[1],184-bounds[2],184-bounds[3])>=2,(direction,i,bounds)
        unmapped=review/f'pose-{i:03}-unmapped.png';mapped=review/f'pose-{i:03}.png';image.save(unmapped)
        if mapped.exists():mapped.unlink()
        palette.map_file('marsh',unmapped,mapped);poses.append(Image.open(mapped).convert('RGBA'))
        records.append({'pose':i,'sourceBox':box,'scale':scale,'position':position,'bounds':bounds})
    poses[0]=idle
    rows={'lie-down-'+direction:poses[:4],'sleep-'+direction:[poses[3],poses[4]],'get-up-'+direction:[poses[3],poses[2],poses[1],idle]}
    board=Image.new('RGB',(736,630),'#17212a');draw=ImageDraw.Draw(board)
    for r,(state,row) in enumerate(rows.items()):
        folder=BASE/'frames'/state;folder.mkdir(parents=True,exist_ok=True)
        for i,image in enumerate(row):
            image.save(folder/f'{i:03}.png');board.paste(image,(184*i,210*r+20),image);draw.text((184*i+3,210*r+3),state+' '+str(i),fill='white')
    board.save(review/'contact.png')
    pack=json.loads((ROOT/'character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json').read_text());timing={s['id']:s for s in pack['states']}
    animation=[];durations=[]
    for action in ('lie-down','sleep','sleep','get-up'):
        state=action+'-'+direction
        for image,ms in zip(rows[state],timing[state]['frameDurationsMs']):
            canvas=Image.new('RGB',(240,210),'#17212a');canvas.paste(image,(28,12),image);animation.append(canvas);durations.append(ms)
    animation[0].save(review/'chain.gif',save_all=True,append_images=animation[1:],duration=durations,loop=0)
    record={'direction':direction,'source':sourcepath.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'fixedScale':scale,'poses':records,'registration':'Bounding center at x92, implied supporting surface at y172, one fixed anatomical scale','derivation':{'lie-down':[0,1,2,3],'sleep':[3,4],'get-up':[3,2,1,0]},'omittedSourcePoses':[5,6,7],'omissionReason':'Rise reverses selected descent to preserve resting orientation; exact runtime idle replaces generated standing poses'}
    (review/'registration.json').write_text(json.dumps(record,indent=2)+'\n');return record
if __name__=='__main__':
    palette=palette_module();records=[make(d,palette) for d in DIRECTIONS];(BASE/'registration.json').write_text(json.dumps(records,indent=2)+'\n');print('Packaged 40 generic rest frames with exact idle and rest joins')
