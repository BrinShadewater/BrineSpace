from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
bare=r/'character/james-carry-headcaps-v1';helm=r/'character/james-shared-helmet-runtime-v1';m=json.loads((helm/'manifest.json').read_bytes())
files=[helm/'manifest.json',r/'scripts/grid_canvas.gd',bare/'candidate-manifest.json']
for direction in ['south','west']:
    state=next(s for s in m['states'] if s['id']=='idle-'+direction);ref=state['frameFiles'][0]
    source=r/ref.removeprefix('res://') if ref.startswith('res://') else helm/ref
    master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(source).convert('RGBA'),(128-int(m['pivot'][0]),224-int(m['pivot'][1])))
    master.save(p/(direction+'-standing.png'));master.crop((96,56,160,120)).resize((512,512),Image.Resampling.NEAREST).save(p/(direction+'-helmet-reference.png'));files += [source,p/(direction+'-standing.png'),p/(direction+'-helmet-reference.png')]
for index,name in [(1,'early'),(2,'middle'),(3,'late')]:
    source=bare/'frames'/f'{index:03}.png';Image.open(source).convert('RGBA').crop((96,56,160,120)).resize((512,512),Image.Resampling.NEAREST).save(p/(name+'-target.png'))
    orientation={'early':'mostly front with a SMALL turn toward image LEFT (both eyes visible)','middle':'diagonal front-left halfway between front and left profile','late':'mostly LEFT profile with a slight remaining frontal component'}[name]
    prompt=f'''EDIT TARGET: first square bare head/collar crop of James. SUPPORTING REFERENCES: second and third images are the selected shared engineering diving-helmet standing masters in South and West orientations. Equip target with exactly this same compact matte dark-grey diving helmet, appropriate for target {orientation}. Keep target face/head orientation, head center and neck/collar attachment; never turn to right or copy a different pose. Same helmet shell design, worn metal fittings, restrained muted yellow details, no visor glow/purple or shine. Compact helmet adds only a small consistent rim around this master-sized head, never a giant bubble. Use supplied masters' projected width/height as the common ruler and interpolate orientation naturally; do not grow the head.

Preserve exact crop canvas/framing and all target collar/shoulder/body details. Only replace bare head/hair/forehead-goggles with the shared helmet and its correct face opening. Helmet crown should remain level with the two supplied helmet masters (around12/64 of this crop height), collar stays target at54/64. Shell centered over target neck, no fore-aft displacement, head bob/tilt or stretched face. Genuine transparent alpha, original empty margins. Return ONE square head crop, no text/scene/extra frames or body redesign. Engineering-yellow glyphs/material remain subdued and matte. Match shared helmet silhouette, openings and fittings; avoid an invented angular substitute.'''
    (p/(name+'-prompt.txt')).write_text(prompt+'\n',encoding='utf-8')
    local=files+[source,p/(name+'-target.png'),p/(name+'-prompt.txt'),Path(__file__)]
    (p/(name+'-inputs.json')).write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in local},'bareSource':source.relative_to(r).as_posix(),'crop':[96,56,160,120],'admissionRegion':[102,62,155,110],'selected':False,'scope':'Single shared-helmet projection for paired carried body; full gear/fit/material/cadence review pending.'},indent=2)+'\n',encoding='utf-8')
print('Three64square bare target head crops plus actual selected standing helmet refs; input/prompt hashes frozen.')
