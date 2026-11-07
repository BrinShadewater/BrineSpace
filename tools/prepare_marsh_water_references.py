"""Preserve swim/tread/start geometry and metadata for Marsh's water identity pass."""
from pathlib import Path
import json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-water-match-v1';BARE=ROOT/'character/marsh-v2/frames/bare'
if (BASE/'contract.json').exists():raise SystemExit('Water references already preserved')
BASE.mkdir(parents=True,exist_ok=True);ref=BASE/'references';ref.mkdir(exist_ok=True)
cat=json.loads((ROOT/'character/marsh-v2/catalog.json').read_text());states={};packs={}
for relative in cat['body']:
    path=ROOT/'character/marsh-v2'/relative;pack=json.loads(path.read_text());packs[path.relative_to(ROOT).as_posix()]=pack
    for s in pack['states']:
        if s['id'].startswith(('swim-','tread-')) and not s['id'].startswith(('swim-carry','swim-pickup','swim-distress')):
            states[s['id']]={'manifest':path.relative_to(ROOT).as_posix(),'metadata':s,'files':[(path.parent/f).relative_to(ROOT).as_posix() for f in s['frameFiles']],'canvas':[pack['frameWidth'],pack['frameHeight']]}
prompts={}
for d in ('south','north','east','west'):
    paths=[BARE/f'swim-{d}/{i:03}.png' for i in range(4)]+[BARE/f'tread-{d}/{i:03}.png' for i in range(4)]
    paths += [ROOT/states['swim-start-'+d]['files'][i] for i in (1,2,3)]+[BARE/f'idle-{d}/000.png']
    sheet=Image.new('RGBA',(2688,896))
    for i,path in enumerate(paths):
        im=Image.open(path).convert('RGBA');sheet.alpha_composite(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(i%6*448+40,i//6*448+20))
    sheet.save(ref/f'{d}-pose-layout.png');Image.open(BARE/f'idle-{d}/000.png').resize((736,736),Image.Resampling.NEAREST).save(ref/f'{d}-identity.png')
    view={'south':'south/front; face visible','north':'north/rear; back of head visible','east':'east/right profile; small anatomical-right temple implant visible','west':'west/left profile; temple implant hidden on far side'}[d]
    prompts[d]=f"Edit FIRST transparent pose sheet to match Marsh identity in SECOND reference. Exactly TWELVE separately spaced figures in TWO rows of SIX. All face {view}. Blond clean-shaven adult android in matte fitted ivory/slate suit, muted sage shoulder caps, graphite gloves and boots, no beard, helmet, bulky armor or backpack. Preserve the FIRST sheet's pose geometry, projected body length, limb positions, orientation and camera very closely. TOP row figures 1-4: FOUR streamlined swimming poses, subtle coordinated alternating kick and reaching arm motion. Top row figures 5-6: first TWO upright treading-water poses, arms gently sculling with bent knees. BOTTOM row figures 1-2: other TWO treading poses completing the loop. Bottom row figures 3-5: THREE swim-start interior poses tilting from upright tread toward horizontal swim. Bottom row figure 6: standing reference for anatomical scale. This is a continuous coherent swim/tread/launch set, same head size and limb length in every pose. Preserve reference head ends, hand positions and individual pose placement; NEVER mirror the equipment or turn to the opposite direction. No water, bubbles, cargo, props, floor, shadows, text or grid; completely transparent background and generous transparent gaps. Crisp painted game sprite detail with consistent clean-shaven identity and suit."
(BASE/'prompts.json').write_text(json.dumps(prompts,indent=2)+'\n');(BASE/'contract.json').write_text(json.dumps({'states':states,'packs':packs},indent=2)+'\n');print('Prepared four water pose sheets and immutable runtime contracts')
