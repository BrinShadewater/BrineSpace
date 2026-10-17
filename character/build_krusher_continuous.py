from pathlib import Path
import json,hashlib
from PIL import Image
R=Path.cwd();H=R/'character/krusher-continuous-playback-v1';H.mkdir(exist_ok=True);P=R/'character/krusher-animation-package-v10';V=R/'character/krusher-animation-package-v9';read=lambda p:json.loads(p.read_text(encoding='utf8'));pi=read(P/'package.json');vi=read(V/'package.json');br=read(R/'character/krusher-continuity-bank-v1/revision.json')['records'];by={q['source']:q for q in br};style={q['source']:q for q in read(R/'character/krusher-style-neck-bank-v1/revision.json')['records']};states={};cache={}
for key,q in pi['states'].items():
 mp=P/q['manifest'];m=cache.setdefault(str(mp),read(mp));s=next(s for s in m['states'] if s['id']==key.split(':',1)[1]);vp=V/vi['states'][key]['manifest'];vm=cache.setdefault(str(vp),read(vp));vs=next(s for s in vm['states'] if s['id']==s['id'] and s['id']==key.split(':',1)[1]);files=[];boxes=[];heads=[]
 for f,vf in zip(s['frameFiles'],vs['frameFiles']):
  path=(mp.parent/f).resolve();im=Image.open(path);bb=im.getbbox();files.append('/'+path.relative_to(R).as_posix());boxes.append(bb);base=by[(vp.parent/vf).resolve().relative_to(V).as_posix()];meta=style[base['sourceRaw']];a=base if base.get('newHead') else meta
  if a.get('newHead'):
   hi=Image.open(R/a['newHead']);hi=hi.rotate(a.get('rotationDegrees',0),expand=True);x,y=a['newPaste'];heads.append([round(x+hi.width/2),round(y+hi.height/2+8)])
  else:heads.append([round((bb[0]+bb[2])/2),bb[1]+25])
 states[key]={'files':files,'durations':s['frameDurationsMs'],'loop':s.get('loop',False),'pivot':m['pivot'],'width':m['frameWidth'],'height':m['frameHeight'],'heads':heads,'bounds':[min(b[0] for b in boxes)-m['pivot'][0],min(b[1] for b in boxes)-m['pivot'][1],max(b[2] for b in boxes)-m['pivot'][0],max(b[3] for b in boxes)-m['pivot'][1]]}
keys=sorted(states,key=lambda k:(0 if '-turn-' in k else 1,k));plans=[]
for key in keys:
 s=states[key];segments=[]
 if '-turn-' in key:
  gear,action=key.split(':');family,dirs=action.split('-turn-');a,b=dirs.split('-');family='carry' if family=='carry' else family;entry=gear+':'+family+'-'+a;exit=gear+':'+family+'-'+b
  segments=[{'key':entry,'role':'entry','duration':sum(states[entry]['durations'])},{'key':key,'role':'target','duration':sum(s['durations'])},{'key':exit,'role':'destination','duration':sum(states[exit]['durations'])}]
 else:segments=[{'key':key,'role':'target','duration':sum(s['durations'])*(2 if s['loop'] else 1)}]
 plans.append({'key':key,'segments':segments,'duration':sum(q['duration'] for q in segments)+500,'targetSlots':len(s['files'])})
(H/'library.json').write_text(json.dumps({'states':states,'plans':plans,'statesTotal':586,'holdsTotal':8058},separators=(',',':')))
print({'states':len(states),'holds':sum(len(s['files']) for s in states.values()),'turnChains':sum('-turn-' in k for k in keys),'batchCount':(len(plans)+5)//6,'estimatedSeconds':round(sum(max(q['duration'] for q in plans[i:i+6]) for i in range(0,len(plans),6))/1000)})
