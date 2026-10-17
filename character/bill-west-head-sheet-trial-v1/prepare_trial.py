from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
OUT.joinpath('sources').mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bank=ROOT/'character/bill-walk-west-master-repair-v2'
assessment=bank/'bank-assessment.json';poses={q['frame']:bank/q['study'] for q in json.loads(assessment.read_text())['poses']}
sheet=Image.new('RGBA',(704,704));records=[]
for cell,i in enumerate([25,31,32,37]):
 p=poses[i];im=Image.open(p).convert('RGBA');assert im.size==(256,256)
 x=(cell%2)*352;y=(cell//2)*352;sheet.alpha_composite(im,(x+32,y))
 records.append({'frame':i,'sourcePath':str(p),'sourceSha256':sha(p),'cell':[x,y,x+352,y+352],'originalCrop':[32,0,288,256],'originalCanvas':[256,256],'commonPivot':[160,224]})
target=OUT/'sources/whole-four-pose-target-4x.png';sheet.resize((2816,2816),Image.Resampling.NEAREST).save(target)
prompt="Edit this single transparent sprite sheet containing exactly four complete poses in a fixed 2 by 2 grid. Preserve every cell, all empty margins and each body's size, location, collar/shoulders, hands, stride, legs, toes and soles exactly. Correct only the four heads to the same slightly more compact natural proportions, about10percent smaller skull/hair/beard silhouette, still naturally attached at the existing collar. Keep the existing left-facing perspective and natural vertical bob of each pose. Give all four heads the same mature angular Bill face, warm brown hair/beard, clear eye/nose lines and restrained skin shadows. Keep the same subdued matte charcoal-grey quilted suit, muted brick-red panels, dull ivory hardware and small cyan accents across all four. Clarify existing seams/rivets and shoulder circle insignia within the existing square border, without changing suit construction or exposure. Do not enlarge, move, recenter or reshape any body. Do not rearrange the grid or invent poses. Return the entire exact same square transparent sheet with four fully visible original poses and coherent head/detail corrections."
pf=OUT/'sources/prompt-v1.txt';pf.write_text(prompt,encoding='utf-8')
q={'revision':1,'status':'prepared','method':'builtin imagegen','singleGenerationFourPoses':True,'references':[{'path':str(target),'sha256':sha(target),'role':'single whole-sheet edit target'}],'promptFile':str(pf),'promptSha256':sha(pf),'submittedPromptSha256':sha(pf),'normalizationCanvas':[704,704],'standingRuler':148,'poses':records,'assessmentPath':str(assessment),'assessmentSha256':sha(assessment),'normalAdmission':False}
(OUT/'generation-job-v1.json').write_text(json.dumps(q,indent=2),encoding='utf-8');print('Prepared one four-pose sheet trial and exact extraction contract.')
