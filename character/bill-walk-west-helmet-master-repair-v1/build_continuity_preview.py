from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
a=json.loads((OUT/'bank-assessment.json').read_text(encoding='utf-8'));nums=a['frames'];assert len(nums)==len(set(nums))
state=json.loads((ROOT/'character/bill-walk-west-material-v1/helmet-manifest.json').read_text(encoding='utf-8'))['states'][0]
assert state['frameCount']==48 and sum(state['frameDurationsMs'])==2000
freeze=json.loads((OUT/'selected-gait-freeze.json').read_text(encoding='utf-8'))
for path,h in freeze.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h
windows={'wrap':[47,0,1],'early':list(range(4)),'stride':list(range(3,8)),'first8':list(range(8)),'passing':list(range(7,10)),'first10':list(range(10)),'first12':list(range(12)),'first16':list(range(16)),'outward':list(range(16,21)),'first20':list(range(20)),'first24':list(range(24)),'returning':list(range(24,29)),'first29':list(range(29)),'closing':list(range(28,33)),'first33':list(range(33)),'opposite':list(range(32,40)),'first40':list(range(40)),'final':list(range(40,48)),'full48':list(range(48))}
windows={k:v for k,v in windows.items() if all(n in nums for n in v)};assert windows
segments={k:{'frames':v,'holds':[state['frameDurationsMs'][n] for n in v]} for k,v in windows.items()}
paths={str(n):{'old':f'/character/bill-walk-west-material-v1/frames/helmet/walk-west/{n:03}.png','new':f'canvas-normalized-study-{n:03}.png'} for n in nums}
board=Image.new('RGB',(1536,600*((len(nums)+5)//6)),(23,42,51));draw=ImageDraw.Draw(board)
for i,n in enumerate(nums):
 for row,(name,path) in enumerate([('Selected',ROOT/f'character/bill-walk-west-material-v1/frames/helmet/walk-west/{n:03}.png'),('Material study',OUT/f'canvas-normalized-study-{n:03}.png')]):
  im=Image.open(path).convert('RGBA');assert im.size==(256,256);x=(i%6)*256;y=(i//6)*600+row*300
  draw.text((x+8,y+6),f'{name} {n:03}',fill='white');board.paste(im,(x,y+25),im)
board.save(OUT/'bank-overview.png')
headnums=[47]+list(range(8));assert all(n in nums for n in headnums)
heads=Image.new('RGB',(168*len(headnums),420),(23,42,51));draw=ImageDraw.Draw(heads)
for i,n in enumerate(headnums):
 for row,(name,path) in enumerate([('Selected',ROOT/f'character/bill-walk-west-material-v1/frames/helmet/walk-west/{n:03}.png'),('Edited',OUT/f'canvas-normalized-study-{n:03}.png')]):
  crop=Image.open(path).convert('RGBA').crop((99,65,155,122)).resize((168,171),Image.Resampling.NEAREST);x=i*168;y=row*210
  draw.text((x+5,y+5),f'{n:03} {name}',fill='white');heads.paste(crop,(x,y+30),crop)
heads.save(OUT/'opening-helmet-head-review.png')
if len(nums)==48:
 for start in [0,24]:
  b=Image.new('RGB',(1344,840),(23,42,51));d=ImageDraw.Draw(b)
  for i,n in enumerate(range(start,start+24)):
   im=Image.open(OUT/f'canvas-normalized-study-{n:03}.png').convert('RGBA').crop((99,65,155,122)).resize((168,171),Image.Resampling.NEAREST);x=i%8*168;y=i//8*280;d.text((x+4,y+5),f'{n:03} candidate',fill='white');b.paste(im,(x,y+30),im)
  b.save(OUT/f'full48-helmet-collar-{start:02}-{start+23:02}.png')
html=(OUT/'sources/continuity-template.html').read_text(encoding='utf-8')
html=re.sub(r'const segments=.*?;const paths=.*?;',lambda m:'const segments='+json.dumps(segments)+';const paths='+json.dumps(paths)+';',html,count=1)
labels={'wrap':'Loop boundary','early':'First four frames','stride':'Opening stride','first8':'First eight frames','passing':'Approaching feet pass','first10':'First ten frames','first12':'First twelve frames','first16':'First sixteen frames','outward':'Outward stride','first20':'First twenty frames','first24':'First twenty-four frames','returning':'Returning stride','first29':'First twenty-nine frames','closing':'Closing stride','first33':'First thirty-three frames','opposite':'Opposite stride','first40':'First forty frames','final':'Final stride','full48':'Complete forty-eight frame loop'}
options=''.join('<option value="'+k+'">'+labels[k]+': '+('47 to 0 to 1' if k=='wrap' else str(v[0])+' to '+str(v[-1]))+'</option>' for k,v in windows.items())
html=re.sub(r'<select id="segment">.*?</select>','<select id="segment">'+options+'</select>',html,count=1,flags=re.S)
html=html.replace('Bill West walking continuity','Bill West helmet walking continuity').replace('Six authored source studies',str(len(nums))+' authored helmet source studies').replace('six-pose-context-review.png','bank-overview.png').replace('Selected and edited frames47,0,1,28,34,35 with head closeups','Selected and edited complete helmet source bank')
html=html.replace('The grey fabric and brown hair are closer to the master. Small head-outline changes remain at the loop boundary; this is not ready to replace the complete gait.','Suit material is closer to the master. Helmet, face/collar, shoulder/glove and sole continuity remain unaccepted; these source studies are not installed.')
html=html.replace('6 of48bare phases authored; helmet version and full-loop continuity still pending.',str(len(nums))+' of 48 helmet phases authored; complete motion and master consistency remain pending. <a href="index.html">Master and pose closeups</a>.')
(OUT/'continuity.html').write_text(html,encoding='utf-8')
report={'status':'bounded_source_preview_unselected','authoredHelmetStudies':len(nums),'remainingHelmet':48-len(nums),'windows':segments,'selectedGaitFilesUnchanged':98,'normalAdmission':False,'nativeAcceptance':False,'scope':'Original selected holds in contiguous windows; source playback only; actual root/contact and normal-controller acceptance remain pending.'}
(OUT/'continuity-assessment.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
q=OUT/'index.html';s=q.read_text(encoding='utf-8');s=s.replace('<h1>Bill West helmet master pass</h1>','<h1>Bill West helmet master pass</h1><p><a href="continuity.html">Opening stride and loop-boundary comparison</a></p>');q.write_text(s,encoding='utf-8')
print(json.dumps(report))
