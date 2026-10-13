"""Prepare complete remaining phase targets, retaining selected motion/identity refs."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
slots=[s for s in range(48) if s not in [0,12,24,36]]
for slot in slots:
    D=P/f'sequence-individual-{slot:03}-v1';D.mkdir(exist_ok=False)
    target=R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png'
    Image.open(target).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(D/'edit-target.png')
    refs=[dict(source=str(target),sourceSha256=sha(target),path=str(D/'edit-target.png'),sha256=sha(D/'edit-target.png'),role=f'Only edit target: exact complete gait phase {slot} of48')]
    for src,name,role in [(P/'stride-000-v1/raw-000.png','preferred-walk-reference.png','Preferred whole walking identity/material continuity, not replacement pose'),(P/'original-master.png','original-master.png','Original master identity/material authority, not replacement pose')]:
        shutil.copyfile(src,D/name);refs.append(dict(source=str(src),sourceSha256=sha(src),path=str(D/name),sha256=sha(D/name),role=role))
    prompt=f'''Edit only image1, the exact complete Bill walking phase {slot} of48. Preserve image1's precise arm and leg articulation, foot positions, body proportions, width, crown and sole heights, head size, camera and transparent square canvas placement. Image2 supplies the preferred detailed walking rendering and identity; image3 is the original Bill master authority. Use exactly the same warm angular face, brown hair/beard, small head, collar, fine MATTE charcoal quilt stitching, restrained worn metal, square/ring insignia and burgundy accents as these references. Match the preferred walking face, suit color and matte finish, not brighter/glossier armor or a black face. No pose copying from the references. Do not enlarge the body or boots, raise the head/neck, move feet or change stride. One connected complete figure, transparent background with clean alpha and no background halo or shadow. Whole figure design/material fidelity repair only; original gait geometry stays unchanged.'''
    (D/'prompt.txt').write_text(prompt,encoding='utf-8');(D/'references.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8')
(P/'remaining-source-plan-v1.json').write_text(json.dumps(dict(slots=slots,total=48,prepared=len(slots),normalAdmission=False,method='One whole-source edit per original phase, same fixed master/walking continuity refs. No partial installation.'),indent=2)+'\n',encoding='utf-8')
print('Prepared all44 remaining exact whole gait targets; no selected sources changed.')
