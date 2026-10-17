from pathlib import Path
import json,hashlib
from PIL import Image
R=Path.cwd();P=R/'character/bill-east-interact-master-consistency-v1';N=P/'native';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((N/'verification.json').read_text())
for x in q['pages']:
 assert sha(N/x['file'])==x['sha256'];x['reviewed']=True
for x in q['captures']:
 if isinstance(x,dict): assert sha(N/x['file'])==x['sha256']
for path,h in q['currentContextInputs'].items(): assert sha(R/path)==h,path
assert sha(N/'corrected-source-audit.json')==q['correctedAuditSha256']
assert sha(N/'current-join-context.png')==q['currentContextSha256']
q['visualReview']='All three native capture pages and corrected current context inspected October 3. More readable face/hair and suit definition at H148/82/54/27; brighter face and ivory fittings remain a visible idle/action seam. No gross scale enlargement observed; source edge differences remain. Cyan pivot guide is not world floor/contact proof.'
q['decision']='Retain provisional and unselected; restrained grade pilot before full-family expansion.'
(N/'verification.json').write_text(json.dumps(q,indent=2)+'\n')
B=P/'grade-pilot-v1';B.mkdir(exist_ok=False)
source=P/'frames/interact-east/003.png';canvas=Image.new('RGBA',(352,352));canvas.alpha_composite(Image.open(source).convert('RGBA'),(68,52));canvas.resize((1408,1408),Image.Resampling.NEAREST).save(B/'target.png')
a=json.loads((N/'corrected-source-audit.json').read_text());idle=R/a['selected']['bare']['idle-east']['files'][0];canvas=Image.new('RGBA',(352,352));canvas.alpha_composite(Image.open(idle).convert('RGBA'),(68,52));canvas.resize((1408,1408),Image.Resampling.NEAREST).save(B/'idle-reference.png')
prompt='''Edit Image 1 only: Bill reaching east with his arm fully extended. Image 2 is the original East master, the authority for angular face, warm brown hair/beard, anatomy and detailed illustrated matte graphite suit. Image 3 is his current idle, a supporting reference for subdued exposure and dull pale hardware. Keep every pose coordinate and the complete silhouette of Image 1: same head width and height, chin seated on collar, shoulder joint, extended arm and glove, torso, backpack, legs, boots and exact soles. Preserve Image 1 camera, transparent square canvas, physical scale and placement. Do not copy the reference pose or recenter.
Make a restrained material and lighting consistency edit: bring the overbright cheek, hair highlights and ivory forearm cuff/knee/boot fittings closer to the subdued matte exposure of Image 3. Keep the warm face readable and retain the angular brow/nose/beard identity and fine suit quilt, seams, buckles, shoulder emblem and muted brick red patches from Images 1 and 2. Soft dull hardware, diffuse fabric shading, no gloss or new white rim light. Do not uniformly blacken the character, crush shadows, simplify texture, widen his head/body or change any joint. Result is one complete figure matching Image 1 gesture and exact placement, transparent background. No ground, shadow, labels, grid or additional images.'''
(B/'prompt.txt').write_text(prompt,encoding='utf-8')
refs=[{'path':str(B/'target.png'),'role':'only edit target, whole-canvas nearest4x'},{'path':str(P/'sources/original-east-master-common.png'),'role':'original master identity/material authority'},{'path':str(B/'idle-reference.png'),'role':'current idle subdued exposure reference only'}]
for x in refs:x['sha256']=sha(Path(x['path']))
job={'status':'prepared','method':'builtin imagegen','source':str(source),'sourceSha256':sha(source),'references':refs,'promptFile':str(B/'prompt.txt'),'promptSha256':sha(B/'prompt.txt'),'submittedPromptSha256':sha(B/'prompt.txt'),'frozenInputs':{str(x):sha(x) for x in [source,idle,N/'corrected-source-audit.json',N/'verification.json',P/'sources/original-east-master-common.png']},'returnCrop':[68,52,252,236],'targetTranslation':[68,52],'commonCanvas':[352,352],'standingHeight':148,'normalAdmission':False}
(B/'job.json').write_text(json.dumps(job,indent=2)+'\n');print('Native review hashes checked; grade pilot exact inputs and prompt frozen.')
