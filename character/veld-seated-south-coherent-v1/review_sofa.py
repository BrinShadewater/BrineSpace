"""Review actual observation sofa source and native sequence joins."""
from pathlib import Path
import json,hashlib,re
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent; R=P.parents[1]; O=R/'output/veld-seated-south-sofa-audit-v1'
data=json.loads((O/'sofa-records.json').read_text()); report=[]; bound={}; labels=['baseline-bare','candidate-bare','baseline-helmet','candidate-helmet']
native=Image.new('RGB',(2048,840),'#202a30'); source_board=Image.new('RGB',(2048,1080),'#202a30'); nd=ImageDraw.Draw(native); sd=ImageDraw.Draw(source_board)
for row,label in enumerate(labels):
 records=[r for r in data['records'] if r['label']==label]
 groups={stage:[r for r in records if r['stage']==stage] for stage in dict.fromkeys(r['stage'] for r in records)}
 down=groups['observation_sit']; read=groups['observation_read']; rise=groups['observation_rise']
 samples=[('Entry',down[0]),('Last down',down[-1]),('First read',read[0]),('Read middle',read[len(read)//2]),('Last read',read[-1]),('First rise',rise[0]),('Last rise',rise[-1]),('Idle',groups[''][0])]
 for col,(name,r) in enumerate(samples):
  im=Image.open(O/r['source']).convert('RGBA'); pivot=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',r['pivot'])]; scale=148/r['standingHeight']
  registered=Image.new('RGBA',(256,256)); sized=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
  registered.alpha_composite(sized,(round(128-pivot[0]*scale),round(224-pivot[1]*scale)))
  source_board.paste(registered,(col*256,row*270+10),registered); sd.text((col*256+3,row*270+2),label+' / '+name,fill='white')
  # Fixed actual sofa context, including back/cushion, actor and grounded feet.
  crop=Image.open(O/r['room']).convert('RGB').crop((490,286,660,391)).resize((256,158),Image.Resampling.NEAREST)
  native.paste(crop,(col*256,row*210+30)); nd.text((col*256+3,row*210+2),label+' / '+name,fill='white')
  bbox=registered.getchannel('A').point(lambda a:255 if a>180 else 0).getbbox()
  report.append({'label':label,'moment':name,'record':r,'registeredOpaqueBounds':bbox,'registeredHeight':bbox[3]-bbox[1]})
  for key in ('source','room'):
   path=O/r[key];bound[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
source_board.save(P/'sofa-source-joins.png'); native.save(P/'sofa-native-joins.png')
for file in ('native.log','validation.json','sofa-records.json','profile-before.json','profile-after.json'):
 path=O/file;bound[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(P/'sofa-review.json').write_text(json.dumps({'scope':'actual observation route/service/stage updates and captured source/native joins; prescribed entry, staged candidate, not chooser/Continue/visual acceptance','station':data['station'],'samples':report,'bindings':bound},indent=2)+'\n')
print(json.dumps({'records':len(data['records']),'joinSamples':len(report),'boundFiles':len(bound),'candidateBareHeights':{r['moment']:r['registeredHeight'] for r in report if r['label']=='candidate-bare'}}))
