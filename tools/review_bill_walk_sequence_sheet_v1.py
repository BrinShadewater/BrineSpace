"""Archive a rejected fixed-grid source experiment without extraction/admission."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';D=P/'sequence-000-005-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=D/'raw-sheet.png';im=Image.open(raw).convert('RGBA');a=np.asarray(im)
refs=json.loads((D/'references.json').read_text(encoding='utf-8'))
assert all(sha(Path(r['path']))==r['sha256'] for r in refs)
assert all(sha(Path(r['source']))==r['sourceSha256'] for r in refs if 'source' in r)
assert all(sha(Path(r['path']))==r['sha256'] for r in json.loads((D/'selected-inputs.json').read_text(encoding='utf-8')))
cells=[]
if im.size==(1536,1024):
 for slot in range(6):
  x=(slot%3)*512;y=(slot//3)*512;b=a[y:y+512,x:x+512,3];yy,xx=np.where(b>127)
  source=np.asarray(Image.open(R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png').convert('RGBA'));sy,sx=np.where(source[:,:,3]>127)
  cells.append(dict(slot=slot,rawCellBounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],targetCellBounds=[int(sx.min()*2),int(sy.min()*2),int((sx.max()+1)*2),int((sy.max()+1)*2)],cornerAlpha=int(b[0,0]),opaquePixels=int((b>127).sum())))
report=dict(status='rejected_before_extraction',generationId='exec-e04768b1-78a9-47ee-ad32-569cdbc466a6',rawPath=str(raw),rawSha256=sha(raw),promptSha256=sha(D/'prompt.txt'),references=refs,rawSize=list(im.size),alphaRange=[int(a[:,:,3].min()),int(a[:,:,3].max())],cells=cells,visualReviewed=True,findings=['Whole raw sheet inspected. Figures enlarged/repositioned inside cells, inconsistent with original source geometry.','Background has brown/grey luminous halo; transparency request did not produce clean cutouts.','Six figures are very similar; precise original consecutive motion was not retained reliably.'],normalAdmission=False,nativeTested=False,frameExtraction=False,coverageAdded=0)
(D/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
for name in ['prepare_bill_walk_sequence_sheet_v1.py','review_bill_walk_sequence_sheet_v1.py','prepare_bill_walk_remaining_sources_v1.py']:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
pngs=list(D.glob('*.png'));attrs=subprocess.run(['git','check-attr','filter','--']+[str(p.relative_to(R)).replace('\\','/') for p in pngs],cwd=R,capture_output=True,text=True,check=True);assert all(line.endswith(': filter: lfs') for line in attrs.stdout.splitlines())
print(json.dumps(dict(status=report['status'],rawSize=report['rawSize'],alphaRange=report['alphaRange'],coverageAdded=0,pythonSyntaxFiles=3,pngLfsCount=len(pngs))))
