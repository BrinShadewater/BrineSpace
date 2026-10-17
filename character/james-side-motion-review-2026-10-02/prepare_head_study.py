from pathlib import Path
from PIL import Image
import json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1]
bank=json.loads((P/'selected-banks.json').read_bytes())['banks'][0]
path=R/bank['manifest'];pack=json.loads(path.read_bytes());state=next(s for s in pack['states'] if s['id']=='carry-east')
atlas=Image.new('RGBA',(768,512));refs=[]
for i,rel in enumerate(state['frameFiles']):
    file=(path.parent/rel).resolve();im=Image.open(file).convert('RGBA')
    at=((i%3)*256+round(128-pack['pivot'][0]),(i//3)*256+round(224-pack['pivot'][1]))
    atlas.alpha_composite(im,at);refs.append(file.relative_to(R).as_posix())
atlas.save(P/'east-carry-head-edit-target.png')
path=R/'character/crew-runtime-matte-v1/branforth/manifest.json';pack=json.loads(path.read_bytes());state=next(s for s in pack['states'] if s['id']=='idle-east')
file=(path.parent/state['frameFiles'][0]).resolve();shutil.copy2(file,P/'east-idle-master-reference.png')
(P/'head-study-layout.json').write_text(json.dumps({'targetCells':[256,256],'layout':'3columns2rows row-major, six original carry poses, no rescale; registered local pivot128,224','originalSources':refs,'master':file.relative_to(R).as_posix(),'status':'authoring study unselected'},indent=2))
print('Six-pose East carry target and exact idle master prepared.')
