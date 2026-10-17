from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;previous=P/'continuous-video-v2';D=P/'continuous-video-v3-white';D.mkdir(exist_ok=True)
assert not (D/'generation.json').exists(),'Preserve exclusive submission ledger'
source=Image.open(previous/'whole-source-reference.png').convert('RGBA')
plate=Image.new('RGBA',(768,1024),(255,255,255,255));plate.alpha_composite(source,(190,130));plate.convert('RGB').save(D/'master-input.png')
source.save(D/'whole-source-reference.png')
prompt=(previous/'prompt.txt').read_text(encoding='utf-8').replace('unchanged flat bright green background','unchanged flat neutral white background')
assert prompt!=(previous/'prompt.txt').read_text(encoding='utf-8')
(D/'prompt.txt').write_text(prompt,encoding='utf-8')
old=np.array(Image.open(previous/'master-input.png').convert('RGB'));new=np.array(plate.convert('RGB'));mask=Image.new('L',(768,1024));mask.paste(source.getchannel('A'),(190,130));opaque=np.array(mask)==255
assert np.array_equal(old[opaque],new[opaque]),'Opaque artwork changed'
record={'previousTask':'448379855364450','change':'Background conditioning only: pure white instead of pure green. Same complete source RGBA, same placement and motion/colour prompt except background words.','opaqueArtworkPixelsExact':True,'opaquePixelCount':int(opaque.sum()),'inputSHA256':hashlib.sha256((D/'master-input.png').read_bytes()).hexdigest(),'reason':'Both green-backed videos tint cloth purple including frame zero. Explicit standard decode matrices do not restore input colours. Test neutral background conditioning as a different source approach, not another prompt-only repeat.','scope':'One diagnostic paid trial; no automatic retry, stride or final artwork admission.'}
(D/'trial-intent.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
