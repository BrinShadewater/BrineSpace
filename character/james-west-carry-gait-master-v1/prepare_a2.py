from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
prompt=(p/'contact-b-prompt.txt').read_text(encoding='utf-8').replace('reaches BACKWARD to image RIGHT','reaches FORWARD to image LEFT').replace('reaches FORWARD to image LEFT. Keep hip','reaches BACKWARD to image RIGHT. Keep hip').replace('Far forward heel','Near forward heel').replace('near rear toe','far rear toe').replace('Far forward sole center','Near forward sole center').replace('gold-seamed near shin must angle diagonally back toward image RIGHT; unseamed far shin advances image LEFT','gold-seamed near shin must angle diagonally FORWARD toward image LEFT; unseamed far shin goes BACKWARD toward image RIGHT')
prompt+='\nIMAGE 3 shows the PREVIOUS rejected ordering (gold-seamed shin trailing on the RIGHT). Your new ordering must differ: gold-seamed shin crossing forward toward the LEFT boot, plain far shin trailing to RIGHT. Do not copy IMAGE 3 leg ordering. Keep the top knee identities and seam continuous.\n'
(p/'contact-a2-prompt.txt').write_text(prompt,encoding='utf-8')
Image.open(p/'contact-a-native-crop.png').resize((704,704),Image.Resampling.LANCZOS).save(p/'ordering-reference.png')
inputs=json.loads((p/'contact-a-inputs.json').read_bytes());files=[p/'legs-target.png',p/'whole-reference.png',p/'ordering-reference.png',p/'base.png',p/'contact-a2-prompt.txt',Path(__file__)]
inputs['preCallSha256']={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(p/'contact-a2-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8')
(p/'package_a2.py').write_text((p/'package_contact.py').read_text().replace('contact-a','contact-a2').replace('contact A draft','contact A2 draft'),encoding='utf-8')
print('Explicit seam-owned leading-leg correction prepared.')
