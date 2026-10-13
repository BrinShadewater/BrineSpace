"""Preserve pose geometry and identity references for the generic rest repair."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-rest-match-v1'
BARE=ROOT/'character/marsh-v2/frames/bare'
prompts={}
board=Image.new('RGB',(736,4*420),'#17212a');draw=ImageDraw.Draw(board)
for row,d in enumerate(('south','north','east','west')):
    folder=BASE/'references';folder.mkdir(parents=True,exist_ok=True)
    paths=[BARE/f'lie-down-{d}/{i:03}.png' for i in range(4)]
    paths += [BARE/f'sleep-{d}/001.png', BARE/f'get-up-{d}/001.png',BARE/f'get-up-{d}/002.png',BARE/f'idle-{d}/000.png']
    layout=Image.new('RGBA',(1792,896))
    for i,path in enumerate(paths):
        im=Image.open(path).convert('RGBA')
        layout.alpha_composite(im.resize((368,368),Image.Resampling.NEAREST),(i%4*448+40,i//4*448+40))
        board.paste(im,(i%4*184,row*420+i//4*200+20),im)
    draw.text((4,row*420+402),d+' / current generic rest',fill='white')
    layout.save(folder/f'{d}-pose-layout.png')
    Image.open(BARE/f'idle-{d}/000.png').resize((736,736),Image.Resampling.NEAREST).save(folder/f'{d}-identity.png')
    facing={'south':'south, viewed from the front','north':'north, viewed from behind','east':'east, viewed from his anatomical right; show the small right temple implant','west':'west, viewed from his anatomical left; the far-side temple implant is hidden'}[d]
    prompts[d]=f"Edit FIRST reference transparent sprite layout into an eight-pose Marsh lying-down, sleeping and getting-up animation sheet. Match character identity and fitted suit in SECOND reference: blond clean-shaven adult android, matte ivory/slate fitted suit, muted sage shoulder caps, graphite gloves and boots, no beard, helmet, bulky armor or backpack. All figures face {facing}. Preserve each reference pose's silhouette, orientation, body length and limb placement very closely. TOP ROW: standing idle, lowering toward rest, leaning back supported by one hand, fully horizontal resting body. BOTTOM ROW: the SAME horizontal rest pose with only subtle breath variation, rising to an elbow/hand, halfway upright with bent knees, standing idle. The two horizontal poses must have matching head, hip, boot and hand positions apart from tiny breathing; keep the reference head and foot ends, do not turn onto another side. These are weight-bearing poses on an implied surface, but draw NO furniture, bed, cushion, props or floor. Preserve one anatomical scale through every pose; lying body length matches standing body height. Exactly FOUR separately spaced figures per row, TWO rows, same composition as layout, transparent gaps, no labels, no grid, no shadows, completely transparent background. Crisp hand-painted game sprite finish, same palette and facial identity in every pose."
board.save(BASE/'references/current-rest-contact.png')
(BASE/'prompts.json').write_text(json.dumps(prompts,indent=2)+'\n')
print('Prepared four rest geometry and identity references')
