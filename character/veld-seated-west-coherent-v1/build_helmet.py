"""Fit the selected west helmet unchanged to source collar landmarks."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent; R=P.parents[1]
idle_path=R/'character/veld-shared-helmet-v1/frames/idle-west/000.png'
component_path=R/'character/veld-shared-helmet-v1/fitted-west.png'
idle=Image.open(idle_path).convert('RGBA'); component=Image.open(component_path).convert('RGBA'); assert component.size==(34,38)
component.save(P/'native-helmet-component.png')
first=Image.new('RGBA',(256,256)); first.alpha_composite(idle,(36,52)); frames=[first]
registration=json.loads((P/'bare-registration.json').read_text()); m=json.loads((P/'bare-manifest.json').read_text()); records=[]
anchor=[17,36]; necks=[[330,133],[797,169],[1290,220],[335,716],[790,716],[1266,716]]
for slot in range(1,6):
 r=registration['frames'][slot]; scale=registration['fixedRuler']
 neck=[r['position'][axis]+(necks[slot][axis]-r['rawBox'][axis])*scale for axis in range(2)]
 h=registration['headBoxes'][slot]; center=[r['position'][0]+((h[0]+h[2])/2-r['rawBox'][0])*scale,r['position'][1]+((h[1]+h[3])/2-r['rawBox'][1])*scale]
 bare=np.array(Image.open(P/m['states'][0]['frameFiles'][slot]).convert('RGBA')); y,x=np.indices(bare.shape[:2])
 # The low bun extends left of the face landmark in the fourth source pose.
 # Include its complete source silhouette within the head's vertical band.
 erase_box=[r['position'][0]-2,int(np.floor(r['position'][1]+(h[1]-r['rawBox'][1])*scale))-2,int(np.ceil(r['position'][0]+(h[2]-r['rawBox'][0])*scale))+2,min(round(neck[1]),int(np.ceil(r['position'][1]+(h[3]-r['rawBox'][1])*scale))+2)]
 erase=(x>=erase_box[0])&(x<erase_box[2])&(y>=erase_box[1])&(y<erase_box[3])
 fitted=bare.copy(); fitted[erase]=0; position=[round(neck[0]-anchor[0]),round(neck[1]-anchor[1])]
 frame=Image.fromarray(fitted); frame.alpha_composite(component,position); frames.append(frame)
 records.append({'slot':slot,'sourceNeck':necks[slot],'neck':neck,'headCenter':center,'componentPosition':position,'componentSize':list(component.size),'nativeScale':1,'rotationDegrees':0,'eraseBox':erase_box})
files=[]
for slot,frame in enumerate(frames):
 path=P/f'frames/helmet/sit-down-west/{slot:03}.png'; path.parent.mkdir(parents=True,exist_ok=True); frame.save(path); files.append(path.relative_to(P).as_posix())
m['name']='Veld west seated native helmet candidate'; m['equipment']='diving-helmet'; m['states'][0]['frameFiles']=files; m['states'][1]['frameFiles']=files[::-1]; m['states'][2]['frameFiles']=[files[-1]]
(P/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
report={'nativeComponent':'native-helmet-component.png','nativeComponentSha256':hashlib.sha256((P/'native-helmet-component.png').read_bytes()).hexdigest(),'helmetIdle':idle_path.relative_to(R).as_posix(),'helmetIdleSha256':hashlib.sha256(idle_path.read_bytes()).hexdigest(),'nativeComponentAuthority':component_path.relative_to(R).as_posix(),'nativeAnchor':anchor,'frames':records,'scope':'staged source-tracked selected west helmet; exact standing/body/component checks; native and furniture review pending'}
(P/'helmet-registration.json').write_text(json.dumps(report,indent=2)+'\n')
bare_frames=[Image.open(P/f).convert('RGBA') for f in json.loads((P/'bare-manifest.json').read_text())['states'][0]['frameFiles']]
board=Image.new('RGB',(1536,1010),'#202a30'); d=ImageDraw.Draw(board)
for row,sequence in enumerate((bare_frames,frames)):
 for slot,frame in enumerate(sequence):
  x=slot*256; y=row*505; board.paste(frame,(x,y+10),frame); d.text((x+5,y+2),('Bare' if row==0 else 'Helmet')+f' {slot}',fill='white')
  crop=frame.crop((75,65,170,160)).resize((225,225),Image.Resampling.NEAREST); board.paste(crop,(x+15,y+265),crop)
board.save(P/'paired-contact.png')
print(json.dumps({'pairedExports':12,'nativeSize':list(component.size),'normalSelection':False}))
