from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'heel-peel-guide-v1';D.mkdir(exist_ok=True)
source=R/'character/veld-east-held-original-master-v1/frames/bare/000.png'
im=Image.open(source).convert('RGBA');large=im.resize((1024,1024),Image.Resampling.NEAREST)
large.save(D/'original-native-master-4x.png')
guide=Image.new('RGB',(1024,1024),(32,43,49));guide.paste(large,(0,0),large);d=ImageDraw.Draw(guide)
near=(125*4,222*4);toe=(146*4,218*4);heel=(134*4,214*4)
for point,line,label,color in [(near,(220,925),'NEAR foreground boot: unchanged and planted',(108,197,232)),(toe,(710,915),'FAR right toe: stays touching its original floor',(137,218,158)),(heel,(710,795),'FAR heel only: peel UP slightly, toe stays down',(237,174,103))]:
 d.line((line[0],line[1],point[0],point[1]),fill=color,width=2)
 d.ellipse((point[0]-4,point[1]-4,point[0]+4,point[1]+4),outline=color,width=2)
 d.text((40 if point==near else 650,line[1]-20),label,fill=color)
d.line((heel[0]+4,heel[1]-3,heel[0]+4,heel[1]-11),fill=(237,174,103),width=2)
d.line((heel[0],heel[1]-7,heel[0]+4,heel[1]-11,heel[0]+8,heel[1]-7),fill=(237,174,103),width=2)
guide.save(D/'heel-peel-authoring-guide.png')
(D/'GUIDE.json').write_text(json.dumps({'appearanceAuthority':source.relative_to(R).as_posix(),'originalSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'enlargement':'Whole unchanged original native master4x nearest.','annotationRole':'Instructional foot roles only: near unchanged, far toe stays down, far heel peels slightly upward. Markers are approximate visible authoring anchors, not calibrated physical contacts. Never render labels/arrows into output.','scope':'No new pose/artwork/contact acceptance.'},indent=2)+'\n',encoding='utf-8')
print('Original whole master and separate heel/toe instruction guide saved.')
