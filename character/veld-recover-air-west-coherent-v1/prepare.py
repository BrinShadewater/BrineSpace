from pathlib import Path
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent
s=(P.parent/'veld-recover-air-east-coherent-v1/build.py').read_text()
replacements=[('idle-east-breathing-v1','idle-west-transition-matte-v1'),('SX=.285','SX=.29'),('SY=148/482','SY=148/488'),('HEADS=[(205,11,294,100),(782,36,874,126),(1301,60,1400,153),(296,583,400,680),(785,543,881,637),(1220,522,1318,615)]','HEADS=[(220,16,310,100),(643,46,736,132),(1132,69,1233,158),(169,590,274,681),(687,539,791,629),(1222,523,1320,612)]'),('assert all(n[k]>40000','assert all(n[k]>35000'),('(rx>96)','(rx<85)'),('(bx>np.median(bx))','(bx<np.median(bx))'),('(x>np.median(x))','(x<np.median(x))'),('recover-air-east','recover-air-west'),('east authored','west authored'),("['east']","['west']"),('exec-f3ae57fe-27ea-49ad-be51-875ebf9e88f0','exec-e058d4d6-7cd7-47a3-87af-b12d40768b6b'),('482px maps to148px;158px body width maps to45px','488px maps to148px;142px body width maps to41px')]
for old,new in replacements:
 assert old in s,old
 s=s.replace(old,new)
(P/'build.py').write_text(s)
for name in ['review.py','validate.py']:
 s=(P.parent/'veld-recover-air-east-coherent-v1'/name).read_text().replace('recover-air-east','recover-air-west').replace('east recovery','west recovery').replace('east breathing','west breathing').replace('Native east helmet','Native west helmet')
 (P/name).write_text(s)
f=P.parent/'veld-shared-helmet-v1/frames/idle-west/000.png';im=Image.open(f);a=np.array(im);y,x=np.where(a[:,:,3]>180)
print('donor',im.size,'bbox',x.min(),y.min(),x.max(),y.max())
h=Image.open(P.parent/'veld-shared-helmet-v1/fitted-west.png');print('component',h.size)
s=(P.parent/'veld-recover-air-east-coherent-v1/fit_helmet.py').read_text()
for old,new in [('character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png','character/veld-shared-helmet-v1/frames/idle-west/000.png'),("head=idle.crop((82,17,116,55))","head=Image.open(ROOT/'character/veld-shared-helmet-v1/fitted-west.png').convert('RGBA')"),('canonical-east-helmet','canonical-west-helmet'),('head.rotate(-angle','head.rotate(angle'),('rad=math.radians(angle)','rad=math.radians(-angle)'),('dx=19-head.width/2','dx=15-head.width/2'),('recover-air-east','recover-air-west'),('east native helmet','west native helmet'),('"sourceBox":[82,17,116,55]','"sourceBox":[67,17,101,55]')]:
 s=s.replace(old,new)
# Explicit component provenance: west uses its canonical isolated component.
s=s.replace("'sourceBox':[82,17,116,55]","'componentAuthority':'character/veld-shared-helmet-v1/fitted-west.png'")
(P/'fit_helmet.py').write_text(s)
