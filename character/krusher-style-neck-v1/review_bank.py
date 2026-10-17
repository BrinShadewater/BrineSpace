from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
H=Path(__file__).resolve().parent;R=H.parents[1];BASE=R/'character/krusher-animation-package-v8';BANK=R/'character/krusher-style-neck-bank-v1';read=lambda p:json.loads(p.read_text());rev=read(BANK/'revision.json');rows={q['source']:q for q in rev['records']};mapping=read(H/'bank-mapping.json')['records'];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),19)
problems=rev['attachmentFindings'];board=Image.new('RGBA',(1536,max(1,len(problems))*560),'#252d31');draw=ImageDraw.Draw(board)
for i,q in enumerate(problems):
 r=rows[q['source']];meta=mapping[q['source']];images=[Image.open(BASE/q['source']).convert('RGBA'),Image.open(R/meta['originalBody']).convert('RGBA'),Image.open(BANK/r['output']).convert('RGBA')]
 for j,im in enumerate(images):
  board.alpha_composite(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(j*512,i*560+30));draw.text((j*512+8,i*560+5),q['example']+' / '+['before','original body','candidate'][j],font=font,fill='white')
board.save(H/'swim-attachment-diagnostic.png')
index=read(BASE/'package.json');cases=['idle','repair','carry','read-seated','lie-down','sleep','get-up','salvage','death-ground','death-water','swim','swim-distress'];records=[]
for page in range(4):
 board=Image.new('RGBA',(1200,6*230),'#252d31');draw=ImageDraw.Draw(board)
 for group,key in enumerate(cases[page*3:page*3+3]):
  for gi,g in enumerate(['bare','helmet']):
   for di,d in enumerate(['south','east','north','west']):
    full=g+':'+key+'-'+d
    if full not in index['states']:continue
    q=index['states'][full];mp=BASE/q['manifest'];m=read(mp);s=next(s for s in m['states'] if s['id']==key+'-'+d);i=len(s['frameFiles'])//2;rel=(mp.parent/s['frameFiles'][i]).resolve().relative_to(BASE.resolve()).as_posix();record=rows[rel];im=Image.open(BANK/record['output']).convert('RGBA');bbox=im.getbbox();body=im.crop(bbox);x=di*300+10;y=(group*2+gi)*230+25;board.alpha_composite(body,(x+(280-body.width)//2,y));draw.text((x,y-23),full,font=font,fill='white');records.append({'state':full,'frame':i,'bankOutput':record['output']})
 board.save(H/f'family-review-{page}.png')
(H/'family-review-index.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps({'reviewedFamilySamples':len(records),'attachmentDiagnostics':len(problems)}))
