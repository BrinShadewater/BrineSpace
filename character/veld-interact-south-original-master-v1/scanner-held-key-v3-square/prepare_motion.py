from pathlib import Path
from PIL import Image
import json,hashlib,shutil
K=Path(__file__).resolve().parent;R=K.parents[2];V=K.parent
review=json.loads((K/'KEY_REVIEW.json').read_bytes())
assert all(review['key'][k]==review['master'][k] for k in ['height','top','floor','headWidth','headAxis'])
held=Image.open(K/'native-held-key.png').convert('RGBA').resize((768,768),Image.Resampling.NEAREST)
bg=Image.new('RGB',(768,768),(12,18,24));bg.paste(held,(0,0),held);bg.save(K/'held-input.png')
prompts={
'draw-video-v1':'Fixed camera, front-facing full-body game character. One continuous scanner DRAW: start at the first relaxed standing image, use the gloved hand on IMAGE RIGHT to draw the small scanner from the vertical pouch at that same image-right hip, then bring it to upper abdomen and support it with the other hand. Finish exactly in the supplied scanner-held last image. The image-left three pale cylinders stay untouched. Only arms/hands and scanner move; head stays at its original upright angle, feet and body stance remain planted. Preserve the exact warm skin, brown hair with grey streak, matte charcoal quilted suit, blue patches, head size, height and proportions. Small scanner has constant dim matte grey-blue screen, no glow or flashing. Hands stay attached to original sleeves. No repeated action, head bow, turning, walking, scaling, zoom or camera movement. Flat dark background RGB12,18,24.',
'stow-video-v1':'Fixed camera, front-facing full-body game character. One continuous scanner STOW: start at the supplied two-handed scanner-held first image, lower the small scanner and put it back into the vertical pouch at IMAGE RIGHT hip with the gloved hand on that same image-right side. Release it, lower both hands, and finish exactly in the supplied relaxed standing last image. The image-left three pale cylinders stay untouched. Only arms/hands and scanner move; head stays at its original upright angle, feet and body stance stay planted. Preserve the exact warm skin, brown hair with grey streak, matte charcoal quilted suit, blue patches, head size, height and proportions. Small scanner screen stays constant dim matte grey-blue, no glow or flashing. Hands attach to original sleeves. No repeated action, new tool, head bow, turning, walking, scaling, zoom or camera movement. Flat dark background RGB12,18,24.'}
for name,prompt in prompts.items():
    P=K/name;P.mkdir(exist_ok=True);assert not (P/'generation.json').exists()
    draw=name.startswith('draw')
    first=V/'master-input.png' if draw else K/'held-input.png'
    last=K/'held-input.png' if draw else V/'master-input.png'
    shutil.copyfile(first,P/'master-input.png');shutil.copyfile(last,P/'last-input.png')
    shutil.copyfile(V/'original-idle-master.png',P/'original-idle-master.png')
    shutil.copyfile(V/'original-idle-master.png' if draw else K/'native-held-key.png',P/'prepared-idle-master.png')
    (P/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
    files=[P/'master-input.png',P/'last-input.png',P/'prompt.txt',K/'native-held-key.png',K/'KEY_REVIEW.json']
    (P/'INPUTS.json').write_text(json.dumps(dict(method='Complete source motion between original rest and whole authored scanner-held key with matching fixed-canvas ruler. No local edits or cut middle.',phase='draw' if draw else 'stow',registration=dict(scale=1/3,offset=[0,0]),estimatedUSD=.28,billingVerified=False,bindings={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}),indent=2)+'\n',encoding='utf-8')
    source=(V/'review_source.py').read_text(encoding='utf-8').replace('R=P.parents[1]','R=P.parents[3]').replace('res://character/veld-interact-south-original-master-v1/frames/',f'res://character/veld-interact-south-original-master-v1/scanner-held-key-v3-square/{name}/frames/').replace('source-interact-south','source-'+('draw' if draw else 'stow')+'-south')
    (P/'review_source.py').write_text(source,encoding='utf-8')
print('Two complete scanner phase sources prepared, matching original/held endpoints.')
