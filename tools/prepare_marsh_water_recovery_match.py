"""Package matched underwater shutdown and retained recovery sprites."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-water-recovery-match-v1'
def main():
    contract=json.loads((BASE/'contract.json').read_text());palette=palette_module();records=[]
    for direction in ('south','north','east','west'):
        path=BASE/f'sources/{direction}-sheet-01.png';source=Image.open(path).convert('RGBA');cells=[]
        labels,_=label(np.asarray(source.getchannel('A'))>80);counts=np.bincount(labels.ravel());counts[0]=0;components=[]
        for component in np.flatnonzero(counts>1000):
            y,x=np.where(labels==component);box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));components.append((box,component))
        assert len(components)==18,(direction,len(components))
        components.sort(key=lambda r:(int(((r[0][1]+r[0][3])/2)/source.height*3),(r[0][0]+r[0][2])/2))
        for box,component in components:
            data=np.asarray(source.crop(box)).copy();data[labels[box[1]:box[3],box[0]:box[2]]!=component]=0;tile=Image.fromarray(data,'RGBA');cells.append((tile,(0,0,tile.width,tile.height),box))
        idle=Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{direction}/000.png').convert('RGBA');ib=idle.getbbox();scale=(ib[3]-ib[1])/(cells[16][1][3]-cells[16][1][1])
        tread=Image.open(ROOT/f'character/marsh-v2/frames/bare/tread-{direction}/000.png').convert('RGBA');swim=Image.open(ROOT/f'character/marsh-v2/frames/bare/swim-{direction}/000.png').convert('RGBA')
        tb=tread.getbbox();sb=swim.getbbox()
        for action,indices in [('death-water',range(5)),('swim-distress',range(6,12)),('recover-air',range(12,16))]:
            info=contract['states'][action+'-'+direction];frames=[tread.copy()] if action=='death-water' else [idle.copy()] if action=='recover-air' else [];review=BASE/f'review/{action}-{direction}';review.mkdir(parents=True,exist_ok=True)
            for slot,cell in enumerate(indices):
                tile,bodybox,sourcebox=cells[cell]
                if action=='recover-air':position=(round((ib[0]+ib[2])/2-(bodybox[0]+bodybox[2])/2*scale),round(ib[3]-bodybox[3]*scale))
                else:
                    t=(slot+1)/5 if action=='death-water' else 0
                    cx=(tb[0]+tb[2])/2*(1-t)+(sb[0]+sb[2])/2*t;cy=(tb[1]+tb[3])/2*(1-t)+(sb[1]+sb[3])/2*t
                    height=(bodybox[3]-bodybox[1])*scale;cy=min(cy,170-height/2)
                    position=(round(cx-(bodybox[0]+bodybox[2])/2*scale),round(cy-(bodybox[1]+bodybox[3])/2*scale))
                image=Image.new('RGBA',tuple(info['canvas']));image.alpha_composite(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS),position)
                data=np.asarray(image).copy();data[:,:,3]=np.where(data[:,:,3]>=80,255,0).astype('uint8');image=Image.fromarray(data,'RGBA');bounds=image.getbbox();assert min(bounds[0],bounds[1],image.width-bounds[2],image.height-bounds[3])>=2,(direction,action,slot,bounds)
                raw=review/f'{slot:03}-unmapped.png';mapped=review/f'{slot:03}.png';image.save(raw)
                if mapped.exists():mapped.unlink()
                palette.map_file('marsh',raw,mapped);frames.append(Image.open(mapped).convert('RGBA'));records.append({'state':action+'-'+direction,'pose':len(frames)-1,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'cell':sourcebox,'bodyBounds':bodybox,'scale':scale,'position':position,'bounds':bounds})
            if action=='recover-air':frames.append(idle.copy())
            folder=BASE/f'frames/{action}-{direction}';folder.mkdir(parents=True,exist_ok=True);board=Image.new('RGB',(1104,232),'#17212a');draw=ImageDraw.Draw(board);gif=[]
            for i,image in enumerate(frames):
                image.save(folder/f'{i:03}.png');board.paste(image,(184*i,24),image);draw.text((184*i+4,4),str(i),fill='white');bg=Image.new('RGB',(240,244),'#17212a');bg.paste(image,(28,24),image);gif.append(bg)
            board.save(review/'contact.png');gif[0].save(review/'motion.gif',save_all=True,append_images=gif[1:],duration=info['metadata']['frameDurationsMs'],loop=0)
    (BASE/'registration.json').write_text(json.dumps({'poses':records,'notes':'Water shutdown starts at selected tread. Fixed anatomical scale, projected body centers interpolate toward selected swim. Retained distress/recovery are compatibility poses; no air requirement added.'},indent=2)+'\n');print('Packaged 72 frames from 60 authored poses')
if __name__=='__main__':main()
