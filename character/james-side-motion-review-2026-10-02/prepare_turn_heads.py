from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parent; R=P.parents[1]
spec=[('james-cargo-turn-east-north-v1','carry-turn-east-north',i) for i in range(3)]+[('james-cargo-turn-east-south-height-v3','carry-turn-east-south',i) for i in range(1,4)]
target=Image.new('RGBA',(768,512));records=[]
for n,(bank,key,i) in enumerate(spec):
    path=R/'character'/bank/'bare-manifest.json';pack=json.loads(path.read_bytes());s=next(s for s in pack['states'] if s['id']==key);file=path.parent/s['frameFiles'][i]
    crop=Image.open(file).convert('RGBA').crop((110,61,174,125)).resize((256,256),Image.Resampling.NEAREST);target.alpha_composite(crop,((n%3)*256,(n//3)*256))
    records.append({'cell':n,'state':key,'index':i,'source':file.relative_to(R).as_posix(),'crop':[110,61,64,64]})
target.save(P/'turn-head-target.png')
master=Image.new('RGBA',(768,256));manifest=R/'character/crew-runtime-matte-v1/branforth/manifest.json';pack=json.loads(manifest.read_bytes())
for n,direction in enumerate(['east','north','south']):
    s=next(s for s in pack['states'] if s['id']=='idle-'+direction);im=Image.open(manifest.parent/s['frameFiles'][0]).convert('RGBA');master.alpha_composite(im.crop((60,10,124,74)).resize((256,256),Image.Resampling.NEAREST),(n*256,0))
master.save(P/'turn-head-masters.png')
(P/'turn-head-layout.json').write_text(json.dumps(records,indent=2))
prompt='''Edit image1, a transparent 3-column 2-row sheet of six James head/collar closeups. Image2 contains the identity masters in East, North, South order. Image3 is the already revised East head size/identity reference. Preserve image1 exact six cell grid, individual orientation, neck base/collar anchors and pixel-art rendering. Correct only cranial/cheek size and identity: compact master-matching grey-haired middle-aged engineer, yellow goggles resting on forehead, matte warm neutral skin, charcoal collar, no purple cast, no extra shine. Reduce the oversized head width about15-20 percent and height about8-10 percent while keeping neck attachment fixed. Top row: East profile, turning away toward North slightly, turning away toward North more. Bottom row: turning toward South slightly, turning toward South more, near-frontal South three-quarter. Each pose keeps its existing distinct yaw; do not make all faces face East, do not mirror equipment. Preserve coherent eye line across turn, brow/goggles size and short grey hair. Do not modify collar/shoulder suit, add torso, add limbs, alter background, or introduce halo/haze. Keep transparent background. Deliver this same 3x2 six-cell sheet, equal cells, no labels, guides or extra cells. This is a source for six separate head cutouts, so avoid overlarge hair silhouettes and detached necks.'''
(P/'turn-head-prompt.txt').write_text(prompt)
print('Six turn head closeups and three directional master references retained.')
