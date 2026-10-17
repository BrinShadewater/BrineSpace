from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
H=Path('character/krusher-continuity-audit-v1');B=Path('character/krusher-continuity-bank-v1');P=Path('character/krusher-animation-package-v10');rs=json.loads((B/'revision.json').read_text())['records'];errors=[];n=0
for q in rs:
 a=np.array(Image.open(Path('character/krusher-animation-package-v9')/q['source']).convert('RGBA'))
 if q['changedPixels']:
  b=np.array(Image.open(B/q['output']).convert('RGBA'));m=np.array(Image.open(B/q['mask']))>0
  if not np.array_equal(a[~m],b[~m]):errors.append(q['example'])
  n+=1
assert not errors
assert not json.loads((H/'registered-alias-audit.json').read_text())['conflicts']
(H/'bank-validation.json').write_text(json.dumps({'drawings':len(rs),'changedDrawings':n,'protectedPixelFailures':errors,'authoredAttachmentFailures':[q['example'] for q in rs if q.get('attached') is False],'registeredPoseConflicts':0},indent=2))
# Large collar details for every authored or helmet geometry repair.
qs=[q for q in rs if q['changedPixels'] and 'accent correction' not in q['mode'] and (q.get('newHead') or 'false portrait' in q['mode'])];raw={q['source']:q for q in json.loads(Path('character/krusher-style-neck-bank-v1/revision.json').read_text())['records']}
for page in range((len(qs)+19)//20):
 sheet=Image.new('RGBA',(1200,1150),'#293236');d=ImageDraw.Draw(sheet)
 for i,q in enumerate(qs[page*20:(page+1)*20]):
  x=i%5*240;y=i//5*285;im=Image.open(B/q['output']).convert('RGBA');base=raw[q['sourceRaw']];head=Image.open(q.get('newHead') or base['newHead']);angle=q.get('rotationDegrees',base.get('rotationDegrees',0));head=head.rotate(angle,expand=True);px,py=q.get('newPaste',base['newPaste']);cx=px+head.width/2;cy=py+head.height/2+8;crop=im.crop((round(cx-28),round(cy-30),round(cx+28),round(cy+30)));sheet.alpha_composite(crop.resize((224,240),Image.Resampling.NEAREST),(x+8,y+28));d.text((x+4,y+3),q['example'][:34],fill='white')
 sheet.save(H/('final-collars-%02d.png'%page))
print({'protectedDrawings':len(rs),'changed':n,'collarSheets':(len(qs)+19)//20})
