from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-shared-original-helmet-west-turns-v1'
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['passed']
records=json.loads((O/'records.json').read_text(encoding='utf-8'));assert len(records)==208
boards=[];movies=[];bindings={};decoded=0
for gear in ['bare','helmet']:
 for action in ['north-west','west-north','south-west','west-south']:
  row=[r for r in records if r['gear']==gear and r['action']==action]
  name=gear+'-'+action;board=Image.new('RGB',(1080,244*math.ceil(len(row)/6)),'#202a30');draw=ImageDraw.Draw(board);frames=[]
  for i,record in enumerate(row):
   source=O/(record['name']+'-source.png');native=O/(record['name']+'-native.png')
   for path in [source,native]:bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
   im=Image.open(native).convert('RGB');frames.append(im);src=Image.open(source).convert('RGBA').resize((96,96),Image.Resampling.LANCZOS)
   x=i%6*180;y=i//6*244;draw.text((x+3,y+3),str(round(record['time'],3))+'s slot'+str(record['sourceIndex']),fill='white');board.paste(src,(x+42,y+16),src);board.paste(im.crop((160,455,340,585)),(x,y+114))
  filename=name+'-native-review.png';board.save(P/filename);boards.append(filename)
  groups=[]
  for i,frame in enumerate(frames):
   hold=round((row[i+1]['time']-row[i]['time'])*1000) if i+1<len(row) else 33
   if groups and frame.tobytes()==groups[-1]['image'].tobytes():groups[-1]['hold']+=hold;groups[-1]['indices'].append(i)
   else:groups.append({'image':frame,'hold':hold,'indices':[i]})
  path=P/(name+'-native-review.apng');movies.append(path.name)
  images=[g['image'] for g in groups];images[0].save(path,format='PNG',save_all=True,append_images=images[1:],duration=[g['hold'] for g in groups],loop=0,disposal=0,blend=0,optimize=False)
  with Image.open(path) as movie:
   assert movie.n_frames==len(groups)
   for i,g in enumerate(groups):
    movie.seek(i);assert movie.info['duration']==g['hold']
    for index in g['indices']:assert movie.convert('RGB').tobytes()==frames[index].tobytes();decoded+=1
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
 path=O/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(P/'native-review-evidence.json').write_text(json.dumps({'boards':boards,'movies':movies,'sourceNativePairs':208,'decodedNativeFramesExact':decoded,'validation':v,'bindings':bindings,'visualReview':'pending','scope':'Standalone shared original West helmet quarters/reverse, finite800ms. Repeating previews are review resets. No world cadence/cardinal-family installation evidence.'},indent=2)+'\n',encoding='utf-8')
print('8 chronological boards /208 source-native pairs;208 lossless native decode checks pass.')
