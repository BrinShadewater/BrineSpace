"""Native selected rear helmet, tracked collar; protected body below the neck."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
COMP=R/'character/veld-shared-helmet-v1/fitted-north.png'
IDLE=R/'character/veld-shared-helmet-v1/frames/idle-north/000.png'
NECKS=[[297,128],[764,185],[1223.5,223],[291.5,707],[765,720],[1236,719]]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
registration=json.loads((P/'bare-registration.json').read_text());manifest=json.loads((P/'bare-manifest.json').read_text())
native=Image.open(COMP).convert('RGBA');first=Image.new('RGBA',(256,256));first.alpha_composite(Image.open(IDLE).convert('RGBA'),(36,52));frames=[first];records=[]
for slot in range(1,6):
    geometry=registration['frames'][slot];scale=registration['fixedRuler']
    neck=[geometry['position'][axis]+(NECKS[slot][axis]-geometry['box'][axis])*scale for axis in range(2)]
    center=[geometry['position'][axis]+(registration['heads'][slot][axis]-geometry['box'][axis])*scale for axis in range(2)]
    bare=Image.open(P/manifest['states'][0]['frameFiles'][slot]).convert('RGBA');pixels=np.array(bare);yy,xx=np.indices(pixels.shape[:2])
    mask=((xx-center[0])**2+(yy-center[1])**2<18**2)&(yy<=round(neck[1]))
    pixels[mask]=0
    position=[round(neck[0]-16),round(neck[1]-32)]
    frame=Image.fromarray(pixels);frame.alpha_composite(native,position);frames.append(frame)
    records.append({'pose':slot,'sourceNeck':NECKS[slot],'neck':neck,'headCenter':center,'componentPosition':position,'componentSize':list(native.size),'nativeScale':1,'rotationDegrees':0,'eraseRadius':18,'eraseYMax':round(neck[1]),'scope':'upright rear component registered to source collar; depth/cadence/furniture review distinct'})
files=[]
for slot,frame in enumerate(frames):
    path=P/f'frames/helmet/sit-down-north/{slot:03}.png';path.parent.mkdir(parents=True,exist_ok=True);frame.save(path);files.append(path.relative_to(P).as_posix())
manifest['name']='Veld north seated current helmet candidate';manifest['equipment']='diving-helmet'
manifest['states'][0]['frameFiles']=files;manifest['states'][1]['frameFiles']=files[::-1];manifest['states'][2]['frameFiles']=[files[-1]]
(P/'helmet-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
data={'nativeComponent':COMP.relative_to(R).as_posix(),'nativeComponentSha256':sha(COMP),'helmetIdle':IDLE.relative_to(R).as_posix(),'helmetIdleSha256':sha(IDLE),'nativeAnchor':[16,32],'sourceNecks':NECKS,'frames':records,'scope':'staged paired chair-height sitting, native rear hardware; exact standing entry, tracked collar, no normal selection/world acceptance'}
(P/'helmet-registration.json').write_text(json.dumps(data,indent=2)+'\n')
board=Image.new('RGB',(1536,810),'#202a30');draw=ImageDraw.Draw(board)
bare_frames=[Image.open(P/f).convert('RGBA') for f in json.loads((P/'bare-manifest.json').read_text())['states'][0]['frameFiles']]
for row,sequence in enumerate([bare_frames,frames,[first]*6]):
    for slot,frame in enumerate(sequence):board.paste(frame,(slot*256,row*270+16),frame);draw.text((slot*256+6,row*270),['Bare','Helmet','Helmet master'][row]+f' {slot}',fill='white')
board.save(P/'paired-contact-sheet.png')
print(json.dumps({'helmetStates':3,'pairedExports':12,'nativeSize':list(native.size),'normalSelection':False}))
