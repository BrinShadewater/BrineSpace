from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];B=P.parent/'bill-rest-north-coherent-v1';D=P.parent/'bill-seated-helmet-north-coherent-v1';A=P.parent/'bill-death-ground-helmet-north-coherent-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((B/'manifest.json').read_text());reg=json.loads((B/'registration.json').read_text());donor=json.loads((A/'helmet-registration.json').read_text())
    sources=P/'sources';sources.mkdir(parents=True,exist_ok=True)
    for src,name in [(D/'sources/canonical-head.png','canonical-head.png'),(A/'sources/equipment-v1.png','equipment-perspectives.png'),(A/'sources/prompt-equipment.txt','prompt-equipment.txt')]:shutil.copy2(src,sources/name)
    assert sha(sources/'equipment-perspectives.png')==donor['sourceSha256'] and sha(sources/'canonical-head.png')==donor['authoritySha256']
    canonical=Image.open(sources/'canonical-head.png').convert('RGBA');raw=Image.open(sources/'equipment-perspectives.png').convert('RGBA')
    components={0:canonical};component_hashes={}
    for pose in [1,2,3,4]:
        head=np.array(raw.crop(donor['sourceBoxes'][pose]));rgb=head[:,:,:3].astype(float);neutral=(head[:,:,3]>0)&(np.ptp(rgb,axis=2)<35)
        curve=donor['curveInput'];target=donor['curveOutput'];mapped=np.interp(rgb.mean(2)[neutral],curve,target)
        head[neutral,:3]=np.clip(rgb[neutral]*mapped[:,None]/np.maximum(rgb.mean(2)[neutral,None],1),0,255).astype('uint8')
        image=Image.fromarray(head);sx,sy=donor['helmetRuler'];image=image.resize((round(image.width*sx),round(image.height*sy)),Image.Resampling.LANCZOS)
        f=sources/f'component-{pose}.png';image.save(f);component_hashes[f.name]=sha(f);components[pose]=image
    idle=D/'frames/sit-down-north/000.png';frames=[Image.open(idle).convert('RGBA')];yy,xx=np.indices((256,256));records=[]
    rows=reg['loweringFrames']+reg['frames'];necks=[(461,323),(1065,420),(771,201),(1241,238),(302,669),(769,675),(1249,675)]
    centers=[(461,279),(1065,378),(771,178),(1241,217),(302,638),(769,650),(1249,650)]
    poses=[0,0,1,2,3,4,4]
    for i,row in enumerate(rows,1):
        path=R/m['states'][0]['frameFiles'][i][6:];bare=np.array(Image.open(path).convert('RGBA'));rgb=bare[:,:,:3].astype(float)
        sx,sy=row['scale'];bx,by=row['box'][:2];px,py=row['position'];nx,ny=necks[i-1];neck=[px+(nx-bx)*sx,py+(ny-by)*sy]
        pose=poses[i-1];component=components[pose]
        anchor=[17,29] if pose==0 else [component.width/2,component.height]
        pos=[round(neck[0]-anchor[0]),round(neck[1]-anchor[1])]
        # Lock settled equipment to one registered endpoint; only authored body breathing varies.
        if i==7:pos=records[-1]['position'].copy()
        hx,hy=centers[i-1];center=[px+(hx-bx)*sx,py+(hy-by)*sy]
        local=((xx-center[0])/13)**2+((yy-center[1])/13)**2<1
        warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);erase=local&warm
        out=bare.copy();out[erase]=0;image=Image.fromarray(out);image.alpha_composite(component,pos);frames.append(image)
        records.append({'frame':i,'sourceNeck':list(necks[i-1]),'neck':neck,'position':pos,'componentPose':pose,'componentSize':list(component.size),'nativeScale':1,'sourceComponentRuler':donor['helmetRuler'] if pose else None,'bareSha256':sha(path),'eraseEllipse':{'center':center,'radii':[13,13]},'sleepHelmetLocked':i>=6})
    mapping={};hashes={}
    for i,image in enumerate(frames):
        f=P/f'frames/lie-down-north/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);image.save(f)
        mapping[m['states'][0]['frameFiles'][i]]='res://'+f.relative_to(R).as_posix();hashes[mapping[m['states'][0]['frameFiles'][i]]]=sha(f)
    for state in m['states']:state['frameFiles']=[mapping[f] for f in state['frameFiles']]
    m.update(name='Bill north generic rest with shared rear helmet candidate',equipment='diving-helmet')
    record={'donor':A.relative_to(R).as_posix(),'generation':donor['generation'],'sourceSha256':sha(sources/'equipment-perspectives.png'),'canonicalSha256':sha(sources/'canonical-head.png'),'componentHashes':component_hashes,'endpoint':idle.relative_to(R).as_posix(),'endpointSha256':sha(idle),'bareRegistrationSha256':sha(B/'registration.json'),'frames':records,'scope':'existing authored pitched helmet components fitted over new rest bodies; same component/placement across sleep; no actual north furniture or normal selection proof'}
    for name,data in [('manifest.json',m),('helmet-registration.json',record),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    board=Image.new('RGB',(2048,768),(34,52,62));bm=json.loads((B/'manifest.json').read_text())
    for i,image in enumerate(frames):
        board.paste(image,(i*256,0),image);bare=Image.open(R/bm['states'][0]['frameFiles'][i][6:]);board.paste(bare,(i*256,256),bare);board.paste(frames[0],(i*256,512),frames[0])
    board.save(P/'contact-sheet.png');print('Built north helmet rest3 states/8 slots; authored pitch, stable sleep hardware and paired bodies')
if __name__=='__main__':main()
