from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
index=json.loads((p/'contact-v13-prompt-index.json').read_bytes())
for i in (3,30):
 f=p/f'walk{i:02d}-contact-v14.png';assert f.exists()
 index['poses'][i].update(source=f.name,prompt=f'walk{i:02d}-contact-v14-prompt.txt',sourceSha256=hashlib.sha256(f.read_bytes()).hexdigest(),promptSha256=hashlib.sha256((p/f'walk{i:02d}-contact-v14-prompt.txt').read_bytes()).hexdigest())
(p/'contact-v14-prompt-index.json').write_text(json.dumps(index,indent=2)+'\n')
source=(p/'build_dense_cycle_v9.py').read_text()
source=source.replace('    if i == 3: return',"    if i in (3,30): return p / f'walk{i:02d}-contact-v14.png'\n    if i == 46: return p / 'walk46-contact-v13.png'\n    if i in (21,34,45): return p / f'walk{i:02d}-material-v10.png'\n    if i == 3: return")
source=source.replace('dense-cycle-v9-','dense-cycle-v14-')
start=source.index('reuse = {}');end=source.index('report =',start);source=source[:start]+'reuse = {}\n'+source[end:]
exec(compile(source,str(p/'build_dense_cycle_v9.py'),'exec'))
source=(p/'pair_helmet_v11.py').read_text().replace("'paired-v11'","'paired-v14'").replace('dense-cycle-v10-prompt-index.json','contact-v14-prompt-index.json')
source=source.replace("'status':'candidate_unselected_motion_review',","'strideDistanceCells':{'carry-west':bm['strideDistanceCells']['walk-west']}, 'status':'candidate_unselected_contact_review',")
exec(compile(source,str(p/'pair_helmet_v11.py'),'exec'))
print('Full49 v14 assembled: new3/30, retained46, exact original head/leg/helmet/stride contracts.')
