"""Publish current-source native evidence and fixed station comparisons."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];O=R/'output/bill-east-master-world-v5';P=R/'character/bill-east-reach-adjacent-motion-v2';N=P/'native';N.mkdir(exist_ok=False)
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));d=json.loads((O/'report.json').read_text(encoding='utf-8'))
assert v['passed'] and not d['interactionContactFindings'] and len(d['samples'])==150 and len(d['captures'])==36
for name in ['validation.json','report.json','inputs-before.json','inputs-after.json']:shutil.copyfile(O/name,N/name)
shutil.copyfile(P/'family-review.json',N/'family-review-native-input.json')
for c in d['captures']:
 for key in ['sourceFile','worldFile']:shutil.copyfile(O/c[key],N/c[key])
for page in range(3):
 board=Image.new('RGB',(1680,610),'#17252d');draw=ImageDraw.Draw(board);draw.text((15,12),['Idle before action','Interaction','Idle return'][page]+' - fixed station crop, candidate above / selected below',fill='white')
 for n,c in enumerate(d['captures'][page*12:page*12+12]):
  crop=Image.open(N/c['worldFile']).crop((495,170,635,305)).resize((280,270),Image.Resampling.NEAREST);col=n//2;row=n%2;board.paste(crop,(col*280,45+row*280));draw.text((col*280+6,31+row*280),f"slot {c['slot']} {c['variant']}",fill='white')
 board.save(N/f'world-review-{page}.png')
proof=dict(sourceSoleDepthAccepted=True,nativePagesReviewed=False,scope='150 prescribed paused samples in actual furnished-room bare renderer, explicit current-source table binding. Six occupied-height checks match inspected source. Strict Ysole depth only; not 2D planted feet, natural chooser, continuous cadence, equipment, fullSave/TitleContinue or normal admission.',pages=[f'native/world-review-{i}.png' for i in range(3)],sourceInputSha256=hashlib.sha256((N/'family-review-native-input.json').read_bytes()).hexdigest(),normalAdmission=False)
(N/'verification.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
print('Published36native/source capture pairs and3fixed-crop pages for V5 current-source interval.')
