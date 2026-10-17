from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;records=[q for q in json.loads((P/'revision.json').read_text())['records'] if not q['alias'] and q['changedPixels']];groups={};font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),18)
for q in records:
 # Keep actual neck/collar context; duplicate head/collar crops need one visual review.
 im=Image.open(P/q['output']).convert('RGBA').crop((65,8,121,62));key=(q['gear'],q['state'].rsplit('-',1)[1],hashlib.sha256(im.tobytes()).hexdigest())
 if key not in groups:groups[key]={'image':im,'record':q,'aliases':[]}
 groups[key]['aliases'].append([q['state'],q['index']])
rows=list(groups.values());review=P/'review/source';review.mkdir(parents=True,exist_ok=True)
for start in range(0,len(rows),64):
 chunk=rows[start:start+64];board=Image.new('RGB',(1440,80+((len(chunk)+7)//8)*194),'#252b2e');draw=ImageDraw.Draw(board);draw.text((15,12),'KRUSHER / CANONICAL COMPLETE HEAD-NECK / ALL UNIQUE COLLAR CONTEXTS',font=font,fill='white')
 for j,z in enumerate(chunk):
  x=j%8*180;y=55+j//8*194;im=z['image'].resize((168,162),Image.Resampling.NEAREST);board.paste(im,(x+6,y),im);q=z['record'];draw.text((x+3,y+164),q['gear']+' '+q['state'].replace('interact','tab')+' '+str(q['index']),font=font,fill='#c1d5d5')
 board.save(review/f'heads-{start//64:02}.png')
(review/'index.json').write_text(json.dumps({'changedDrawings':len(records),'distinctHeadCollarCrops':len(rows),'pages':(len(rows)+63)//64,'scope':'All changed drawings grouped only by exact cropped RGBA and gear/direction, actual collar context preserved. Original whole-body conservation checked separately.','groups':[{'representative':z['record']['output'],'slots':z['aliases']} for z in rows]},indent=2)+'\n');print(json.dumps({'changedDrawings':len(records),'distinctHeadCollarCrops':len(rows),'pages':(len(rows)+63)//64}))
