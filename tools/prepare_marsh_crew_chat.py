"""Package generated arm gestures on the exact current idle body and head."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
from prepare_marsh_carry_chain import palette_module
from prepare_marsh_full_polish import material_mask,grade
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-crew-chat-v1'
DIRS=('south','north','east','west')
REGIONS={'south':(34,69,82,137),'north':(103,69,156,137),'east':(100,69,153,137),'west':(31,69,86,137)}
DURATIONS=[120,100,140,200,160,140,100,140]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def feet(image):
    a=np.asarray(image.getchannel('A'))>80;y,x=np.where(a);bottom=int(y.max()+1);y,x=np.where(a&(np.arange(image.height)[:,None]>=bottom-9));return (x.min()+x.max()+1)/2,bottom
def main():
    contract=BASE/'contract.json'
    if not contract.exists():
        states=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
        contract.write_text(json.dumps({d:states['idle-'+d]['files'][0] for d in DIRS},indent=2)+'\n')
    idle_paths=json.loads(contract.read_text());sheet=Image.open(BASE/'sources/gesture-sheet-02.png').convert('RGBA');palette=palette_module();mapper=palette.remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
    labels,_=label(np.asarray(sheet.getchannel('A'))>80);counts=np.bincount(labels.ravel());counts[0]=0;components=[]
    for component in np.flatnonzero(counts>1000):
        y,x=np.where(labels==component);box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));components.append((box,int(component)))
    assert len(components)==24
    components.sort(key=lambda r:(int(((r[0][1]+r[0][3])/2)/sheet.height*4),(r[0][0]+r[0][2])/2))
    states=[];records={};registrations=[];board=Image.new('RGB',(1472,840),'#293b40');draw=ImageDraw.Draw(board)
    for row,d in enumerate(DIRS):
        idle=Image.open(ROOT/idle_paths[d]).convert('RGBA');ix,iy=feet(idle);tiles=[]
        for col in range(6):
            box,component=components[row*6+col];a=np.array(sheet);a[labels!=component]=0;a[labels==component,3]=255;tile=Image.fromarray(a).crop(box);tiles.append(tile)
        # One reference-calibrated scale per direction, never pose-height scaling.
        scale=(idle.getbbox()[3]-idle.getbbox()[1])/(tiles[0].getbbox()[3]-tiles[0].getbbox()[1]);poses=[idle.copy()]
        for slot,tile in enumerate(tiles):
            bx,by=feet(tile);scaled=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS);a=np.array(scaled);a[a[:,:,3]<80]=0;a[a[:,:,3]>=80,3]=255;scaled=Image.fromarray(a)
            donor=Image.new('RGBA',idle.size);donor.alpha_composite(scaled,(round(ix-bx*scale),round(iy-by*scale)))
            if slot==0:
                ref=np.zeros((184,184),bool);x0,y0,x1,y1=REGIONS[d];ref[y0:y1,x0:x1]=True
                target,tl,_=material_mask(idle);donor_mask,dl,_=material_mask(donor);gain=float(np.clip(tl[target&ref].mean()/dl[donor_mask&ref].mean(),.8,1.08))
            donor=grade(donor,gain,mapper)[0]
            # Preserve locked torso, pelvis, boots and facial identity. The
            # authored forearm moves inside a documented direction-specific mask.
            mask=Image.new('L',idle.size);ImageDraw.Draw(mask).rectangle(REGIONS[d],fill=255)
            if d=='south' and slot==1:ImageDraw.Draw(mask).polygon([(75,78),(106,78),(106,103),(75,106)],fill=255)
            out=Image.composite(donor,idle,mask)
            # Restrained nod from the canonical head, without resampling it.
            nod=(0,0,0,2,1,0)[slot]
            if nod:
                a=np.asarray(idle);rgb=a[:,:,:3].astype(int);warm=(a[:,:,3]>0)&(rgb[:,:,0]-rgb[:,:,1]>20)&(rgb[:,:,0]-rgb[:,:,2]>45)&(np.arange(idle.height)[:,None]<idle.getbbox()[1]+30)
                ys,xs=np.where(warm);box=(int(xs.min())-1,int(ys.min())-1,int(xs.max())+2,int(ys.max())+2);head=idle.crop(box);ImageDraw.Draw(out).rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=(0,0,0,0));out.alpha_composite(head,(box[0],box[1]+nod))
            poses.append(out);registrations.append({'direction':d,'sourceColumn':slot,'fixedScale':scale,'ivoryGain':gain,'feetAnchor':[float(ix),int(iy)],'armRegion':REGIONS[d],'headTranslation':[0,nod]})
        poses.append(idle.copy());files=[];gifs=[]
        for i,im in enumerate(poses):
            p=BASE/f'frames/crew-chat-{d}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);rel=p.relative_to(ROOT).as_posix();files.append(p.relative_to(BASE).as_posix());records[rel]={'sha256':sha(p),'actor':'marsh','idleSource':idle_paths[d],'idleSha256':sha(ROOT/idle_paths[d]),'gestureSource':'character/marsh-crew-chat-v1/sources/gesture-sheet-02.png'}
            board.paste(im,(i*184,row*210+15),im);draw.text((i*184+3,row*210+194),d+' '+str(i),fill='white');bg=Image.new('RGB',(184,184),'#293b40');bg.paste(im,(0,0),im);gifs.append(bg.resize((368,368),Image.Resampling.NEAREST))
        gifs[0].save(BASE/('crew-chat-'+d+'.gif'),save_all=True,append_images=gifs[1:],duration=DURATIONS,loop=0)
        states.append({'id':'crew-chat-'+d,'frameFiles':files,'frameDurationsMs':DURATIONS,'loop':False})
    board.save(BASE/'contact.png');(BASE/'manifest.json').write_text(json.dumps({'revision':'marsh-crew-chat-v1','canvas':[184,184],'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
    (BASE/'installation.json').write_text(json.dumps({'frames':records,'registration':registrations,'gestureSourceSha256':sha(BASE/'sources/gesture-sheet-02.png'),'method':'Generated forearms on exact selected idle; canonical head translated for restrained nod; exact idle endpoints'},indent=2)+'\n')
    print('Four conversation directions / 32 slots, exact idle joins and locked legs/torso')
if __name__=='__main__':main()
