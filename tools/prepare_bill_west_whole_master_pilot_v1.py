"""Prepare whole pose and original master references; no part fitting or grading."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-west-whole-master-pilot-v1';D.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
refs=[]
for name,relative,role in [('edit-target','character/bill-west-master-head-repair-v1/bare-walk-000-candidate.png','Existing preferred whole West stride000; exact pose/placement target'),('master-reference','character/bill-west-master-head-audit-v1/master-sole-registered.png','Original West whole master uniformly registered H148,p160224'),('east-material-reference','character/bill-east-walk-master-full-v1/frames/000.png','Installed East suit/face material consistency; no facing/pose transfer')]:
 source=R/relative;im=Image.open(source).convert('RGBA')
 if im.size in [(320,320),(352,320)]:
  # Crop only the common transparent margin, preserving the full registered figure.
  im=im.crop((32,0,288,256))
 assert im.size==(256,256)
 out=D/(name+'.png');im.resize((1024,1024),Image.Resampling.NEAREST).save(out)
 refs.append({'path':str(out),'sha256':sha(out),'source':relative,'sourceSha256':sha(source),'role':role})
prompt='''Edit image1, the entire West-facing Bill walking figure, as one coherent sprite. Preserve its exact stride phase, boot positions and angles, hand locations, arm anatomy, slim build, torso width, head angle and placement; keep every part at the same canvas position and scale. Image2 is the original West identity/rendering master, with matching physical height and registered floor. Restore its angular warm bearded face, medium brown hair, textured charcoal matte diamond-quilt suit, fine stitch lines, muted red square patches, practical harness/belt/pouches and worn subdued boot metal. Image3 shows the installed East material finish only: do not copy its facing or stance. The current West face and cloth are too smooth/cartoon-like; make them finely textured and angular like image2, with restrained midtones and a readable warm face. Keep the original pose body and feet fixed, no enlarged shoulders/torso/head, no extra hands, no swapped limbs, no shiny suit, no washed-out grade. One whole figure on exactly the same square transparent canvas; no added shadow, halo, text, checkerboard or props. Reference canvases are1024square with common pivot512,896 and standingH592. Return one whole corrected sprite.'''
(D/'prompt.txt').write_text(prompt,encoding='utf-8');(D/'references.json').write_text(json.dumps(refs,indent=2)+'\n')
print(json.dumps({'references':len(refs),'output':str(D),'wholePose':True}))
