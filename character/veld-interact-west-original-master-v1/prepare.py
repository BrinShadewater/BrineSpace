from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
specs={'master':R/'character/veld-side-foundation-v1/west-standing.png','motion':R/'character/veld-action-west-matched-v1/frames/interact-west/002.png'}
records={}
for role,source in specs.items():
 im=Image.open(source).convert('RGBA');assert im.size==(184,184)
 plate=Image.new('RGBA',(256,256));plate.paste(im,(36,52))
 plate.save(P/(role+'-native.png'));plate.resize((768,768),Image.Resampling.NEAREST).save(P/(role+'-input.png'))
 records[role]={'source':str(source.relative_to(R)).replace('\\','/'),'SHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'paddingOnly':[36,52],'inputScale':3,'inputSHA256':hashlib.sha256((P/(role+'-input.png')).read_bytes()).hexdigest()}
prompt='''Edit the FIRST image, the original West-facing Veld master, into ONE standing scanner-interaction key pose. The SECOND image provides ONLY arm/hand/scanner pose, never appearance. Preserve the first image's exact whole framing, small head, face, dark brown bun, matte warm skin, original neutral charcoal suit, shoulder patch, detailed chest/belt equipment, gloves, boots, waist, leg stance and ground contacts. Keep the entire head, torso and legs unchanged in appearance and placement; only articulate both arms naturally forward to hold the little cyan-lit scientific scanner at lower chest height, following the second image's hand action. Show anatomically connected shoulders and continuous sleeves with the original sleeve material and badge; no floating hands, doubled arms or cut seams. Strict west profile facing left, same original perspective, no turn toward camera. Do not adopt the second image's cool blue-grey smooth suit, larger head, simplified panels or changed equipment. Retain the FIRST image's coarse detailed pixel-art texture without adding glossy highlights, glow, white rim, blue cast or blurry repainting. Scanner light is a small cyan screen, not light spilling onto skin or suit. Full figure on the same square transparent canvas: same head top, head axis, boot floor, body height and width as first image. Do not enlarge, recenter, raise feet, crop or invent a new silhouette. Return ONE complete sprite only, no sheet, guides, text, shadow or background.'''
(P/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
(P/'INPUTS.json').write_text(json.dumps(records,indent=2)+'\n')
print('2 whole references prepared; original scale/colour unchanged')
