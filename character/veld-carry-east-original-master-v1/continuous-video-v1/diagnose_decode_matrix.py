"""Test explicit standard YUV decode matrices on frame zero; no art grading."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import subprocess,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;D=P/'decode-diagnostic';D.mkdir(exist_ok=True)
source=np.array(Image.open(P/'master-input.png').convert('RGB')).astype(float)
green=(source[:,:,1]>source[:,:,0]+40)&(source[:,:,1]>source[:,:,2]+40)&(source[:,:,1]>100)
mask=ndimage.binary_erosion(~green,iterations=8)
rows=[];board=Image.new('RGB',(1024,1080),'#202a30');draw=ImageDraw.Draw(board)
for i,matrix in enumerate(['bt601','bt709','bt2020']):
 output=D/f'first-{matrix}.png'
 command=['ffmpeg','-y','-v','error','-threads','1','-i',str(P/'source.mp4'),'-vf',f'scale=in_color_matrix={matrix}:out_range=full','-frames:v','1','-threads','1',str(output)]
 result=subprocess.run(command,capture_output=True,text=True);assert result.returncode==0,result.stderr
 image=Image.open(output).convert('RGB');values=np.array(image).astype(float)
 rows.append({'matrix':matrix,'foregroundMeanAbsoluteRGBErrorVsInput':float(np.abs(values[mask]-source[mask]).mean()),'medianChannelError':np.median(values[mask]-source[mask],axis=0).tolist()})
 thumb=image.resize((256,341),Image.Resampling.LANCZOS);board.paste(thumb,(i*256,25));draw.text((i*256+3,3),matrix,fill='white')
reference=Image.open(P/'master-input.png').convert('RGB').resize((256,341),Image.Resampling.LANCZOS);board.paste(reference,(768,25));draw.text((772,3),'exact input',fill='white');board.crop((0,0,1024,380)).save(D/'matrix-review.png')
report={'rows':rows,'scope':'Frame-zero decode diagnostic with explicit standard YUV matrices. No artistic colour correction, no chosen alternate decoder, no change to prior source or exports. Full non-green interior mask defined from exact input; tiny pose differences still affect errors.'}
(D/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
