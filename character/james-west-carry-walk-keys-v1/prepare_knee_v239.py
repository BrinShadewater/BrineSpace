from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'knee-material-phase30-v239';out.mkdir(exist_ok=True)
base=p/'lower-material-phase30-v205';master=r/'character/branforth-west-direct-v2/master-input.png'
box=(80,140,176,236)
for role,f,crop in [('edit-target',base/'bare-head-protected.png',box),('master-metal-reference',master,(555,865,675,985))]:
 im=Image.open(f).convert('RGBA').crop(crop);im.resize((1024,1024),Image.Resampling.NEAREST if role=='edit-target' else Image.Resampling.LANCZOS).save(out/f'{role}.png')
prompt='''Edit Image1 only, the fixed lower-body crop of James carrying while walking west in phase30. Image2 is a material sample from the original master, not a pose reference. Change only the surface finish of the small near knee fitting in Image1, centred roughly at image coordinate(400,250), corresponding to original sprite rectangle x108..126,y157..182. Its current pale highlight is too bright against the neighbouring matte warm-gray leg fittings. Reduce the broad pale sheen into detailed worn dull warm silver, retaining subdued small highlights, rivets, seams and the existing charcoal edge. Match Image2's matte illustrated material. Preserve the exact knee shape, location, diagonal orientation, calf connection, overlapping legs, straps, boot contours, toe/heel/sole placement and every original landmark. Recolour the existing fitting only; no movement, reshaping, new hardware, dark shadow masses, purple/magenta, gold additions or smoothing away construction detail. All other surfaces stay unchanged. Return the same1024x1024 transparent crop, with identical framing and scale. No background, text, glow or pixel-art conversion.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
files=[base/'bare-head-protected.png',base/'helmet-head-protected.png',master]
refs=[out/'edit-target.png',out/'master-metal-reference.png']
(out/'inputs.json').write_text(json.dumps(dict(phase=30,baseFolder=base.relative_to(r).as_posix(),cropBox=box,admissionRectangle=[108,157,127,183],sourceSha256={f.relative_to(r).as_posix():sha(f) for f in files},referenceSha256={f.relative_to(r).as_posix():sha(f) for f in refs},promptSha256=sha(out/'prompt.txt'),normalChanged=False),indent=2)+'\n',encoding='utf-8')
print('Prepared phase30 knee finish with fixed anatomical registration.')
