"""Inventory selected base walks; diagnostics are not visual animation acceptance."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_fill_holes
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/crew-walk-audit-2026-09-21'
def main():
 OUT.mkdir(exist_ok=True)
 report=[]
 for name in ('major-bill-v3','dr-veld-v2','chief-engineer-branforth-v2','marsh-v2'):
  root=ROOT/'character'/name;catalog=json.loads((root/'catalog.json').read_text());rows=[]
  for rel in catalog['body']:
   manifest_path=root/rel;manifest=json.loads(manifest_path.read_text())
   for state in manifest['states']:
    if state['id'] not in ['walk-'+d for d in ('east','west','north','south')]:continue
    frames=[Image.open((manifest_path.parent/f).resolve()).convert('RGBA') for f in state['frameFiles']]
    top=frames[0].getbbox()[1];upper=[];holes=[];clipped=[]
    for frame in frames:
     pixels=np.array(frame);mask=pixels[:,:,3]>0;gap=binary_fill_holes(mask)&~mask;gap[:119]=False;holes.append(int(gap.sum()))
     bounds=frame.getbbox();clipped.append(bounds[0]==0 or bounds[1]==0 or bounds[2]==frame.width or bounds[3]==frame.height)
     aligned=Image.new('RGBA',frame.size);aligned.alpha_composite(frame,(0,top-bounds[1]));upper.append(hashlib.sha256(np.array(aligned)[:119].tobytes()).hexdigest())
    report.append({'character':name,'state':state['id'],'frames':len(frames),'unique_registered_upper_poses':len(set(upper)),'enclosed_lower_alpha_pixels':holes,'canvas_edge_contact':clipped,'manifest':str(manifest_path.relative_to(ROOT))})
    rows.append((state['id'],frames))
  sheet=Image.new('RGBA',(184*6,210*len(rows)),'#26383c');draw=ImageDraw.Draw(sheet)
  for row,(state,frames) in enumerate(rows):
   for i,frame in enumerate(frames):sheet.alpha_composite(frame,(184*i,210*row))
   draw.text((8,210*row+186),name+' / '+state,fill='white')
  sheet.save(OUT/(name+'.png'))
 (OUT/'report.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report))
if __name__=='__main__':main()
