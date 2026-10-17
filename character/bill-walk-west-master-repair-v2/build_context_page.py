from pathlib import Path
import json,hashlib,re
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
bank=ROOT/'character/bill-walk-west-material-v1'
manifest=json.loads((bank/'manifest.json').read_text(encoding='utf-8'));state=manifest['states'][0]
assert state['frameCount']==48 and sum(state['frameDurationsMs'])==2000
freeze=json.loads((OUT/'selected-gait-freeze.json').read_text(encoding='utf-8'))
assert len(freeze)==98
for p,sha in freeze.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha
numbers=[47,0,1,2,3,28,34,35];rows=[]
board=Image.new('RGB',(2048,930),(23,42,51));draw=ImageDraw.Draw(board)
paths={}
for i,n in enumerate(numbers):
 file='canvas-normalized-study.png' if n==28 else f'canvas-normalized-study-{n:03}.png'
 old=Image.open(bank/f'frames/bare/walk-west/{n:03}.png').convert('RGBA');new=Image.open(OUT/file).convert('RGBA')
 draw.text((i*256+8,6),f'Selected {n:03}',fill='white');board.paste(old,(i*256,25),old)
 draw.text((i*256+8,300),f'Edited {n:03}',fill='white');board.paste(new,(i*256,320),new)
 crop=new.crop((108,70,146,115)).resize((190,225),Image.Resampling.NEAREST);board.paste(crop,(i*256+20,635),crop)
 report=json.loads((OUT/('review.json' if n==28 else f'review-{n:03}.json')).read_text(encoding='utf-8'))
 rows.append({'frame':n,'silhouetteIoU':report['silhouetteIoU'],'selectedBounds':report['selectedBounds'],'editedBounds':report['editedBounds']})
 paths[str(n)]={'old':f'/character/bill-walk-west-material-v1/frames/bare/walk-west/{n:03}.png','new':file}
board.save(OUT/'eight-pose-context-review.png')
wrap=rows[:3];old=[r['selectedBounds'][1] for r in wrap];new=[r['editedBounds'][1] for r in wrap]
d={'authoredBareStudies':8,'remainingBare':40,'remainingHelmet':48,'selectedGaitUnchanged':98,'poses':rows,'wrapFrames':[47,0,1],'wrapSelectedCrownY':old,'wrapEditedCrownY':new,'selectedCrownDelta':[old[1]-old[0],old[2]-old[1]],'editedCrownDelta':[new[1]-new[0],new[2]-new[1]],'sourceFrameDurationsMs':{str(n):state['frameDurationsMs'][n] for n in [47,0,1,2,3,34,35]},'normalSelected':False,'nativeAcceptance':False,'scope':'Three actual adjacent loop boundary poses and one adjacent pair, not a complete48phase loop. Crown changes remain a motion defect; no automatic outline metric establishes identity, joint geometry or material acceptance.'}
(OUT/'context-assessment.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
segments={'wrap':{'frames':[47,0,1],'holds':[state['frameDurationsMs'][n] for n in [47,0,1]]},'adjacent':{'frames':[34,35],'holds':[state['frameDurationsMs'][n] for n in [34,35]]},'early':{'frames':[1,2,3],'holds':[state['frameDurationsMs'][n] for n in [1,2,3]]}}
html=(OUT/'sources/context-template.html').read_text(encoding='utf-8')
html=re.sub(r'const segments=.*?;const paths=.*?;',lambda m:'const segments='+json.dumps(segments)+';const paths='+json.dumps(paths)+';',html,count=1)
assert 'const segments='+json.dumps(segments) in html
html=html.replace('Six authored source studies','Eight authored source studies').replace('six-pose-context-review.png','eight-pose-context-review.png').replace('6 of48bare phases authored','8 of48bare phases authored').replace('Selected and edited frames47,0,1,28,34,35 with head closeups','Eight selected and edited walking poses with head closeups')
(OUT/'context.html').write_text(html,encoding='utf-8')
print('8source studies; selected98unchanged; wrapcrown old'+str(old)+' / edit'+str(new))

p=OUT/'context.html'
html=p.read_text(encoding='utf-8')
html=re.sub(r'<select id="segment">.*?</select>', '<select id="segment"><option value="wrap">Loop boundary: 47 to 0 to 1</option><option value="adjacent">Adjacent poses: 34 to 35</option><option value="early">Early stride: 1 to 2 to 3</option></select>',html,count=1,flags=re.S)
p.write_text(html,encoding='utf-8')
