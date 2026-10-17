from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bank=ROOT/'character/bill-walk-west-master-repair-v2'
assessment=bank/'bank-assessment.json'
poses=json.loads(assessment.read_text(encoding='utf-8'))['poses']
assert sorted(p['frame'] for p in poses)==list(range(48))
replacement={int(q['key'].split('-')[-1]):q for q in json.loads((OUT/'review.json').read_text())['poses'] if q['key'].startswith('bare')}
completeCoverage=len(replacement)==48
coverageLabel='Complete head correction study' if completeCoverage else 'Partial head correction diagnostic'
coverageNote='All48 poses have provisional corrections; detail, grade and motion acceptance remain pending.' if completeCoverage else 'Untouched frames intentionally remain visible.'
familyPath=OUT/'family-review.json'
familyCurrent=familyPath.exists() and json.loads(familyPath.read_text(encoding='utf-8'))['frozenInputs'].get(str(OUT/'review.json'))==sha(OUT/'review.json')
familyHtml='<h2>Master, corrected walk and water joint sources</h2><img src="walk-water-master-family-review.png">' if completeCoverage and familyCurrent and (OUT/'walk-water-master-family-review.png').exists() else ''
methodPath=OUT/'shared-to-single-review.json'
if methodPath.exists() and (OUT/'shared-to-single-review.png').exists():
 method=json.loads(methodPath.read_text(encoding='utf-8'))
 if all(Path(p).exists() and sha(Path(p))==h for p,h in method['inputs'].items()):
  familyHtml+='<h2>Original, prior shared study and single-target revision</h2><img src="shared-to-single-review.png">'
inputs={str(assessment):sha(assessment)};old={};new={}
materialPath=OUT/'cropped-master-detail-review.json'
if materialPath.exists() and (OUT/'cropped-master-detail-review.png').exists():
 material=json.loads(materialPath.read_text(encoding='utf-8'))
 if all(Path(p).exists() and sha(Path(p))==h for p,h in material['inputs'].items()):
  familyHtml+='<h2>Face and cropped-master suit-detail studies</h2><img src="cropped-master-detail-review.png">'
  if (OUT/'neighbor-detail-family-review.png').exists():
   familyHtml+='<h2>Neighbor detail groups and water family</h2><img src="neighbor-detail-family-review.png">'
  if (OUT/'middle-detail-family-review.png').exists():
   familyHtml+='<h2>Middle detail gaps and master family</h2><img src="middle-detail-family-review.png">'
  if (OUT/'seam-face-detail-review.png').exists():
   familyHtml+='<h2>Loop seam, face definition and original master</h2><img src="seam-face-detail-review.png">'
  if (OUT/'face-reference-trials-review.png').exists():
   familyHtml+='<h2>Rejected face-reference trials and preferred studies</h2><img src="face-reference-trials-review.png">'
for p in poses:
 i=p['frame'];src=bank/p['study'];inputs[str(src)]=sha(src)
 old[i]=Image.open(src).convert('RGBA');assert old[i].size==(256,256)
 if i in replacement:
  src=OUT/f'bare-walk-{i:03}-candidate.png';inputs[str(src)]=sha(src)
  new[i]=Image.open(src).convert('RGBA')
 else:new[i]=old[i].copy()
frames=[]
for i in range(48):
 im=Image.new('RGBA',(900,600),(31,35,40,255));d=ImageDraw.Draw(im)
 d.text((12,10),f'West walk | source frame {i:02}/47 | {len(replacement)} head studies only | unselected',fill='white')
 for x,label,source in [(10,'Original complete walk',old[i]),(455,coverageLabel,new[i])]:
  d.text((x+10,35),label,fill='white');im.alpha_composite(source,(x+90,60))
  d.line((x+90,284,x+346,284),fill=(70,185,195))
  im.alpha_composite(source.crop((93,55,163,125)).resize((210,210),Image.Resampling.NEAREST),(x+110,345))
 d.text((12,580),'Fixed canvas/ruler148; no frame fitting. '+coverageNote,fill='white')
 frames.append(im)
dur=[42 if i%3 else 41 for i in range(48)];assert sum(dur)==2000
for name,times in [('walk-full-normal.png',dur),('walk-full-slow.png',[x*4 for x in dur])]:
 frames[0].save(OUT/name,save_all=True,append_images=frames[1:],duration=times,loop=1,disposal=0,blend=0)
 with Image.open(OUT/name) as test:
  assert test.n_frames==48
  for i,frame in enumerate(frames):
   test.seek(i);assert test.convert('RGBA').tobytes()==frame.tobytes()
   assert test.info['duration']==times[i]
board=Image.new('RGBA',(1715,840),(31,35,40,255));d=ImageDraw.Draw(board)
groups=[[25,26,27,28,29,30,31],[32,33,34,35,36,37]]
for row,group in enumerate(groups):
 for col,i in enumerate(group):
  x=col*245;y=row*410;d.text((x+8,y+8),f'{i:03} '+('corrected' if i in replacement else 'unchanged'),fill='white')
  for dy,label,source in [(35,'Before',old[i]),(225,'After',new[i])]:
   d.text((x+8,y+dy),label,fill='white')
   crop=source.crop((105,65,155,115)).resize((150,150),Image.Resampling.NEAREST)
   board.alpha_composite(crop,(x+45,y+dy+20))
board.save(OUT/'neighbor-head-review.png')
early=Image.new('RGBA',(1715,1260),(31,35,40,255));ed=ImageDraw.Draw(early)
for row,group in enumerate([[47,0,1,2,3,4,5],[6,7,8,9,10,11,12],[13,14,15,16]]):
 for col,i in enumerate(group):
  x=col*245;y=row*420;ed.text((x+8,y+8),f'{i:03} '+('corrected' if i in replacement else 'unchanged'),fill='white')
  for dy,label,source in [(35,'Before',old[i]),(225,'After',new[i])]:
   ed.text((x+8,y+dy),label,fill='white')
   crop=source.crop((105,65,155,115)).resize((150,150),Image.Resampling.NEAREST)
   early.alpha_composite(crop,(x+45,y+dy+20))
early.save(OUT/'early-neighbor-head-review.png')
mid=Image.new('RGBA',(1715,840),(31,35,40,255));md=ImageDraw.Draw(mid)
for row,group in enumerate([range(14,21),range(21,27)]):
 for col,i in enumerate(group):
  x=col*245;y=row*420;md.text((x+8,y+8),f'{i:03} '+('corrected' if i in replacement else 'unchanged'),fill='white')
  for dy,label,source in [(35,'Before',old[i]),(225,'After',new[i])]:
   md.text((x+8,y+dy),label,fill='white')
   crop=source.crop((105,65,155,115)).resize((150,150),Image.Resampling.NEAREST)
   mid.alpha_composite(crop,(x+45,y+dy+20))
mid.save(OUT/'mid-neighbor-head-review.png')
late=Image.new('RGBA',(1715,840),(31,35,40,255));ld=ImageDraw.Draw(late)
for row,group in enumerate([range(36,43),[43,44,45,46,47,0,1]]):
 for col,i in enumerate(group):
  x=col*245;y=row*420;ld.text((x+8,y+8),f'{i:03} '+('corrected' if i in replacement else 'unchanged'),fill='white')
  for dy,label,source in [(35,'Before',old[i]),(225,'After',new[i])]:
   ld.text((x+8,y+dy),label,fill='white')
   crop=source.crop((105,65,155,115)).resize((150,150),Image.Resampling.NEAREST)
   late.alpha_composite(crop,(x+45,y+dy+20))
late.save(OUT/'late-neighbor-head-review.png')
report={'completeWalkFrames':48,'provisionalHeadCorrections':sorted(replacement),'remainingUncorrected':48-len(replacement),'decodedFramesExact':96,'normalDurationMs':2000,'slowDurationMs':8000,'frozenInputs':inputs,'normalAdmission':False,'nativeAcceptance':False,'fullVisualAcceptance':False}
(OUT/'motion-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
prompts=[];seenGeneration=set()
for path in sorted(OUT.glob('generation-provenance-*.json')):
 q=json.loads(path.read_text(encoding='utf-8'));text=Path(q['promptFile']).read_text(encoding='utf-8')
 if q['generationId'] in seenGeneration:continue
 seenGeneration.add(q['generationId'])
 label=q['key']
 if q.get('derivedSheetPose'):
  shared=json.loads(Path(q['sharedProvenancePath']).read_text(encoding='utf-8'))
  label='shared sheet phases'+','.join(str(p['frame']) for p in shared['poses'])+' (one generation)'
 prompts.append(f"## {label} v{q['revision']} | builtin imagegen | "+('rejected' if q.get('rejected') else 'provisional')+'\n\n'+text+'\n')
(OUT/'prompt-set.md').write_text('# Exact saved head-repair prompts\n\n'+'\n'.join(prompts),encoding='utf-8')
(OUT/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Bill West master head consistency</title>
<style>body{background:#1f2328;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}button{padding:10px;margin:8px}</style>
<h1>Bill West master head consistency</h1><p>PROVISIONAL_COUNT provisional walking head corrections in the full 48-frame sequence, with a focused detail pass. Source comparison only. COVERAGE_NOTE Helmet Ready correction is separate. Full identity, detail and motion acceptance remains pending.</p>
<button onclick="document.getElementById('motion').src='walk-full-normal.png?v='+Date.now()">Replay normally</button>
<button onclick="document.getElementById('motion').src='walk-full-slow.png?v='+Date.now()">Replay slowly</button>
<p><img id="motion" src="walk-full-normal.png" alt="Full walk before and partial correction after"></p>
<h2>Original, proportion correction and detail pass</h2><img src="detail-family-review.png">
FAMILY_REVIEW
<h2>Loop seam and early head frames</h2><img src="early-neighbor-head-review.png"><h2>Middle stride head joins</h2><img src="mid-neighbor-head-review.png"><h2>Closing stride and loop seam</h2><img src="late-neighbor-head-review.png"><h2>Adjacent head frames</h2><img src="neighbor-head-review.png"><h2>Complete current head survey</h2><img src="all48-current-head-review.png"><h2>Complete partial-repair head survey</h2><img src="all48-partial-head-review.png"><h2>Helmet Ready</h2><img src="helmet-ready-neighbor-review.png">
<p><a href="prompt-set.md">Exact prompts (builtin imagegen)</a> · <a href="review.json">Source measurements</a> · <a href="motion-review.json">Full sequence validation</a></p>'''.replace('PROVISIONAL_COUNT',str(len(replacement))).replace('COVERAGE_NOTE',coverageNote).replace('FAMILY_REVIEW',familyHtml),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='frozenInputs'}))
