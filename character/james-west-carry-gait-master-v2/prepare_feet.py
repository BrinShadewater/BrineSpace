from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
for phase,delta in [('near',3),('far',1)]:
    name='contact-'+phase;source=p/(name+'.png');im=Image.open(source).convert('RGBA');target=p/(name+'-feet-target.png');im.crop((88,176,168,256)).resize((640,640),Image.Resampling.LANCZOS).save(target)
    prompt=f'''Edit only this fixed80x80-native square lower-shin/boot crop enlarged8x. Preserve framing, margins, two-leg pose and original costume ownership. This source is a left-facing heavy-cargo walking contact. The visible soles currently finish {delta} native pixels ABOVE the correct ground line. Correct lower shin/ankle anatomy and lower BOTH boots by precisely {delta} native pixels ({delta*8} enlarged pixels) so forward heel and rear toe contact finish at native y224, crop y48/enlarged y384. Keep upper shins/knees above native y197 (crop y21) exactly unchanged. Extend the ankle/lower-shin attachment naturally to the lowered boot positions, preserve boot proportions and intact ankles. Do not resize/shift whole crop, change thigh/knee/leg ordering, swap gold seam, invent a third foot or a shadow to fake height. Preserve forward heel flat and rear heel slightly raised, both soles on y224. No boot pixels below y224. Keep same muted neutral matte graphite and dull worn silver fittings; no shine, purple, new black cavity, bright outline or background. Genuine alpha transparency. Return original full square crop, with all empty margins preserved.'''
    (p/(name+'-feet-prompt.txt')).write_text(prompt+'\n',encoding='utf-8')
    files=[source,target,p/(name+'-feet-prompt.txt'),Path(__file__)]
    (p/(name+'-feet-inputs.json')).write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':[88,176,168,256],'admissionRegion':[88,197,168,224],'delta':delta},indent=2)+'\n',encoding='utf-8')
print('Two fixed-density boot/ankle repairs prepared from actual measured sole deficits.')
