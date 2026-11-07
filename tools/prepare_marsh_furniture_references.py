"""Preserve live furniture pose geometry before matching Marsh's identity."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-furniture-match-v1'
if (BASE/'contract.json').exists():
    raise SystemExit('Furniture references already preserved; do not replace the pre-install contract')
profiles={'bunk':('character/marsh-v2/supplemental/bunk-east/bare',7),'berth':('character/marsh-v2/supplemental/berth-east',6)}
prompts={};contracts={}
for kind,(relative,count) in profiles.items():
    ref=BASE/'references';ref.mkdir(parents=True,exist_ok=True)
    cols=4 if kind=='bunk' else 3;size=(512*cols,544*2);sheet=Image.new('RGBA',size);contact=Image.new('RGB',(256*cols,292*2),'#17212a');draw=ImageDraw.Draw(contact)
    records=[]
    for i in range(count):
        path=ROOT/relative/f'{i:03}.png';im=Image.open(path).convert('RGBA');x=i%cols;y=i//cols
        sheet.alpha_composite(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(x*512+(512-im.width*2)//2,y*544+(544-im.height*2)//2))
        contact.paste(im,(x*256,y*292+18),im);draw.text((x*256+3,y*292+3),kind+' '+str(i),fill='white');records.append({'path':path.relative_to(ROOT).as_posix(),'bounds':im.getbbox()})
    if kind=='bunk':
        im=Image.open(ROOT/relative/'000.png').convert('RGBA');sheet.alpha_composite(im.resize((512,544),Image.Resampling.NEAREST),(1536,544))
    sheet.save(ref/f'{kind}-pose-layout.png');contact.save(ref/f'{kind}-old-contact.png')
    manifest=json.loads((ROOT/relative/'manifest.json').read_text());contracts[kind]={'runtime':relative,'count':count,'canvas':list(im.size),'poses':records,'manifest':manifest}
    positions='exactly EIGHT figures in TWO rows of FOUR; the last figure is an extra standing reference' if kind=='bunk' else 'exactly SIX figures in TWO rows of THREE'
    prompts[kind]=f"Edit FIRST reference transparent pose sheet to match Marsh identity in SECOND reference. Preserve the FIRST sheet's pose geometry, body length, limb positions, pelvis locations and hanging boot position very closely. All poses show the same adult blond clean-shaven android, anatomical right profile facing east; small right temple implant visible. Matte fitted ivory/slate suit with muted sage shoulder caps, graphite gloves and boots; NO helmet, beard, bulky armor or backpack. This is a {kind} boarding sequence from standing through sitting on the edge with hanging legs, leaning back, bringing both boots onto an implied mattress, then fully horizontal resting. Keep the exact pose order and head/foot ends shown, the legs in the seated phase MUST retain the original hanging boot length below the knee. All figures have one anatomical scale, same head size and limb proportions as the standing figure. Draw NO bed, cushion, rail, furniture, props, ground, grid, labels or shadows. Transparent sheet with {positions}, generous transparent gaps and same composition as reference. Crisp painted game sprite finish. Change the costume and facial identity; preserve the mechanics of the poses."
prompts['berth']=prompts['berth'].replace('All poses show the same adult blond clean-shaven android, anatomical right profile facing east; small right temple implant visible.','All poses show the same adult blond clean-shaven android. The top three poses are anatomical right profile facing east with small right temple implant visible. Bottom row retains the reference oblique then front-facing foreshortened mattress-rest views, head toward the top of the sheet and feet toward the bottom. Do NOT turn these into side-on horizontal bodies; preserve the reference projected pelvis and head positions.')
Image.open(ROOT/'character/marsh-v2/frames/bare/idle-east/000.png').resize((736,736),Image.Resampling.NEAREST).save(BASE/'references/east-identity.png')
(BASE/'prompts.json').write_text(json.dumps(prompts,indent=2)+'\n');(BASE/'contract.json').write_text(json.dumps(contracts,indent=2)+'\n')
print('Preserved six berth and seven bunk poses with runtime metadata')
