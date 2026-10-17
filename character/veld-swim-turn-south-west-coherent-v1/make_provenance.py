"""Record actual source selections and exact generation evidence."""
from pathlib import Path
import hashlib,json
from PIL import Image
H=Path(__file__).resolve().parent
G='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'
sources=[
 ('bare-source-v1.png','bare-source-prompt-v1.txt','exec-dc8645c1-d400-4909-8233-dffb3e1afeac.png','slots1-3 selected at .21;slot0 rejected too straight south'),
 ('near-south-source-v2.png','near-south-source-prompt-v2.txt','exec-b3017c50-c57a-4355-8c35-40bfa0876b6c.png','selected first interior at independent .12 ruler'),
 ('helmet-source-v1.png','helmet-source-prompt-v1.txt','exec-53261ad8-2f10-487a-b6ba-def1c38c9e08.png','slots2-3 selected at .095;slots0-1 rejected front collar/prone camera mismatch'),
 ('helmet-source-v2.png','helmet-source-prompt-v2.txt','exec-2d20a862-c2e0-4e35-86dc-ff1f1670f395.png','slots0-1 selected at .083;slots2-3 omitted because camera stays overhead near west'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for file,prompt,original,status in sources:
 im=Image.open(H/file)
 records.append(dict(file=file,sha256=sha(H/file),dimensions=list(im.size),mode=im.mode,prompt=prompt,promptSha256=sha(H/prompt),builtinOriginal=G+original,status=status))
refs=['selected-endpoint-reference.png','yaw-orientation-guide-v1.png','near-south-orientation-guide-v2.png','helmet-endpoint-reference.png','helmet-camera-guide-v2.png','bare-turn-contact-v1.png']
(H/'source-provenance.json').write_text(json.dumps(dict(method='Built-in imagegen; deterministic extraction, shared material curves and reference-calibrated source rulers',records=records,referenceHashes={f:sha(H/f) for f in refs},guideCaveat='Rotated native sprites are generation camera/yaw guides only, never candidate artwork',installed=False),indent=2)+'\n')
p=H/'source-request-v1.json';s=json.loads(p.read_text());s.update(status='paired_staged_native_checked',selectedSources=[x[0] for x in sources],nativeGate='native-candidate-v1-checks.json',installed=False);p.write_text(json.dumps(s,indent=2)+'\n')
print('4 raw source/prompt records; selected and rejected cells explicit')
