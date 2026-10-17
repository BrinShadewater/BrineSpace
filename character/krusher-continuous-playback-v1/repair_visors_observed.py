from pathlib import Path
import json,sys,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
from scipy.spatial import ConvexHull
R=Path.cwd();H=R/'character/krusher-continuous-playback-v1';sys.path.insert(0,str(R/'character/krusher-continuity-audit-v1'));from repair_sources import pad,cyan
V=R/'character/krusher-animation-package-v10';qbank=json.loads((R/'character/krusher-continuity-bank-v1/revision.json').read_text())['records'];style={q['source']:q for q in json.loads((R/'character/krusher-style-neck-bank-v1/revision.json').read_text())['records']};maps=json.loads((R/'character/krusher-style-neck-v1/bank-mapping.json').read_text())['records'];rows=[]
observed=json.loads((H/'visor-observed-polygons.json').read_text());oldrows=json.loads((H/'visor-automatic-rejected.json').read_text())['candidates'];grid={q['sourceRaw']:q['gridBox'] for q in oldrows}
for q in qbank:
 if q['gear']!='helmet' or '-turn-' not in q['example']:continue
 if q.get('portraitPolygon') or 'false portrait' in q['mode']:continue
 if q['example'] not in ['helmet:swim-turn-east-south','helmet:swim-turn-south-west','helmet:swim-carry-turn-east-south','helmet:swim-carry-turn-south-west'] or q['exampleFrame'] not in [1,2,3,4]:continue
 rel='frames/'+q['outputHash']+'.png' if q['changedPixels'] else q['source'];sq=style[q['sourceRaw']]
 if not sq.get('newHead'):continue
 original=pad(Image.open(R/maps[q['sourceRaw']]['originalBody']).convert('RGBA'),sq);raw=np.array(original);before=np.array(Image.open(V/rel).convert('RGBA'));head=Image.open(R/sq['newHead']).convert('RGBA');ang=sq.get('rotationDegrees',0);head=head.rotate(ang,resample=Image.Resampling.BICUBIC,expand=True) if ang else head;pts=np.array(observed[q['example']+':'+str(q['exampleFrame'])])+np.array(grid[q['sourceRaw']][:2]);mask=Image.new('L',original.size);ImageDraw.Draw(mask).polygon([tuple(p) for p in pts],fill=255);ap=np.array(mask)>0;portrait=np.array(Image.open(R/'character/krusher-style-neck-bank-v1'/sq['mask']).convert('L'))>0;over=0;ys,xs=np.where(ap)
 restored=cyan(raw);out=before.copy();out[portrait]=restored[portrait];ha=np.array(head);hr,hg,hb=[ha[:,:,k].astype(float) for k in range(3)];hm=(ha[:,:,3]>120)&(hr>hg*1.1)&(hr>hb*1.15)&(hr>110);hy,hx=np.where(hm);ay,ax=np.where(ap)
 if not len(hx):continue
 face={'style-se-native.png':[16,18],'style-sw-native.png':[8,17],'style-south-bowed-native.png':[11,19],'style-west-native.png':[6,17]}[Path(sq['newHead']).name];at=np.rint([ax.mean()-face[0],ay.mean()-face[1]]).astype(int);layer=Image.new('RGBA',original.size);layer.alpha_composite(head,tuple(at));out[ap,:3]=[26,28,29];merged=np.array(Image.alpha_composite(Image.fromarray(out),layer));out[ap,:3]=merged[ap,:3];dest=H/'pilot'/('visor-'+Path(q['source']).stem+'.png');Image.fromarray(out).save(dest);rows.append({'source':'character/krusher-animation-package-v10/'+rel,'output':dest.relative_to(R).as_posix(),'example':q['example'],'frame':q['exampleFrame'],'sourceRaw':q['sourceRaw'],'gridBox':grid[q['sourceRaw']],'shellOverlapPixels':over,'aperturePixels':int(ap.sum()),'skinPixels':len(xs),'newPaste':at.tolist(),'polygon':pts.tolist(),'head':sq['newHead']})
(H/'visor-pilot.json').write_text(json.dumps(rows,indent=2));print({'candidates':len(rows),'examples':[{k:q[k] for k in ['example','frame','shellOverlapPixels','aperturePixels']} for q in rows[:12]]})
for page in range((len(rows)+11)//12):
 board=Image.new('RGBA',(1440,4*260),'#303c42');d=ImageDraw.Draw(board)
 for j,q in enumerate(rows[page*12:page*12+12]):
  x=j%3*480;y=j//3*260;d.text((x+4,y+2),q['example']+' '+str(q['frame']),fill='white');sq=style[q['sourceRaw']];head=Image.open(R/sq['newHead']);head=head.rotate(sq.get('rotationDegrees',0),expand=True);cx=sq['newPaste'][0]+head.width/2;cy=sq['newPaste'][1]+head.height/2+8
  for col,p in enumerate([R/q['source'],R/q['output']]):
   im=Image.open(p).convert('RGBA').crop((round(cx-28),round(cy-30),round(cx+28),round(cy+30)));board.alpha_composite(im.resize((224,240),Image.Resampling.NEAREST),(x+col*240+5,y+20))
 board.save(H/('visor-pilot-%02d.png'%page))
