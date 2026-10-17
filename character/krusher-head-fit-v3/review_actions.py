from pathlib import Path
import json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parents[2]
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22)
for family,actions in [('repair',['kneel','repair','stand']),('torch',['torch-draw','weld','torch-stow']),('seated',['sit-down','sit-idle','sit-rise','read-seated-enter','read-seated','read-seated-exit'])]:
 P=R/f'character/krusher-{family}-family-v3';O=P/'review';F=O/'video-frames';F.mkdir(parents=True,exist_ok=True)
 ms={g:json.loads((P/(g+'-manifest.json')).read_text()) for g in ['bare','helmet']};ss={g:{s['id']:s for s in m['states']} for g,m in ms.items()}
 checks=0;seconds=0;index=0;chapters=[];joins=[]
 for g in ['bare','helmet']:
  old=json.loads((R/f'character/krusher-{family}-family-v1'/(g+'-manifest.json')).read_text())
  assert {k:v for k,v in old.items() if k!='states'}=={k:v for k,v in ms[g].items() if k!='states'};checks+=1
  for a,b in zip(old['states'],ms[g]['states']):
   assert {k:v for k,v in a.items() if k!='frameFiles'}=={k:v for k,v in b.items() if k!='frameFiles'};checks+=1
  for q in json.loads((P/'revision.json').read_text())['records']:
   if q['gear']!=g:continue
   before=np.array(Image.open(R/q['source'][6:]).convert('RGBA'));after=np.array(Image.open(P/q['output']).convert('RGBA'));mask=np.array(Image.open(P/q['mask']))>0
   assert np.array_equal(before[~mask],after[~mask]);checks+=1
   if g=='helmet':assert np.array_equal(before[:,:,3],after[:,:,3]);checks+=1
  for d in ['south','east','north','west']:
   can=R/'character/krusher-james-canonical-v6';cm=json.loads((can/(g+'-manifest.json')).read_text());idle=next(s for s in cm['states'] if s['id']=='idle-'+d)
   im=Image.open(can/idle['frameFiles'][0]).convert('RGBA');expected=Image.new('RGBA',(ms[g]['frameWidth'],ms[g]['frameHeight']));expected.paste(im,(0,0))
   for action,i in [(actions[0],0),(actions[2],-1)]:
    actual=Image.open(P/ss[g][action+'-'+d]['frameFiles'][i]).convert('RGBA')
    assert actual.tobytes()==expected.tobytes();checks+=1;joins.append([g,action+'-'+d,i])
 with (O/'frames.txt').open('w') as listing:
  for d in ['south','east','north','west']:
   for action in actions:
    key=action+'-'+d;s=ss['bare'][key];hs=ss['helmet'][key];start=seconds
    assert s['frameDurationsMs']==hs['frameDurationsMs'];checks+=1
    for i,hold in enumerate(s['frameDurationsMs']):
     board=Image.new('RGB',(800,530),'#252b2e');draw=ImageDraw.Draw(board);draw.text((18,15),'KRUSHER DOM / '+family.upper()+' HEAD FIT',font=font,fill='white');draw.text((18,48),key+' / pose '+str(i)+' / original timing',font=font,fill='#bed2d3')
     for g,x in [('bare',25),('helmet',425)]:
      im=Image.open(P/ss[g][key]['frameFiles'][i]).convert('RGBA');im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);board.paste(im,(x,110),im)
     name=f'{index:04d}.png';board.save(F/name);listing.write(f"file 'video-frames/{name}'\noption framerate 1000\nduration {hold/1000:.9f}\n");index+=1;seconds+=hold/1000;checks+=1
    chapters.append({'state':key,'start':start,'end':seconds})
  listing.write(f"file 'video-frames/{name}'\noption framerate 1000\n")
 with (O/'media.log').open('w') as log:
  subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(O/'frames.txt'),'-t',str(seconds),'-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'head-fit-preview.mp4')],stdout=log,stderr=log,check=True)
 info={'checks':checks,'errors':[],'sourceSeconds':seconds,'pairedSlots':index,'chapters':chapters,'exactCanonicalJoins':joins,'scope':'Every original pose and hold, paired source sprite replay. No station/world acceptance.'}
 (O/'media.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps({'family':family,'checks':checks,'pairedSlots':index,'seconds':seconds,'errors':[]}))

 encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(O/'head-fit-preview.mp4')],text=True));assert abs(encoded-seconds)<=1/60;info['encodedSeconds']=encoded;(O/'media.json').write_text(json.dumps(info,indent=2)+'\n')
