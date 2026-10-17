from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-cargo-east-original-master-v2';rows=json.loads((O/'records.json').read_text(encoding='utf-8'));records={}
for gear in ['bare','helmet']:
 chosen=[r for r in rows if r['gear']==gear];records[gear]=[];images=[]
 for r in chosen:
  dest=P/'native-review'/f"{r['name']}.png";dest.parent.mkdir(exist_ok=True);shutil.copy2(O/f"{r['name']}-native.png",dest);images.append(Image.open(dest).convert('RGBA'));records[gear].append({'file':dest.relative_to(P).as_posix(),**r})
 durations=[round((i+1)*1000/30)-round(i*1000/30) for i in range(len(images))]
 images[0].save(P/f'{gear}-native-playback.png',save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0)
 # Verify encoded replay against every original native sample at its chronological time.
 encoded=Image.open(P/f'{gear}-native-playback.png');segments=[];elapsed=0
 for i in range(encoded.n_frames):
  encoded.seek(i);span=encoded.info['duration'];segments.append((elapsed,elapsed+span,encoded.convert('RGBA').copy()));elapsed+=span
 assert round(elapsed)==1800
 for i,original in enumerate(images):
  t=round(i*1000/30)+1;match=next(im for start,end,im in segments if start<=t<end);assert match.tobytes()==original.tobytes()
 board=Image.new('RGB',(1520,900),'#202a30');d=ImageDraw.Draw(board)
 for i in range(6):
  r=next(r for r in chosen if r['state']=='unload-east' and r['slot']==i);im=Image.open(O/f"{r['name']}-native.png").crop((0,300,760,600));board.paste(im,(i%2*760,i//2*300));d.text((i%2*760+3,i//2*300+3),f"{gear} unload {i} / actual native47,93,148",fill='white')
 board.save(P/f'{gear}-native-pose-review.png')
(P/'review-records.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');(P/'replay-validation.json').write_text(json.dumps({'nativeSamples':108,'exactReplayChecks':108,'failures':0,'durationPerGearMs':1800,'scope':'APNG timeline/pixels equal captured native fixture samples; source clock prescribed, not normal gameplay.'},indent=2)+'\n',encoding='utf-8');print('108 exact native replay checks,0 failures')
