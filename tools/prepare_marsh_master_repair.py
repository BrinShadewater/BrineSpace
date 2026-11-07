"""Freeze current selection and lay out unique authored poses for source editing."""
from pathlib import Path
import json,hashlib
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-master-repair-v1'
def visual(im):
 crop=im.crop(im.getbbox());return hashlib.sha256(str(crop.size).encode()+crop.tobytes()).hexdigest()
def main():
 BASE.mkdir(parents=True,exist_ok=True);(BASE/'inputs').mkdir(exist_ok=True);(BASE/'sources').mkdir(exist_ok=True)
 frozen=BASE/'baseline-contract.json'
 if not frozen.exists():frozen.write_bytes((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_bytes())
 states=json.loads(frozen.read_text())['states'];findings=json.loads((ROOT/'character/marsh-master-comparison-v1/findings.json').read_text())
 protected=set()
 for k,s in states.items():
  if k.startswith(('idle-','walk','crew-chat-','torch-','weld')):
   protected.update(visual(Image.open(ROOT/f).convert('RGBA')) for f in s['files'])
 poses={}
 for k,s in states.items():
  group=next(x for x in findings if any(k.startswith(p) for p in x['prefixes']))
  if not group['priority']:continue
  for i,f in enumerate(s['files']):
   im=Image.open(ROOT/f).convert('RGBA');v=visual(im)
   if v in protected:continue
   poses.setdefault(v,{'id':v,'source':f,'key':k,'slot':i,'group':group['group'],'sha256':hashlib.sha256((ROOT/f).read_bytes()).hexdigest(),'uses':[]})['uses'].append([k,i,f])
 sheets=[]
 for group in [x['group'] for x in findings if x['priority']]:
  entries=[p for p in poses.values() if p['group']==group]
  for start in range(0,len(entries),24):
   batch=entries[start:start+24];index=len(sheets);sheet=Image.new('RGBA',(1536,1024));layout=[]
   for n,p in enumerate(batch):
    im=Image.open(ROOT/p['source']).convert('RGBA');box=im.getbbox();crop=im.crop(box)
    scale=min(220/crop.width,220/crop.height);size=(round(crop.width*scale),round(crop.height*scale));crop=crop.resize(size,Image.Resampling.NEAREST)
    x=(n%6)*256+(256-size[0])//2;y=(n//6)*256+(256-size[1])//2
    sheet.alpha_composite(crop,(x,y));layout.append(dict(p,cell=n,sourceBox=box,placedBox=[x,y,x+size[0],y+size[1]]))
   path=BASE/f'inputs/sheet-{index:02}.png';sheet.save(path)
   sheets.append({'index':index,'group':group,'input':path.relative_to(ROOT).as_posix(),'poses':layout})
 (BASE/'edit-plan.json').write_text(json.dumps({'states':len(states),'slots':sum(len(s['files']) for s in states.values()),'uniqueEditablePoses':len(poses),'sheets':sheets},indent=2)+'\n')
 print(len(poses),'unique editable poses;',len(sheets),'source sheets',[(s['index'],s['group'],len(s['poses'])) for s in sheets])
if __name__=='__main__':main()
