"""Pair source trial with canonical native West equipment, preserving bodies."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;R=P.parent
DONOR=R/'bill-cargo-helmet-west-v1/sources/canonical-head.png'
HEADS=[(158,80),(147,114),(141,118),(130,150),(131,188)]
ENDS=['bill-shared-helmet-runtime-v2/frames/idle-west/000.png','bill-swim-helmet-west-coherent-v1/frames/swim-west/000.png']
PIVOTS=[(92,172),(86,88)]
TIMES=[60,70,80,60,80,90,60]
def main():
    head=Image.open(DONOR).convert('RGBA');assert head.size==(40,40)
    inventory=json.loads((R.parent/'output/bill-flood-source-registration-v1/metadata.json').read_text())
    records=[];endpoints=[];frames=[]
    yy,xx=np.indices((320,320))
    for i in range(7):
        bare=Image.open(P/f'bare/frames/land-swim-west/{i:03}.png').convert('RGBA')
        b=np.array(bare)
        if i in [0,6]:
            j=0 if i==0 else 1
            im=Image.open(R/ENDS[j]).convert('RGBA')
            key=hashlib.sha256(im.tobytes()).hexdigest()
            kind='idle-west' if j==0 else 'swim-west'
            found=[m for m in inventory.get(key,[]) if m['gear']=='diving-helmet' and m['key']==kind and m['index']==0]
            assert len(found)==1 and found[0]['pivot']==list(PIVOTS[j])
            pos=(160-PIVOTS[j][0],224-PIVOTS[j][1])
            out=Image.new('RGBA',(320,320));out.alpha_composite(im,pos)
            assert out.crop((pos[0],pos[1],pos[0]+im.width,pos[1]+im.height)).tobytes()==im.tobytes()
            endpoints.append({'pose':i,'file':ENDS[j],'pivot':PIVOTS[j],'position':pos,'normalMetadata':found[0],'decodedSHA256':key,'paddedPixelsExact':True})
        else:
            x,y=HEADS[i-1];pos=(x-15,y-4)
            poly=[(x-17,y-3),(x+18,y-3),(x+19,y+23),(x+8,y+33),(x-17,y+33),(x-18,y+22)]
            erase=Image.new('L',(320,320));ImageDraw.Draw(erase).polygon(poly,fill=255)
            e=np.array(erase)>0
            a=b.copy();a[e]=0
            out=Image.fromarray(a);out.alpha_composite(head,pos);a=np.array(out)
            fg=(((yy>=y+27)&(xx>=x+7))|((yy>=y+33)&(xx<=x-5))|((yy>=y+18)&(xx<=x-22)))&(b[:,:,3]>0)
            a[fg]=b[fg]
            headarea=Image.new('L',(320,320));headarea.paste(head.getchannel('A'),pos)
            allowed=e|(np.array(headarea)>0)
            assert np.array_equal(a[~allowed],b[~allowed])
            assert np.array_equal(a[fg],b[fg])
            assert np.array_equal(a[yy>=pos[1]+40],b[yy>=pos[1]+40])
            out=Image.fromarray(a)
            records.append({'pose':i,'bareCrown':HEADS[i-1],'position':pos,'scale':1,'rotationDegrees':0,'erasePolygon':poly,'foregroundLeftMaxXMinY':[x-5,y+33],'farGloveMaxXMinY':[x-22,y+18],'foregroundRightMinXMinY':[x+7,y+27],'bodyOutsideHeadExact':True,'foregroundExact':True,'protectedBodyFromY':pos[1]+40})
        frames.append(out)
    manifest=copy.deepcopy(json.loads((P/'bare/manifest.json').read_text()))
    manifest.update(name='Bill West compact water entry canonical helmet trial',equipment='diving-helmet')
    manifest['states'][0]['provenance']='Exact loaded standing/swim endpoint context, five protected bare intermediate bodies, original canonical West40x40 head/helmet at native scale1 rotation0. No gameplay admission.'
    F=P/'helmet/frames/land-swim-west';F.mkdir(parents=True,exist_ok=True)
    hashes={}
    for i,im in enumerate(frames):
        path=F/f'{i:03}.png';im.save(path);hashes[path.relative_to(P).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    (P/'helmet/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    ap=P/'helmet/source-enter.png'
    frames[0].save(ap,save_all=True,append_images=frames[1:],duration=TIMES,loop=0,disposal=0,blend=0)
    with Image.open(ap) as decoded:
        assert decoded.n_frames==7
        for i,im in enumerate(frames):
            decoded.seek(i);assert decoded.convert('RGBA').tobytes()==im.tobytes() and decoded.info['duration']==TIMES[i]
    head.save(P/'sources/canonical-west-helmet.png')
    board=Image.new('RGB',(2240,720),'#182932');d=ImageDraw.Draw(board)
    for row,gear in enumerate(['bare','helmet']):
        for i in range(7):
            im=Image.open(P/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA')
            board.paste(im,(i*320,row*360+25),im)
            d.text((i*320+5,row*360+5),gear+' '+str(i),fill='white')
            if i<3:d.line((i*320,row*360+249,i*320+319,row*360+249),fill='#6aa39e')
    board.save(P/'paired-helmet-review.png')
    detail=Image.new('RGB',(2800,640),'#182932');d=ImageDraw.Draw(detail)
    crowns=[(157,78)]+HEADS+[(134,195)]
    for row,gear in enumerate(['bare','helmet']):
        for i,(x,y) in enumerate(crowns):
            im=Image.open(P/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA')
            crop=im.crop((x-45,y-10,x+55,y+65)).resize((400,300),Image.Resampling.NEAREST)
            detail.paste(crop,(i*400,row*320+20),crop);d.text((i*400+5,row*320+3),gear+' pose'+str(i)+' /same4x ruler',fill='white')
    detail.save(P/'helmet-neck-details.png')
    e={'scope':'Canonical helmet pairing source trial; native motion/material/collision/live gait/Continue pending.','donor':DONOR.relative_to(R).as_posix(),'donorSHA256':hashlib.sha256(DONOR.read_bytes()).hexdigest(),'helmetSize':[40,40],'scale':1,'rotationDegrees':0,'frames':records,'endpointAuthorities':endpoints,'decodedAPNGFramesExact':7,'timelineMs':sum(TIMES),'frameSHA256':hashes,'visualAcceptance':'pending full source and neck review'}
    (P/'helmet-registration.json').write_text(json.dumps(e,indent=2)+'\n')
    print(json.dumps({'nativeHelmetFits':5,'exactEndpointContexts':2,'decodedAPNGFramesExact':7,'ms':sum(TIMES),'bodyProtectionAssertionsPassed':True}))
if __name__=='__main__':main()
