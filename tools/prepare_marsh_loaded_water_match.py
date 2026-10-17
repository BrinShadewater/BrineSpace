"""Package authored loaded loops and quarter-turns with exact cargo transition joins."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-loaded-water-match-v1'
PAIRS=('east-north','west-north','east-south','west-south')

def main():
    contract=json.loads((BASE/'contract.json').read_text());palette=palette_module();clips={};records=[]
    for pair in ('south','north','east','west',*PAIRS):
        turn='-' in pair;a=pair.split('-')[0];b=pair.split('-')[-1];revision='02' if pair=='west-south' else '01';path=BASE/f'sources/{pair}-sheet-{revision}.png';source=Image.open(path).convert('RGBA')
        labels,_=label(np.asarray(source.getchannel('A'))>80);counts=np.bincount(labels.ravel());items=[]
        for component in range(1,len(counts)):
            if counts[component]<1000:continue
            y,x=np.where(labels==component);items.append((component,(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))))
        assert len(items)==6,(pair,len(items));items.sort(key=lambda item:(((item[1][1]+item[1][3])/2)//(source.height//2),item[1][0]))
        idle=Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{a}/000.png');ib=idle.getbbox();scale=(ib[3]-ib[1])/(items[5][1][3]-items[5][1][1]);poses=[]
        info=contract['states'][('swim-carry-turn-' if turn else 'swim-carry-')+pair]
        for i,(component,box) in enumerate(items[:3 if turn else 4]):
            x0,y0,x1,y1=box;data=np.asarray(source.crop(box)).copy();data[labels[y0:y1,x0:x1]!=component]=0;sprite=Image.fromarray(data,'RGBA')
            size=(round(sprite.width*scale),round(sprite.height*scale));target=info['bounds'][i+1 if turn else i];pos=(round((target[0]+target[2]-size[0])/2),target[3]-size[1])
            image=Image.new('RGBA',tuple(info['canvas']));image.alpha_composite(sprite.resize(size,Image.Resampling.LANCZOS),pos);data=np.asarray(image).copy();data[:,:,3]=np.where(data[:,:,3]>=80,255,0).astype('uint8');image=Image.fromarray(data,'RGBA')
            bounds=image.getbbox();assert min(bounds[0],bounds[1],image.width-bounds[2],image.height-bounds[3])>=2,(pair,i,bounds)
            folder=BASE/f'review/{pair}';folder.mkdir(parents=True,exist_ok=True);raw=folder/f'{i:03}-unmapped.png';mapped=folder/f'{i:03}.png';image.save(raw)
            if mapped.exists():mapped.unlink()
            palette.map_file('marsh',raw,mapped);poses.append(Image.open(mapped).convert('RGBA'))
            records.append({'pair':pair,'pose':i,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sourceBox':box,'scale':scale,'position':pos,'inheritedBounds':target,'bounds':bounds})
        if not turn:
            clips['swim-carry-'+pair]=[poses[i] for i in (0,1,2,3,2,1)]
        else:
            clips['swim-carry-turn-'+pair]=poses
    for pair in PAIRS:
        a,b=pair.split('-');row=[clips['swim-carry-'+a][0],*clips['swim-carry-turn-'+pair],clips['swim-carry-'+b][0]]
        clips['swim-carry-turn-'+pair]=row;clips[f'swim-carry-turn-{b}-{a}']=list(reversed(row))
    for a,b,via in [('east','west','north'),('north','south','east')]:
        first=clips[f'swim-carry-turn-{a}-{via}'];second=clips[f'swim-carry-turn-{via}-{b}'];assert first[-1].tobytes()==second[0].tobytes()
        row=first+second[1:];clips[f'swim-carry-turn-{a}-{b}']=row;clips[f'swim-carry-turn-{b}-{a}']=list(reversed(row))
    for state,frames in clips.items():
        folder=BASE/'frames'/state;folder.mkdir(parents=True,exist_ok=True)
        for i,image in enumerate(frames):image.save(folder/f'{i:03}.png')
        review=BASE/'review'/state.removeprefix('swim-carry-turn-');review.mkdir(parents=True,exist_ok=True)
        board=Image.new('RGB',(224*len(frames),232),'#17212a');draw=ImageDraw.Draw(board);gif=[]
        for i,image in enumerate(frames):
            board.paste(image,(224*i,24),image);draw.text((224*i+4,4),str(i),fill='white');bg=Image.new('RGB',(280,244),'#17212a');bg.paste(image,(28,24),image);gif.append(bg)
        board.save(review/'contact.png');gif[0].save(review/'motion.gif',save_all=True,append_images=gif[1:],duration=contract['states'][state]['metadata']['frameDurationsMs'],loop=0)
    for direction in ('south','north','east','west'):
        endpoint=clips['swim-carry-'+direction][0]
        for state,index in [('swim-pickup-'+direction,5),('cargo-drain-'+direction,0)]:
            folder=BASE/'frames'/state;folder.mkdir(parents=True,exist_ok=True);endpoint.save(folder/f'{index:03}.png')
    (BASE/'registration.json').write_text(json.dumps({'poses':records,'derivation':'16 authored loaded loop poses and 12 quarter-turn interiors; reverse return turns; half-turns concatenate adjacent turns at the exact cardinal endpoint, retaining the inherited combined center duration'},indent=2)+'\n')
    print('Packaged 108 loaded loop/turn/boundary frames from 28 authored poses')
if __name__=='__main__':main()
