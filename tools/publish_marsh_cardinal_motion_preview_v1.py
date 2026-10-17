"""Encode deterministic native samples at their recorded 40ms holds."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'output/marsh-animation-audit/cardinal-motion-preview-v3-2026-10-04'
dst=ROOT/'character/marsh-cardinal-motion-preview-v1';dst.mkdir(exist_ok=True)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((src/'report.json').read_text());assert r['failures']==0 and len(r['cases'])==4
fingerprints={}
for kind in ['owner','inputs']:
 a=json.loads((src/(kind+'-before.json')).read_text());b=json.loads((src/(kind+'-after.json')).read_text())
 fingerprints[kind]={'count':len(a),'afterCount':len(b),'changed':[k for k in sorted(a.keys()|b.keys()) if a.get(k)!=b.get(k)]}
assert not fingerprints['owner']['changed']
seqs={};receipts=[]
for case in r['cases']:
 direction=case['direction'];samples=[s for s in r['samples'] if s['direction']==direction]
 assert len(samples)==case['frames'] and [s['index'] for s in samples]==list(range(len(samples)))
 frames=[Image.open(src/s['file']).convert('RGB') for s in samples];seqs[direction]=frames
 assert all(im.size==(400,400) for im in frames)
 movie=dst/(direction+'.apng');frames[0].save(movie,save_all=True,append_images=frames[1:],duration=40,loop=0,disposal=0,blend=0)
 # APNG may merge identical holds. Expand durations and compare exact native pixels.
 apng=Image.open(movie);expanded=0
 for i in range(apng.n_frames):
  apng.seek(i);duration=round(apng.info['duration']);assert duration>0 and duration%40==0
  pixels=apng.convert('RGB').tobytes()
  for unused in range(duration//40):assert frames[expanded].tobytes()==pixels;expanded+=1
 assert expanded==len(frames)
 idle=[s for s in samples if s['key']=='idle-'+direction]
 start=[s for s in samples if s['key']=='walk-start-'+direction]
 walk=[s for s in samples if s['key']=='walk-'+direction]
 stop=[s for s in samples if s['key'].startswith('walk-stop')]
 assert idle and start and walk and stop
 chosen=[idle[0],start[0],walk[len(walk)//2],stop[0],stop[-1],idle[-1]]
 board=Image.new('RGB',(1200,848),'#20292e');draw=ImageDraw.Draw(board)
 for n,sample in enumerate(chosen):
  x=(n%3)*400;y=(n//3)*424;board.paste(frames[sample['index']],(x,y+24));draw.text((x+8,y+7),sample['key']+' / '+str(sample['slot'])+' / '+str(sample['index']*40)+'ms',fill='white')
 boardpath=dst/(direction+'-joins.png');board.save(boardpath)
 receipts.append({'direction':direction,'frameCount':len(frames),'durationMs':40*len(frames),'apng':movie.name,'apngSha256':h(movie),'board':boardpath.name,'boardSha256':h(boardpath),'sampledJoinReview':False,'continuouslyWatchedReview':False,'sampleHashes':[{'file':s['file'],'sha256':h(src/s['file'])} for s in samples],'keys':sorted(set(s['key'] for s in samples))})
length=max(map(len,seqs.values()));combined=[]
for index in range(length):
 frame=Image.new('RGB',(800,848),'#20292e');draw=ImageDraw.Draw(frame)
 for n,direction in enumerate(['east','west','north','south']):
  x=n%2*400;y=n//2*424;frames=seqs[direction];frame.paste(frames[min(index,len(frames)-1)],(x,y+24));draw.text((x+8,y+7),direction.title(),fill='white')
 combined.append(frame)
combined[0].save(dst/'four-directions.apng',save_all=True,append_images=combined[1:],duration=40,loop=0,disposal=0,blend=0)
receipt={'scope':r['scope'],'checks':r['checks'],'failures':r['failures'],'fingerprints':fingerprints,'cases':receipts,'combinedDurationMs':length*40,'combinedPadding':'Shorter routes hold their final captured idle to the longest route; four separate APNGs retain exact original duration. Native crops and footage density unchanged.','combinedSha256':h(dst/'four-directions.apng'),'reportSha256':h(src/'report.json')}
(dst/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':r['checks'],'failures':r['failures'],'samples':len(r['samples']),'fingerprints':fingerprints,'durations':[(x['direction'],x['durationMs']) for x in receipts]}))
