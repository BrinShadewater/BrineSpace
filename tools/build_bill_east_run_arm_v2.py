"""Package the two repairs, keep four prior frames exact, and expose arm comparisons."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-run-master-v2';A=R/'character/bill-east-run-master-v1'
source=(R/'tools/build_bill_east_run_master_v1.py').read_text(encoding='utf-8').replace('bill-east-run-master-v1','bill-east-run-master-v2')
exec(compile(source,str(R/'tools/build_bill_east_run_master_v1.py'),'exec'))
for slot in [1,2,3,4]:assert (D/f'frames/{slot:03}.png').read_bytes()==(A/f'frames/{slot:03}.png').read_bytes()
board=Image.new('RGBA',(1280,600),'#17252d');draw=ImageDraw.Draw(board)
for col,slot in enumerate([4,5,0,1]):
 for row,(folder,label) in enumerate([(A,'Reported arm'),(D,'Connected arm')]):
  draw.text((col*320+8,row*300+8),f'Phase{slot}: {label}',fill='white')
  im=Image.open(folder/f'frames/{slot:03}.png').convert('RGBA').resize((280,280),Image.Resampling.NEAREST)
  board.alpha_composite(im,(col*320+20,row*300+20))
board.save(D/'arm-comparison.png')
html=(D/'index.html').read_text(encoding='utf-8').replace('All six running poses rebuilt as whole figures to restore the matte quilted suit, hardware and warm face.','Backward-swinging arm corrected in poses 0 and 5: shoulder patch, upper arm, elbow and glove now form one connected sleeve. Four other poses are unchanged.').replace('Master repair','Arm repair').replace('<h2>Every pose beside the current idle</h2>','<h2>Arm comparison through the loop seam</h2><img src="arm-comparison.png"><h2>Every pose beside the current idle</h2>')
html=html.replace('Selected running','Reported arm').replace('id="old" src="selected-1.png"','id="old" src="../bill-east-run-master-v1/candidate-1.png"').replace("['old','selected']","['old','../bill-east-run-master-v1/candidate']").replace("'../bill-run-head-locked-v1/frames/run-east/000.png'","'../bill-east-run-master-v1/frames/000.png'")
(D/'index.html').write_text(html,encoding='utf-8')
print('Four inherited frames byte-identical; changed poses0/5 and neighboring seam comparison saved.')
