from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
prompt=(p/'contact-a-prompt.txt').read_text(encoding='utf-8').replace('near leg reaches forward to image LEFT, far leg reaches backward to image RIGHT','near leg (the image RIGHT knee with gold trouser seam) reaches BACKWARD to image RIGHT; far leg (the image LEFT knee) reaches FORWARD to image LEFT').replace('Near forward heel touches','Far forward heel touches').replace('far rear toe touches','near rear toe touches').replace('Near sole center approx native x112 (crop x24), far toe approx x151 (crop x63)','Far forward sole center approx native x112 (crop x24), near rear toe approx x151 (crop x63)')
prompt+='\nThis is the OPPOSITE contact phase. Preserve clothing handedness: the gold-seamed near shin must angle diagonally back toward image RIGHT; unseamed far shin advances image LEFT. Independently redraw anatomy; never mirror the crop or swap tool sides.\n'
(p/'contact-b-prompt.txt').write_text(prompt,encoding='utf-8')
files=[p/'base.png',p/'legs-target.png',p/'whole-reference.png',p/'contact-b-prompt.txt',Path(__file__)]
inputs=json.loads((p/'contact-a-inputs.json').read_bytes());inputs['preCallSha256']={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(p/'contact-b-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8')
source=(p/'package_contact.py').read_text().replace('contact-a','contact-b').replace('contact A draft','contact B draft');(p/'package_b.py').write_text(source,encoding='utf-8')
print('Opposite anatomical contact prepared; same original crop target, no mirroring.')
