"""Package dry android shutdown and separate white-fluid injury candidates."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-shutdown-injury-match-v1'
def main():
    contract=json.loads((BASE/'contract.json').read_text());palette=palette_module();records=[]
    for direction in ('south','north','east','west'):
        path=BASE/f'sources/{direction}-sheet-01.png';source=Image.open(path).convert('RGBA');cells=[]
        full_labels,_=label(np.asarray(source.getchannel('A'))>80);full_counts=np.bincount(full_labels.ravel());full_counts[0]=0
        bodies=[]
        for component in np.flatnonzero(full_counts>1000):
            yy,xx=np.where(full_labels==component)
            bodies.append((component,(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1))))
        for row in range(2):
            for col in range(6):
                box=(round(col*source.width/6),round(row*source.height/2),round((col+1)*source.width/6),round((row+1)*source.height/2));tile=source.crop(box)
                labels,_=label(np.asarray(tile.getchannel('A'))>80);counts=np.bincount(labels.ravel());counts[0]=0;body=counts.argmax();y,x=np.where(labels==body);assert counts[body]>1000,(direction,row,col)
                bodybox=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));data=np.asarray(tile).copy();data[~np.isin(labels,np.flatnonzero(counts>=20))]=0;cells.append((Image.fromarray(data,'RGBA'),bodybox,box))
                # A grid division can pass through a long prone forearm/boot.
                # Extend that cell to its complete connected body before scaling.
                component,complete=min(bodies,key=lambda r:abs((r[1][0]+r[1][2])/2-(box[0]+box[2])/2)+abs((r[1][1]+r[1][3])/2-(box[1]+box[3])/2)*3)
                if complete[0]<box[0] or complete[2]>box[2] or complete[1]<box[1] or complete[3]>box[3]:
                    expanded=(min(box[0],complete[0]),min(box[1],complete[1]),max(box[2],complete[2]),max(box[3],complete[3]))
                    tile=source.crop(expanded);labels=full_labels[expanded[1]:expanded[3],expanded[0]:expanded[2]];data=np.asarray(tile).copy()
                    keep=(labels==component)
                    for other in np.flatnonzero(full_counts>=20):
                        if other==component or full_counts[other]>1000:continue
                        keep|=(labels==other)
                    data[~keep]=0;bodybox=(complete[0]-expanded[0],complete[1]-expanded[1],complete[2]-expanded[0],complete[3]-expanded[1]);cells[-1]=(Image.fromarray(data,'RGBA'),bodybox,expanded)
        idle=Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{direction}/000.png').convert('RGBA');ib=idle.getbbox();scale=(ib[3]-ib[1])/(cells[5][1][3]-cells[5][1][1]);info=contract['states']['death-ground-'+direction]
        for row,action in [(0,'death-ground'),(1,'injury-ground')]:
            frames=[idle.copy()];review=BASE/f'review/{action}-{direction}';review.mkdir(parents=True,exist_ok=True)
            for i in range(5):
                tile,bodybox,sourcebox=cells[row*6+i];target=info['bounds'][i+1];position=(round((target[0]+target[2])/2-(bodybox[0]+bodybox[2])/2*scale),round(target[3]-bodybox[3]*scale));image=Image.new('RGBA',tuple(info['canvas']));image.alpha_composite(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS),position)
                selected_path=path
                if direction=='north' and i==4:
                    # Revision 02 fixes only the final anatomy; retain all other
                    # original poses and the original standing calibration.
                    selected_path=BASE/'sources/north-sheet-02.png'
                    revised=Image.open(selected_path).convert('RGBA')
                    sourcebox=(round(4*revised.width/6),round(row*revised.height/2),round(5*revised.width/6),round((row+1)*revised.height/2))
                    tile=revised.crop(sourcebox)
                    labels,_=label(np.asarray(tile.getchannel('A'))>80);counts=np.bincount(labels.ravel());counts[0]=0;body=counts.argmax();y,x=np.where(labels==body)
                    bodybox=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));data=np.asarray(tile).copy();data[~np.isin(labels,np.flatnonzero(counts>=20))]=0;tile=Image.fromarray(data,'RGBA')
                    position=(round(info['metadata'].get('pivot',[92,172])[0]-(bodybox[0]+bodybox[2])/2*scale),round(target[3]-bodybox[3]*scale))
                    image=Image.new('RGBA',tuple(info['canvas']));image.alpha_composite(tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS),position)
                data=np.asarray(image).copy();data[:,:,3]=np.where(data[:,:,3]>=80,255,0).astype('uint8');image=Image.fromarray(data,'RGBA');bounds=image.getbbox();assert min(bounds[0],bounds[1],image.width-bounds[2],image.height-bounds[3])>=2,(direction,row,i,bounds)
                raw=review/f'{i:03}-unmapped.png';mapped=review/f'{i:03}.png';image.save(raw)
                if mapped.exists():mapped.unlink()
                palette.map_file('marsh',raw,mapped);frames.append(Image.open(mapped).convert('RGBA'));records.append({'state':action+'-'+direction,'pose':i+1,'source':selected_path.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(selected_path.read_bytes()).hexdigest(),'cell':sourcebox,'bodyBounds':bodybox,'scale':scale,'position':position,'bounds':bounds})
            folder=BASE/f'frames/{action}-{direction}';folder.mkdir(parents=True,exist_ok=True);board=Image.new('RGB',(1104,232),'#17212a');draw=ImageDraw.Draw(board);gif=[]
            for i,image in enumerate(frames):
                image.save(folder/f'{i:03}.png');board.paste(image,(184*i,24),image);draw.text((184*i+4,4),str(i),fill='white');bg=Image.new('RGB',(240,244),'#17212a');bg.paste(image,(28,24),image);gif.append(bg)
            board.save(review/'contact.png');gif[0].save(review/'motion.gif',save_all=True,append_images=gif[1:],duration=info['metadata']['frameDurationsMs'],loop=0)
    (BASE/'registration.json').write_text(json.dumps({'poses':records,'injuryStatus':'Visual candidate only; no injury trigger added. Installed battery shutdown stays dry.'},indent=2)+'\n');print('Packaged 24 dry shutdown frames and 24 staged white-fluid injury frames from 40 authored poses')
if __name__=='__main__':main()
