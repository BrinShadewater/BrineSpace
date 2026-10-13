"""Reuse one repaired whole endpoint across existing turn programs; no art edits."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,copy,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-carry-turn-east-seams-v1';D.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'character/bill-carry-turn-identity-matrix-v5/bare-manifest.json';m=json.loads(old.read_text());target='res://character/bill-cargo-east-master-head-v1/frames/bare/pickup-east/010.png';new='res://character/bill-east-cargo-handoffs-master-v1/frames/pickup-east/010.png';states=[];records=[];protected={old.relative_to(R).as_posix():sha(old)}
for state in m['states']:
 slots=[i for i,p in enumerate(state['frameFiles']) if p==target]
 if not slots:continue
 st=copy.deepcopy(state);st['frameFiles']=[new if p==target else p for p in state['frameFiles']];st['provenance']='Existing whole turn program and original clock; repaired whole East static-held endpoint shared with pickup10 and carry-entry0.';states.append(st)
 for p in state['frameFiles']+st['frameFiles']:protected[p[6:]]=sha(R/p[6:])
 records.append({'key':st['id'],'changedSlots':slots,'originalState':state,'candidateState':st})
assert len(states)==7 and sum(len(r['changedSlots']) for r in records)==7
candidate={k:v for k,v in m.items() if k!='states'};candidate.update(name='Bill carry turns: exact repaired East joins',status='provisional_unselected',states=states);(D/'manifest.json').write_text(json.dumps(candidate,indent=2)+'\n')
pages=[];movies=[]
for rec in records:
 key=rec['key'];rows=[]
 for state in [rec['originalState'],rec['candidateState']]:rows.append([Image.open(R/p[6:]).convert('RGBA') for p in state['frameFiles']])
 count=len(rows[0]);board=Image.new('RGBA',(256*count,550),'#17252d');draw=ImageDraw.Draw(board)
 for row,frames in enumerate(rows):
  for slot,im in enumerate(frames):x=slot*256;y=row*275;draw.text((x+8,y+8),('Previous' if row==0 else 'Shared East')+f' / {slot}',fill='white');board.alpha_composite(im,(x,y+18))
 name=key+'-comparison.png';board.save(D/name);pages.append(name)
 for kind,frames in zip(['previous','candidate'],rows):
  for rate in [1,4]:
   p=D/f'{key}-{kind}-{rate}.png';times=rec['candidateState']['frameDurationsMs'];frames[0].save(p,save_all=True,append_images=frames[1:],duration=[t*rate for t in times],loop=0,disposal=0,blend=0)
   decoded=Image.open(p);assert decoded.n_frames==len(frames)
   for i,im in enumerate(frames):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==im.tobytes() and decoded.info['duration']==times[i]*rate
   movies.append({'file':p.name,'decodedFrames':decoded.n_frames,'durationMs':sum(times)*rate})
q={'records':records,'protectedInputs':protected,'movies':movies,'pages':pages,'changedWholeAliases':7,'newArtSources':0,'unchangedSourceSlots':sum(len(r['candidateState']['frameFiles'])-1 for r in records),'normalAdmission':False,'visualReviewed':False};(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill carry turn joins</title><style>body{background:#17252d;color:#dbe5e9;font:17px system-ui;margin:24px}.row{display:flex;gap:24px}.sprite{height:210px;width:256px}.board{max-width:100%}button{padding:10px}</style><h1>Bill: consistent East carry-turn joins</h1><p>Seven old East held-crate references now share the exact repaired pickup endpoint. Existing turn poses, direction, scale and800/1600ms clocks are retained. No new artwork or normal installation.</p><button id="speed">Quarter speed</button>'''
for r in records:
 key=r['key'];html+=f'<h2>{key}</h2><div class="row">'+''.join(f'<div>{kind}<br><img class="sprite motion" data-name="{key}-{kind}" src="{key}-{kind}-1.png"></div>' for kind in ['previous','candidate'])+f'</div><img class="board" src="{key}-comparison.png">'
html+='''<script>let slow=false;document.querySelector('#speed').onclick=()=>{slow=!slow;document.querySelectorAll('.motion').forEach(im=>im.src=im.dataset.name+'-'+(slow?4:1)+'.png');document.querySelector('#speed').textContent=slow?'Normal speed':'Quarter speed'}</script>''';(D/'index.html').write_text(html,encoding='utf-8')
print(json.dumps({'turnPrograms':7,'changedWholeAliases':7,'untouchedSlots':q['unchangedSourceSlots'],'movies':len(movies),'protected':len(protected)}))
