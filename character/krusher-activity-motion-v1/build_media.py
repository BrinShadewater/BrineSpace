from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent
lib=json.loads((R/'character/krusher-continuous-playback-v1/library.json').read_text())['states']
jobs=[('review-v2','crew_lounge-q0-helmet'),('review-v2','observation_room-q0-bare'),('review-v2','salvage_workshop-q0-helmet'),('turns-v2','helmet-swim-turn-east-south'),('turns-v2','helmet-swim-carry-turn-east-south'),('repair-v3','helmet-maintenance-east'),('construction-v4','helmet-paid-construction-interruption')]
output=H/'media';output.mkdir(exist_ok=True);results=[]
for lane,episode in jobs:
 report=H/lane/'report.json'
 if not report.exists():continue
 q=json.loads(report.read_text())
 rows=[r for r in q['records'] if r.get('episode')==episode] if lane in ['review-v2','turns-v2'] else [r for r in q['records'] if r['gear']=='helmet' and (lane!='repair-v3' or r['direction']=='east')]
 if not rows:continue
 gear=episode.split('-')[-1] if lane=='review-v2' else episode.split('-')[0]
 frames=[];durations=[]
 for i,r in enumerate(rows):
  key=gear+':'+r['source']['key'];s=lib[key];scale=r['screen'][2]/s['width'];foot=r.get('screenFoot',[r['screen'][j]+s['pivot'][j]*scale for j in [0,1]])
  im=Image.open(H/lane/r['file']).convert('RGB');at=(round(170+r['crop'][0]-foot[0]),round(190+r['crop'][1]-foot[1]))
  frame=Image.new('RGB',(340,320),'#1b272d');frame.paste(im,at);d=ImageDraw.Draw(frame);d.rectangle((0,0,340,32),fill='#142129');d.text((5,3),episode,fill='white');d.text((5,17),r['source']['key']+' / %.3fs'%r['time'],fill='#c8e1e5')
  frames.append(frame);next_time=rows[i+1]['time'] if i+1<len(rows) else r['time']+1/30;durations.append(max(1,round(next_time*1000)-round(r['time']*1000)))
 path=output/(episode+'.webp')
 if not path.exists():frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,loop=0,lossless=True,method=0)
 results.append({'file':path.name,'lane':lane,'episode':episode,'samples':len(rows),'durationMs':sum(durations),'scope':'Foot-aligned native renderer crops; simulated30Hz time, source/position change captures. Not full-room real-time video.'})
(H/'media-index.json').write_text(json.dumps(results,indent=2))
print([{k:v for k,v in q.items() if k not in ['scope']} for q in results])
