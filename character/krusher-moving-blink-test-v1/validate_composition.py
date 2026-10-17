from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent;R=P.parent.parent
r=json.loads((P/'verification.json').read_text());errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
eye_mask=np.array(Image.open(P.parent/'krusher-blink-study-v1/eye-mask.png'))>0
for record in r['records']:
    source=R/record['source'];original=np.array(Image.open(source).convert('RGBA'));candidate=np.array(Image.open(P/record['output']).convert('RGBA'));mask=np.zeros((184,184),bool);x,y=record['headPaste']
    if record['blinkClosed']:mask[y:y+28,x:x+23]=eye_mask
    check(hashlib.sha256(source.read_bytes()).hexdigest()==record['sourceSha256'],'input unchanged')
    check(np.array_equal(original[~mask],candidate[~mask]),'outside local eye edit exact')
    check(np.array_equal(original[:,:,3],candidate[:,:,3]),'source alpha exact')
    capture=P/f"review/native/idle-south-{record['index']:02}.png";im=np.array(Image.open(capture).convert('RGBA'));left=im[95:463,100:468];right=im[95:463,580:948]
    render_mask=binary_dilation(np.repeat(np.repeat(mask,2,axis=0),2,axis=1),iterations=2)
    check(np.array_equal(left[~render_mask],right[~render_mask]),'native body/face outside eye filter region exact')
    if record['blinkClosed']:check(bool(np.any(left!=right)),'native blink changes visible pixels')
baseline=json.loads((P/'baseline-manifest.json').read_text())['states'][0];candidate=json.loads((P/'blink-manifest.json').read_text())['states'][0]
check(baseline['frameDurationsMs']==candidate['frameDurationsMs'] and baseline['loop']==candidate['loop'],'source holds/loop unchanged')
check(sum(d for d,record in zip(candidate['frameDurationsMs'],r['records']) if record['blinkClosed'])==84,'84 ms source-aligned blink')
report={'checks':checks,'errors':errors,'scope':'Source and native-rendered body/face outside generated eye edit remain exact; blink readability remains visual review'};(P/'composition-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));raise SystemExit(bool(errors))
