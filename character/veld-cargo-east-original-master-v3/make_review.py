from pathlib import Path
import json,shutil,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-cargo-east-original-master-v3';rows=json.loads((O/'records.json').read_text(encoding='utf-8'));records={};checks=0
for gear in ['bare','helmet']:
 chosen=[r for r in rows if r['gear']==gear];records[gear]=[];images=[]
 for row in chosen:
  dest=P/'native-review'/f"{row['name']}.png";dest.parent.mkdir(exist_ok=True);shutil.copy2(O/f"{row['name']}-native.png",dest);images.append(Image.open(dest).convert('RGBA'));records[gear].append({'file':dest.relative_to(P).as_posix(),**row})
 durations=[round((i+1)*1000/30)-round(i*1000/30) for i in range(len(images))]
 images[0].save(P/f'{gear}-native-playback.png',save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0)
 encoded=Image.open(P/f'{gear}-native-playback.png');segments=[];elapsed=0
 for i in range(encoded.n_frames):
  encoded.seek(i);span=encoded.info['duration'];segments.append((elapsed,elapsed+span,encoded.convert('RGBA').copy()));elapsed+=span
 assert round(elapsed)==2367
 for i,original in enumerate(images):
  t=round(i*1000/30)+1;match=next(im for start,end,im in segments if start<=t<end);assert match.tobytes()==original.tobytes();checks+=1
 board=Image.new('RGB',(900,1200),'#202a30');d=ImageDraw.Draw(board)
 selections=[next(r for r in chosen if r['state']=='unload-east' and r['slot']==3),min((r for r in chosen if r['state']=='idle-east'),key=lambda r:r['actorFoot'][0]),next(r for r in chosen if r['state']=='pickup-east' and r['slot']==3)]
 for i,r in enumerate(selections):
  im=Image.open(O/f"{r['name']}-native.png");board.paste(im,(0,i*400));d.rectangle((0,i*400,900,i*400+45),fill='#202a30');d.text((20,i*400+10),['Contact / separate case behind authored hands','Position probe / original standing body moves aside, floor case fixed','Pickup / floor case removed as handheld source resumes'][i],fill='white')
 board.save(P/f'{gear}-native-lifecycle-review.png')
previous=json.loads((R/'output/veld-cargo-east-original-master-v2/inputs-before.json').read_text(encoding='utf-8'));changes=[ref for ref,sha in previous.items() if hashlib.sha256((R/ref).read_bytes()).hexdigest()!=sha];assert not changes
(P/'carry-forward-validation.json').write_text(json.dumps({'previousNativeInputCount':len(previous),'changed':changes,'scope':'Earlier East cargo v2 native-frozen inputs exactly retained.'},indent=2)+'\n',encoding='utf-8')
(P/'review-records.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');(P/'replay-validation.json').write_text(json.dumps({'nativeSamples':len(rows),'exactReplayChecks':checks,'failures':0,'durationPerGearMs':2367,'scope':'Exact native captures replayed; idle root displacement is prescribed position probe, not gait.'},indent=2)+'\n',encoding='utf-8');print(checks,'exact native replay checks0;',len(previous),'earlier inputs unchanged')
