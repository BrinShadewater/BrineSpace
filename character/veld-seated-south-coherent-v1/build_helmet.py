"""Fixed native front helmet, source-tracked collar, no component regrade."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
component_path=R/'character/veld-shared-helmet-south-v1/fitted-helmet.png';idle_path=R/'character/veld-shared-helmet-v1/frames/idle-south/000.png'
component=Image.open(component_path).convert('RGBA');assert component.size==(35,39)
first=Image.new('RGBA',(256,256));first.alpha_composite(Image.open(idle_path).convert('RGBA'),(36,52));frames=[first]
registration=json.loads((P/'bare-registration.json').read_text());m=json.loads((P/'bare-manifest.json').read_text());records=[]
# Source standing collar maps to104px; existing selected component is at69px.
# Preserve that35px crown-to-collar anchor for every interior pose.
anchor=[17,35]
for slot in range(1,6):
 r=registration['frames'][slot];scale=registration['fixedRuler']
 neck=[r['position'][axis]+(registration['necks'][slot][axis]-r['rawBox'][axis])*scale for axis in range(2)]
 center=[r['position'][axis]+(registration['heads'][slot][axis]-r['rawBox'][axis])*scale for axis in range(2)]
 bare=np.array(Image.open(P/m['states'][0]['frameFiles'][slot]).convert('RGBA'));y,x=np.indices(bare.shape[:2]);erase=((x-center[0])**2+(y-center[1])**2<18**2)&(y<=round(neck[1]))
 fitted=bare.copy();fitted[erase]=0;position=[round(neck[0]-anchor[0]),round(neck[1]-anchor[1])]
 frame=Image.fromarray(fitted);frame.alpha_composite(component,position);frames.append(frame)
 records.append({'slot':slot,'neck':neck,'headCenter':center,'componentPosition':position,'componentSize':list(component.size),'nativeScale':1,'rotationDegrees':0,'eraseRadius':18,'eraseYMax':round(neck[1])})
files=[]
for slot,frame in enumerate(frames):
 path=P/f'frames/helmet/sit-down-south/{slot:03}.png';path.parent.mkdir(parents=True,exist_ok=True);frame.save(path);files.append(path.relative_to(P).as_posix())
m['name']='Veld south seated native helmet candidate';m['equipment']='diving-helmet';m['states'][0]['frameFiles']=files;m['states'][1]['frameFiles']=files[::-1];m['states'][2]['frameFiles']=[files[-1]]
(P/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
report={'nativeComponent':component_path.relative_to(R).as_posix(),'nativeComponentSha256':hashlib.sha256(component_path.read_bytes()).hexdigest(),'helmetIdle':idle_path.relative_to(R).as_posix(),'helmetIdleSha256':hashlib.sha256(idle_path.read_bytes()).hexdigest(),'nativeAnchor':anchor,'frames':records,'scope':'staged source-tracked fixed-scale front helmet; exact standing/body/component checks, native/furniture/motion acceptance distinct'}
(P/'helmet-registration.json').write_text(json.dumps(report,indent=2)+'\n')
bare_frames=[Image.open(P/f).convert('RGBA') for f in json.loads((P/'bare-manifest.json').read_text())['states'][0]['frameFiles']]
board=Image.new('RGB',(1536,1010),'#202a30');d=ImageDraw.Draw(board)
for row,sequence in enumerate((bare_frames,frames)):
 for slot,frame in enumerate(sequence):
  x=slot*256;y=row*505;board.paste(frame,(x,y+10),frame);d.text((x+5,y+2),('Bare' if row==0 else 'Helmet')+f' {slot}',fill='white')
  crop=frame.crop((104,65,152,140)).resize((144,225),Image.Resampling.NEAREST);board.paste(crop,(x+56,y+265),crop)
board.save(P/'paired-contact.png')
print(json.dumps({'pairedExports':12,'nativeSize':list(component.size),'normalSelection':False}))
