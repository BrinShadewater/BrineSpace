from pathlib import Path
import shutil,json,hashlib
P=Path(__file__).resolve().parent;old=P/'continuous-video-v1';new=P/'continuous-video-v2'
new.mkdir(exist_ok=True)
assert not (new/'generation.json').exists(),'Never replace an exclusive submission ledger'
for name in ['master-input.png','whole-source-reference.png','input-record.json']:
 shutil.copyfile(old/name,new/name)
prompt=(old/'prompt.txt').read_text(encoding='utf-8')
prompt=prompt.replace('Stable diffuse matte lighting and colours throughout.','The suit MUST retain the reference image neutral charcoal-grey with subtle muted olive-grey cloth undertones. Skin remains warm tan; hair remains matte brown. Preserve the exact reference hue and saturation during every step. No purple, plum, lavender, magenta, violet or blue tint in the cloth, no cinematic colour grading, no coloured lighting or material recolouring. The blue department patch remains blue, the silver hardware remains neutral silver. Stable diffuse matte lighting and colours throughout.')
(new/'prompt.txt').write_text(prompt,encoding='utf-8')
record={'failureTarget':'V1 all-frame stable material shifted suit toward purple compared with unchanged original-guided input and true East masters. New trial changes grade preservation wording only; same exact input and motion instructions.','previousTask':'448373312799191','inputSHA256':hashlib.sha256((new/'master-input.png').read_bytes()).hexdigest(),'sourceImageUnchanged':(new/'master-input.png').read_bytes()==(old/'master-input.png').read_bytes(),'scope':'One new scoped source trial; no automatic paid retries or normal runtime changes.'}
(new/'trial-intent.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
