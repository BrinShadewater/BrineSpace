"""Keep tall walking evidence readable without altering source drawings."""
from pathlib import Path
import hashlib,json
from PIL import Image
BASE=Path(__file__).resolve().parents[1]/'character/marsh-current-family-audit-2026-10-03-post-cargo'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
path=BASE/'walk-step-contact.png';im=Image.open(path)
for half,(top,bottom) in enumerate([(0,im.height//2),(im.height//2,im.height)]):
    out=BASE/('walk-step-'+['first','second'][half]+'-half.png')
    box=(0,top,im.width,bottom);im.crop(box).save(out)
    records.append({'file':out.name,'sha256':sha(out),'sources':[{'file':path.name,'sha256':sha(path),'crop':box}],'operation':'Exact whole direction-row crop, no scale/paint.'})
for prefix in ['p','phase']:
    paths=[BASE/f'walk-stop-{prefix}{i}-contact.png' for i in range(6)]
    images=[Image.open(p) for p in paths];out=BASE/f'walk-stop-{prefix}-all.png'
    board=Image.new('RGB',(1104,sum(im.height for im in images)));y=0
    for im in images:board.paste(im,(0,y));y+=im.height
    board.save(out)
    records.append({'file':out.name,'sha256':sha(out),'sources':[{'file':p.name,'sha256':sha(p)} for p in paths],'operation':'Six complete original boards stacked, no crop/scale/paint.'})
(BASE/'readable-pages.json').write_text(json.dumps(records,indent=2)+'\n')
print('4readable pages preserve complete walk-step/12stop-phase source boards')
