from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
# Only phase46 passed the neighbouring-pose source review. Preserve rejected raws.
phases=[46]
index=json.loads((p/'dense-cycle-v10-prompt-index.json').read_bytes())
for i in phases:
 f=p/f'walk{i:02d}-contact-v13.png'
 assert f.exists()
 index['poses'][i].update(source=f.name,prompt=f'walk{i:02d}-contact-v13-prompt.txt',
                         sourceSha256=hashlib.sha256(f.read_bytes()).hexdigest(),
                         promptSha256=hashlib.sha256((p/f'walk{i:02d}-contact-v13-prompt.txt').read_bytes()).hexdigest())
(p/'contact-v13-prompt-index.json').write_text(json.dumps(index,indent=2)+'\n')
source=(p/'build_dense_cycle_v9.py').read_text()
source=source.replace('    if i == 3: return',"    if i == 46: return p / 'walk46-contact-v13.png'\n    if i in (21,34,45): return p / f'walk{i:02d}-material-v10.png'\n    if i == 3: return")
source=source.replace('dense-cycle-v9-','dense-cycle-v13-')
start=source.index('reuse = {}');end=source.index('report =',start)
source=source[:start]+'reuse = {}\n'+source[end:]
exec(compile(source,str(p/'build_dense_cycle_v9.py'),'exec'))
source=(p/'pair_helmet_v11.py').read_text()
source=source.replace("'paired-v11'","'paired-v13'").replace('dense-cycle-v10-prompt-index.json','contact-v13-prompt-index.json')
source=source.replace("'status':'candidate_unselected_motion_review',", "'strideDistanceCells':{'carry-west':bm['strideDistanceCells']['walk-west']}, 'status':'candidate_unselected_contact_review',")
exec(compile(source,str(p/'pair_helmet_v11.py'),'exec'))
print('Full49 case-contact v13 and matching original helmet/distance stride rebuilt.')
