from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
p=Path(__file__).resolve().parent;o=p/'north-unload-coherent-motion-v329'
report=json.loads((o/'source-review.json').read_bytes())
bright=[]
for i in range(report['frameCount']):
    a=np.array(Image.open(o/f'frames/bare/{i:03}.png').convert('RGBA'))
    roi=a[100:215,138:151];rgb=roi[:,:,:3].astype(int)
    mask=(roi[:,:,3]>200)&(rgb.min(2)>=210)&((rgb.max(2)-rgb.min(2))<=35)
    bright.append(int(mask.sum()))
board=Image.new('RGB',(1536,540),(48,59,64));d=ImageDraw.Draw(board)
items=[(Image.open(o/'first-alpha-control.png'),'First input')]
items += [(Image.open(o/f'frames/bare/{i:03}.png'),f'Source {i} bright{bright[i]}') for i in [35,62,85,110]]
items += [(Image.open(o/'last-alpha-control.png'),'Last input')]
for j,(im,label) in enumerate(items):
    crop=im.convert('RGBA').crop((88,64,168,232)).resize((240,504),Image.Resampling.NEAREST)
    board.paste(crop,(j*256+8,28),crop);d.text((j*256+8,5),label,fill='white')
board.save(o/'material-and-bend-diagnosis.png')
diagnosis=dict(brightAchromaticPixelROI=[138,100,151,215],threshold='opaque,minRGB>=210,max-min<=35',brightCounts=bright,firstCount=bright[0],maxCount=max(bright),peakFrame=bright.index(max(bright)),status='not_selected_source_fidelity_failed',
    observed=['belt wrench turns bright near-white during bend and returns to muted grey on exit','body compresses deeply; lowest crown130 vs input75','case becomes visible on rise, and broad endpoint prop remains unaccepted'],
    next='Do not install or blanket regrade. Use an authored shallow bend reference with muted belt-tool material and consistent case geometry to constrain the next temporal source; retain all current source evidence.')
(o/'visual-diagnosis-v330.json').write_text(json.dumps(diagnosis,indent=2)+'\n')
print(json.dumps({k:diagnosis[k] for k in ['firstCount','maxCount','peakFrame','status']}))
