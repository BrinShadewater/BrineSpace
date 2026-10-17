from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];b=root/'character/marsh-retained-gesture-material-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for d,prior,fresh,cell in [('west','03','04',3),('north','02','03',2),('south','03','04',3)]:
 o=b/f'{d}-return{fresh}-unselected';o.mkdir(exist_ok=True)
 pp=b/f'{d}{prior}-unselected/manifest.json';np=b/f'{d}{fresh}-unselected/manifest.json';old=json.loads(pp.read_text());priorfiles=old['states'][0]['frameFiles'].copy();new=json.loads(np.read_text());pick=new['states'][0]['frameFiles'][cell+1]
 for state in old['states']:state['frameFiles'][4]=pick
 old['scope']=f'Unselected {d} whole return figure from new cell{cell}, prior first3gestures and exact own-idle endpoints; original six150ms finite holds. No anatomy fragment mixing or helmet behavior.'
 (o/'manifest.json').write_text(json.dumps(old,indent=2)+'\n')
 seq=[Image.open(root/p.removeprefix('res://')).convert('RGBA') for p in old['states'][0]['frameFiles']]
 seq[0].save(o/'gesture.apng',format='PNG',save_all=True,append_images=seq[1:],duration=[150]*6,loop=1,disposal=0,blend=0)
 ap=Image.open(o/'gesture.apng');assert ap.n_frames==6
 for i,im in enumerate(seq):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==150
 board=Image.new('RGB',(1320,690),'#293b40');draw=ImageDraw.Draw(board)
 for row,(name,paths) in enumerate([('Prior staged',priorfiles),('Whole return candidate',old['states'][0]['frameFiles']),('Own idle',[priorfiles[0]]*6)]):
  for i,p in enumerate(paths):im=Image.open(root/p.removeprefix('res://')).convert('RGBA');board.paste(im,(i*220+18,row*230+30),im);draw.text((i*220+3,row*230+3),f'{name}/{d}/{i}',fill='white')
 bp=o/'return-comparison.png';board.save(bp)
 r={'priorManifest':{'path':pp.relative_to(root).as_posix(),'sha256':sha(pp)},'newSourceManifest':{'path':np.relative_to(root).as_posix(),'sha256':sha(np)},'selectedWholeCell':cell,'slots':[{'path':p.removeprefix('res://'),'sha256':sha(root/p.removeprefix('res://'))} for p in old['states'][0]['frameFiles']],'board':{'path':bp.relative_to(root).as_posix(),'sha256':sha(bp),'actuallyInspected':False},'apngDecodedExactFrames':6,'apngTotalDurationMs':900,'normalAdmission':False,'fullGoalComplete':False}
 (o/'selection.json').write_text(json.dumps(r,indent=2)+'\n')
print('3return candidates: first3whole poses unchanged, one whole return each; North uses new cell2,6exact APNG frames each')
