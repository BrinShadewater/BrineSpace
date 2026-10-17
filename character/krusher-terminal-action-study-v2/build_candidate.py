from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'krusher-terminal-action-study-v1'
for folder in ['registered','frames','review']:(P/folder).mkdir(parents=True,exist_ok=True)
raw=Image.open(P/'source-01.png').convert('RGBA');cells=[];bounds=[]
for i in range(8):
    x=(i%4)*384;y=(i//4)*512;im=raw.crop((x,y,x+384,y+512));a=np.array(im.getchannel('A'));ys,xs=np.where(a>100)
    box=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)
    assert box[0]>2 and box[1]>2 and box[2]<382 and box[3]<510
    cells.append(im);bounds.append(box)
scale=148/(bounds[0][3]-bounds[0][1]);size=(round(384*scale),round(512*scale));dest=(round(92-(bounds[0][0]+bounds[0][2])/2*scale),round(172-bounds[0][3]*scale))
for i,im in enumerate(cells):
    registered=Image.new('RGBA',(184,184));registered.alpha_composite(im.resize(size,Image.Resampling.LANCZOS),dest);registered.save(P/f'registered/{i:03}.png')
canonical_path=R/'character/krusher-equipment-study-v1/review/fitted-west.png';canonical=Image.open(canonical_path).convert('RGBA');a=np.array(canonical)
yy,xx=np.mgrid[:184,:184];mask=(xx>=49)&(xx<115)&(yy>=62)&(yy<106)
# Feather only the seam, never distort or repaint anatomy. Four native rows
# transition from the canonical upper arm to authored arm/waist source pixels.
weight=np.clip((yy-62)/4,0,1)*mask
Image.fromarray(mask.astype('uint8')*255).save(P/'patch-mask.png')
sources={f'key-{i:03}':OLD/f'registered/{i:03}.png' for i in range(1,8)}
sources.update({f'close-{i:03}':P/f'registered/{i:03}.png' for i in [4,6]})
images={'idle':canonical};records=[];hashes={}
canonical.save(P/'frames/idle.png')
for name,src in sources.items():
    b=np.array(Image.open(src).convert('RGBA'));out=np.round(a*(1-weight[:,:,None])+b*weight[:,:,None]).astype('uint8');im=Image.fromarray(out)
    im.save(P/f'frames/{name}.png');images[name]=im;hashes[str(src.relative_to(R))]=hashlib.sha256(src.read_bytes()).hexdigest()
    records.append({'name':name,'source':str(src.relative_to(R)),'outsidePatchExact':bool(np.array_equal(out[~mask],a[~mask]))})
states=[('terminal-raise-west',['idle','key-001','key-002','key-003'],[120,160,180,200],False),('terminal-type-west',['key-003','key-004','key-005','key-004','key-005','key-003'],[180,160,160,160,160,180],True),('terminal-lower-west',['key-003','close-004','key-006','key-007','close-006','idle'],[100,120,120,140,140,120],False)]
m=json.loads((OLD/'action-manifest.json').read_text());m['name']='Krusher Dom / west terminal action seam and closing revision';m['states']=[];m['status']='unselected candidate; lift inbetweens and full motion review remain'
for key,names,times,loop in states:
    frames=[images[n] for n in names];s={'id':key,'frameFiles':[f'frames/{n}.png' for n in names],'frameCount':len(names),'frameDurationsMs':times,'loop':loop};m['states'].append(s)
    frames[0].save(P/f'review/{key}.png',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=1,blend=0)
m['seamMethod']='Four-row deterministic feather at y62..66; no geometric warping';m['limitations']=['Two newly authored closing/reclipping poses admitted; lift requests repeated key poses and were rejected','Arm/waist patch remains unselected; no continuous-motion or native station acceptance','West bare only; other directions/helmet remain']
(P/'action-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
report={'source':'source-01.png','sourceSha256':hashlib.sha256((P/'source-01.png').read_bytes()).hexdigest(),'sourceHashes':hashes,'alphaRange':list(raw.getchannel('A').getextrema()),'commonScale':scale,'destination':dest,'bounds':bounds,'generationExecutionId':'9b3e620e-9fb1-4b53-adb8-3e583682ecd0','selectedSourceCells':[4,6],'rejectedSourceCells':{'0':'Does not visibly begin reach before existing grasp','1':'Repeated existing grasp','2':'Repeated waist-level closed terminal; missing halfway lift','3':'Fully-open screen; missing halfway opening','5':'Screen still partly open after earlier fully closed pose; physically inconsistent lowering','7':'Glove remains gripping clip; does not release'},'records':records}
(P/'provenance.json').write_text(json.dumps(report,indent=2)+'\n')
board=Image.new('RGB',(1400,290),'#272b2e');draw=ImageDraw.Draw(board);draw.text((14,10),'KRUSHER / REVISED CLOSE AND STOW / DISTINCT AUTHORED INTERMEDIATES',fill='white')
for i,name in enumerate(states[-1][1]):
    im=images[name].resize((184,184),Image.Resampling.NEAREST);board.paste(im,(i*200+8,35),im);draw.text((i*200+10,230),name,fill='white')
board.save(P/'review/closing-sequence.png')
print(json.dumps({'newClosingPoses':2,'uniqueFrames':len(images),'protectedPixelsExact':all(r['outsidePatchExact'] for r in records),'alphaRange':report['alphaRange']}))
