"""Match furniture poses at fixed scale, retaining inherited contact registration."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from prepare_marsh_welding_match import parts
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-furniture-match-v1'
def main():
    contract=json.loads((BASE/'contract.json').read_text());palette=palette_module();registrations={}
    for kind,v in contract.items():
        sourcepath=BASE/'sources'/f'{kind}-sheet-01.png';source=Image.open(sourcepath).convert('RGBA');items,labels=parts(source)
        items.sort(key=lambda p:(p[1][1]//(source.height//2),p[1][0]));assert len(items)==(8 if kind=='bunk' else 6),(kind,len(items))
        first=items[0][1];oldbox=v['poses'][0]['bounds'];scale=(oldbox[3]-oldbox[1])/(first[3]-first[1]);rows=[];records=[]
        review=BASE/'review'/kind;review.mkdir(parents=True,exist_ok=True);folder=BASE/'frames'/kind;folder.mkdir(parents=True,exist_ok=True)
        canvas=tuple(v['canvas']);board=Image.new('RGB',(canvas[0]*v['count'],canvas[1]+20),'#17212a');draw=ImageDraw.Draw(board)
        for i,(component,box) in enumerate(items[:v['count']]):
            x0,y0,x1,y1=box;data=np.asarray(source.crop(box)).copy();data[labels[y0:y1,x0:x1]!=component]=0;sprite=Image.fromarray(data,'RGBA')
            target=v['poses'][i]['bounds'];size=(round(sprite.width*scale),round(sprite.height*scale));position=(round((target[0]+target[2]-size[0])/2),target[3]-size[1])
            image=Image.new('RGBA',canvas);image.alpha_composite(sprite.resize(size,Image.Resampling.LANCZOS),position)
            data=np.asarray(image).copy();data[:,:,3]=np.where(data[:,:,3]>=80,255,0).astype(np.uint8);image=Image.fromarray(data,'RGBA')
            b=image.getchannel('A').getbbox();assert min(b[0],b[1],canvas[0]-b[2],canvas[1]-b[3])>=2,(kind,i,b)
            unmapped=review/f'pose-{i:03}-unmapped.png';mapped=review/f'pose-{i:03}.png';image.save(unmapped)
            if mapped.exists():mapped.unlink()
            palette.map_file('marsh',unmapped,mapped);image=Image.open(mapped).convert('RGBA')
            if i==0:image=Image.open(ROOT/v['poses'][0]['path']).convert('RGBA')
            image.save(folder/f'{i:03}.png');rows.append(image);board.paste(image,(i*canvas[0],20),image);draw.text((i*canvas[0]+3,3),kind+' '+str(i),fill='white')
            records.append({'pose':i,'sourceBox':box,'scale':scale,'position':position,'inheritedBounds':target,'bounds':image.getbbox()})
        board.save(review/'contact.png')
        states=v['manifest']['states'];entry=states[0];rest=next(s for s in states if s['loop']);exit=next(s for s in states if not s['loop'] and s!=entry)
        ordered=[entry,rest,exit];frames=[];times=[]
        for state in ordered:
            for f,ms in zip(state['frameFiles'],state['frameDurationsMs']):
                image=rows[int(Path(f).stem)];bg=Image.new('RGB',canvas,'#17212a');bg.paste(image,(0,0),image);frames.append(bg);times.append(ms)
        frames[0].save(review/'chain.gif',save_all=True,append_images=frames[1:],duration=times,loop=0)
        registrations[kind]={'source':sourcepath.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'fixedScale':scale,'registration':'Inherited pose bounding-center and lower support; one anatomical scale throughout. Furniture contact requires native visual review.','poses':records,'generatedStandingOmitted':True,'extraBunkStandingOmitted':kind=='bunk'}
    (BASE/'registration.json').write_text(json.dumps(registrations,indent=2)+'\n');print('Packaged 13 unique furniture frames, including two exact idle joins')
if __name__=='__main__':main()
