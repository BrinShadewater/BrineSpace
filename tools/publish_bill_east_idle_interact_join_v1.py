from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];O=R/'output/bill-east-master-world-v3';P=R/'character/bill-east-idle-interact-joined-v1';N=P/'native';N.mkdir(exist_ok=False)
v=json.loads((O/'validation.json').read_text());d=json.loads((O/'report.json').read_text());assert v['passed'] and not d['interactionContactFindings'];assert len(d['samples'])==150 and len(d['captures'])==36
for name in ['validation.json','report.json','inputs-before.json','inputs-after.json']:shutil.copyfile(O/name,N/name)
shutil.copyfile(P/'join-review.json',N/'join-review-native-input.json')
for c in d['captures']:
 for key in ['sourceFile','worldFile']:shutil.copyfile(O/c[key],N/c[key])
for page in range(3):
 board=Image.new('RGB',(1680,610),'#17252d');draw=ImageDraw.Draw(board);draw.text((15,12),['Idle before action','Interaction','Idle return'][page]+' — fixed station crop, candidate above / selected below',fill='white')
 captures=d['captures'][page*12:page*12+12]
 for n,c in enumerate(captures):
  crop=Image.open(N/c['worldFile']).crop((495,170,635,305)).resize((280,270),Image.Resampling.NEAREST);col=n//2;row=n%2;board.paste(crop,(col*280,45+row*280));draw.text((col*280+6,31+row*280),f"slot {c['slot']} {c['variant']}",fill='white')
 board.save(N/f'world-review-{page}.png')
pages=['native/world-review-'+str(i)+'.png' for i in range(3)];proof={'sourceSoleDepthAccepted':True,'scope':'150 prescribed samples, actual normal bare room renderer candidate table binding; same root/same clock comparisons, main pause guard. Strict Y sole depth matches selected all 72 idle +6 interact +72 return. Does not certify 2D planted foot anatomy, natural actor dispatch, continuous cadence, fullSave/TitleContinue or normal admission.','nativePagesReviewed':False,'pages':pages,'sourceInputSha256':hashlib.sha256((N/'join-review-native-input.json').read_bytes()).hexdigest()};(N/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print('Published 36 actual room/source captures, 150 samples and three fixed crop boards. Source depth findings: zero.')
