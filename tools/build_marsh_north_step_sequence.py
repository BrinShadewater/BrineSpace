"""Assemble whole authored North step sources with explicit support registration."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-step-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    paths=['character/marsh-v2/frames/bare/idle-north/000.png','character/marsh-north-step-v1/candidate-04/001.png','character/marsh-north-step-v1/candidate-04/002.png','character/marsh-north-step-v1/candidate-08/001.png','character/marsh-north-step-v1/candidate-09/000.png','character/marsh-north-step-v1/candidate-09/001.png','character/marsh-v2/frames/bare/idle-north/000.png']
    polish='--polish' in sys.argv
    shifts=[(0,0),(0,0),(0,0),(0,0),(5,-13),(4 if polish else 5,-6),(0,0)]
    starts=[0,0,0,0,0,7,13];frames=[];sources=[]
    output=BASE/('sequence-v2' if polish else 'sequence-v1');output.mkdir(exist_ok=True)
    for i,(path,offset) in enumerate(zip(paths,shifts)):
        source=Image.open(ROOT/path).convert('RGBA');frame=Image.new('RGBA',(184,184));frame.alpha_composite(source,offset)
        assert np.count_nonzero(np.array(source)[:,:,3])==np.count_nonzero(np.array(frame)[:,:,3]),'whole figure must remain unclipped'
        frame.save(output/('%03d.png'%i));frames.append(frame)
        sources.append({'slot':i,'wholeSource':path,'sourceSha256':sha(ROOT/path),'integerTranslation':offset,'rootDenseAtHoldStart':starts[i],'frameSha256':sha(output/('%03d.png'%i))})
    manifest={'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'states':[{'id':'walk-step-north','frameFiles':['%03d.png'%i for i in range(7)],'frameDurationsMs':[120]*7,'loop':False,'facings':['north']*7,'waterKinds':['walk']*7,'waterPoses':[False]*7,'depthOffsets':[0.0]*7}]}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    recipe={'status':'unselected contact-aware sequence study; world motion/safety/Continue acceptance pending','normalAdmission':False,'sources':sources,'authoredDenseLength':13,'nominalWorldLength':13*65.28/148,'durationsMs':[120]*7,'grade':'none','limits':'Only whole-source integer registration. Root interpolates7dense pixels in.48–.60 and6 in.60–.72. Within-held-pose whole-sprite offset cancels root progression; feet/torso source pixels never warped. Final neutral stance changes support to right foot; lateral settlement still requires visual review.'}
    if polish:recipe['polish']='Closing whole figure registered one pixel left; measured planted-left centroid now matches landing. Transfer half-pixel sole-centroid quantization remains. V1 preserved.'
    (output/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    board=Image.new('RGB',(184*7,260),'#293b40');draw=ImageDraw.Draw(board)
    for i,frame in enumerate(frames):
        # Contact-space comparison includes the root at that source hold start.
        board.paste(frame,(184*i,45-starts[i]),frame);draw.text((184*i+4,5),'Slot%d root%d'%(i,starts[i]),fill='white')
        draw.line((184*i,45+157,(i+1)*184-1,45+157),fill='#639f92')
    board.save(output/'contact-comparison.png');print('Seven whole poses;13dense/5.734world units; no scale/grade change')
if __name__=='__main__':main()
