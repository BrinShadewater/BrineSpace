from pathlib import Path
import json,hashlib
from PIL import Image
R=Path.cwd();H=R/'character/krusher-continuous-playback-v1';H.mkdir(exist_ok=True);P=R/'character/krusher-animation-package-v11';V=R/'character/krusher-animation-package-v9';read=lambda p:json.loads(p.read_text(encoding='utf8'));pi=read(P/'package.json');vi=read(V/'package.json');br=read(R/'character/krusher-continuity-bank-v1/revision.json')['records'];by={q['source']:q for q in br};style={q['source']:q for q in read(R/'character/krusher-style-neck-bank-v1/revision.json')['records']};states={};cache={}
for key,q in pi['states'].items():
 mp=P/q['manifest'];m=cache.setdefault(str(mp),read(mp));s=next(s for s in m['states'] if s['id']==key.split(':',1)[1]);vp=V/vi['states'][key]['manifest'];vm=cache.setdefault(str(vp),read(vp));vs=next(s for s in vm['states'] if s['id']==s['id'] and s['id']==key.split(':',1)[1]);files=[];boxes=[];heads=[]
 for iii,(f,vf) in enumerate(zip(s['frameFiles'],vs['frameFiles'])):
  path=(mp.parent/f).resolve();im=Image.open(path);bb=im.getbbox();files.append('/'+path.relative_to(R).as_posix());boxes.append(bb);base=by[(vp.parent/vf).resolve().relative_to(V).as_posix()];meta=style[base['sourceRaw']];a=base if base.get('newHead') else meta
  if a.get('newHead'):
   hi=Image.open(R/a['newHead']);hi=hi.rotate(a.get('rotationDegrees',0),expand=True);x,y=a['newPaste'];heads.append([round(x+hi.width/2),round(y+hi.height/2+8)])
  else:heads.append([round((bb[0]+bb[2])/2),bb[1]+25])
  source=q['sourceFrames'][iii];shift=next((v['shift'] for v in read(H/'bunk-registration.json') if v['output']==source),[0,0]);heads[-1]=[a+b for a,b in zip(heads[-1],shift)]
 states[key]={'files':files,'durations':s['frameDurationsMs'],'loop':s.get('loop',False),'pivot':m['pivot'],'width':m['frameWidth'],'height':m['frameHeight'],'heads':heads,'bounds':[min(b[0] for b in boxes)-m['pivot'][0],min(b[1] for b in boxes)-m['pivot'][1],max(b[2] for b in boxes)-m['pivot'][0],max(b[3] for b in boxes)-m['pivot'][1]]}
keys=sorted(states,key=lambda k:(0 if '-turn-' in k else 1,k));plans=[]
for key in keys:
 s=states[key];segments=[]
 if '-turn-' in key:
  gear,action=key.split(':');family,dirs=action.split('-turn-');a,b=dirs.split('-');family='carry' if family=='carry' else family;entry=gear+':'+family+'-'+a;exit=gear+':'+family+'-'+b
  segments=[{'key':entry,'role':'entry','duration':sum(states[entry]['durations'])},{'key':key,'role':'target','duration':sum(s['durations'])},{'key':exit,'role':'destination','duration':sum(states[exit]['durations'])}]
 else:segments=[{'key':key,'role':'target','duration':sum(s['durations'])*(2 if s['loop'] else 1)}]
 if '-turn-' not in key:
  gear,action=key.split(':');direction=action.rsplit('-',1)[-1];stem=action[:-(len(direction)+1)];entry=None;destination=None
  pairs={'sit-down':('idle','sit-idle'),'sit-rise':('sit-idle','idle'),'read-seated-enter':('idle','read-seated'),'read-seated-exit':('read-seated','idle'),'lie-down':('idle','sleep'),'get-up':('sleep','idle'),'bunk-enter':('idle','bunk-sleep'),'bunk-exit':('bunk-sleep','idle'),'pickup':('idle','carry'),'unload':('carry','idle'),'swim-start':('tread','swim'),'swim-stop':('swim','tread'),'kneel':('idle','repair'),'stand':('repair','idle'),'torch-draw':('idle','weld'),'torch-stow':('weld','idle'),'meal-acquire':('idle','eat'),'meal-deposit':('eat','idle'),'cup-acquire':('idle','drink'),'cup-deposit':('drink','idle')}
  if stem in pairs:entry=gear+':'+pairs[stem][0]+'-'+direction;destination=gear+':'+pairs[stem][1]+'-'+direction
  if stem=='equip-helmet':entry='bare:idle-east';destination='helmet:idle-east'
  if stem=='remove-helmet':entry='helmet:idle-east';destination='bare:idle-east'
  if entry in states and destination in states:
   segments=[{'key':entry,'role':'entry','duration':sum(states[entry]['durations'])},{'key':key,'role':'target','duration':sum(s['durations'])*(2 if s['loop'] else 1)},{'key':destination,'role':'destination','duration':sum(states[destination]['durations'])}]
 plans.append({'key':key,'segments':segments,'duration':sum(q['duration'] for q in segments)+500,'targetSlots':len(s['files'])})
(H/'library.json').write_text(json.dumps({'states':states,'plans':plans,'statesTotal':586,'holdsTotal':8058},separators=(',',':')))
print({'states':len(states),'holds':sum(len(s['files']) for s in states.values()),'turnChains':sum('-turn-' in k for k in keys),'batchCount':(len(plans)+5)//6,'estimatedSeconds':round(sum(max(q['duration'] for q in plans[i:i+6]) for i in range(0,len(plans),6))/1000)})
