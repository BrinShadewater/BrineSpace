from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-original-rig-turn-playback-v3';PREV=R/'character/veld-turn-north-east-original-rig-v2'
rows=json.loads((O/'records.json').read_text(encoding='utf-8'));checks=0
for gear in ['bare','helmet']:
 entries=[r for r in rows if r['gear']==gear];ims=[Image.open(O/(r['name']+'-native.png')).convert('RGBA') for r in entries];dur=[33,33,34]*29+[133]
 dest=P/(gear+'-native-chain.png');ims[0].save(dest,save_all=True,append_images=ims[1:],duration=dur,loop=0,disposal=0,blend=0)
 encoded=Image.open(dest);expected=[]
 for im,ms in zip(ims,dur):
  if expected and expected[-1][0].tobytes()==im.tobytes():expected[-1][1]+=ms
  else:expected.append([im,ms])
 assert encoded.n_frames==len(expected);checks+=1
 for i,(im,ms) in enumerate(expected):
  encoded.seek(i);assert encoded.convert('RGBA').tobytes()==im.tobytes();assert abs(encoded.info['duration']-ms)<.01;checks+=2
 assert sum(dur)==3033;checks+=1
 board=Image.new('RGB',(2280,1240),'#202a30');d=ImageDraw.Draw(board)
 for slot in range(6):
  r=next(r for r in entries if r['state']=='carry-turn-north-east' and r['slot']==slot);im=Image.open(O/(r['name']+'-native.png'));x=(slot%3)*760;y=(slot//3)*620;board.paste(im,(x,y+20));d.text((x+10,y+3),f'{gear} turn pose {slot}, {r["time"]:.3f}s',fill='white')
 board.save(P/(gear+'-native-turn-review.png'))
 oldrows=json.loads((R/'output/veld-original-rig-turn-playback-v2/records.json').read_text(encoding='utf-8'))
 strip=Image.new('RGB',(1024,290),'#202a30');sd=ImageDraw.Draw(strip)
 for col,slot in enumerate([3,3,4,5]):
  source=oldrows if col==0 else entries
  r=next(r for r in source if r['gear']==gear and r['state']=='carry-turn-north-east' and r['slot']==slot)
  folder=R/'output/veld-original-rig-turn-playback-v2' if col==0 else O
  im=Image.open(folder/(r['name']+'-native.png')).crop((427,341,683,597));strip.paste(im,(col*256,25));sd.text((col*256+4,4),['previous near','revised near','late intermediate','exact East held'][col],fill='white')
 strip.save(P/(gear+'-native-reveal-comparison.png'))
(P/'preview-validation.json').write_text(json.dumps({'checks':checks,'failures':0,'durationMs':3033,'scope':'Both APNGs reproduce actual native samples with exact merged screenshot pixels and timing; no interpolation or artwork edits.'},indent=2)+'\n',encoding='utf-8')
html=(PREV/'index.html').read_text(encoding='utf-8');head,tail=html.split('const rows=',1);_,tail=tail.split(',cache={}',1);html=head+'const rows='+json.dumps(rows)+',cache={}'+tail
html=html.replace('veld-original-rig-turn-playback-v2','veld-original-rig-turn-playback-v3').replace('Original knee armor and equipment restored. Staged motion review; further contour, material and helmet-angle polish remains.','Knees, hips and boots now turn together in the revised near pose. Staged preview: contour, material and full motion polish remain.')
html=html.replace('<button id="pause">Pause</button>','<button id="pause">Pause</button><button id="nearpose">Review revised pose</button>').replace(';requestAnimationFrame(tick)</script>',';nearpose.onclick=()=>{held=1000;paused=true;pause.textContent="Play"};requestAnimationFrame(tick)</script>')
html=html.replace('t=Math.min(elapsed%3600/1000,2.9)','t=Math.max(0,Math.min(elapsed%3600/1000,2.9))').replace('r=list[Math.min(87,Math.floor(t*30))]','r=list[Math.max(0,Math.min(list.length-1,Math.floor(t*30)))]')
(P/'index.html').write_text(html,encoding='utf-8');print(checks,'native preview encoding checks,0failures; paired native pose boards and reveal comparisons saved')
