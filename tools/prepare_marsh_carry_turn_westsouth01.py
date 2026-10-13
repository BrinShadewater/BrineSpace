"""Freeze own West-to-South yaw without swapping guide or anatomical sides."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-carry-turn-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
g=json.loads((S/'guide-provenance.json').read_text());pair='west-south'
text=(S/'east-south-01.prompt.txt').read_text().replace('EAST/right-facing side','WEST/left-facing side').replace('East','West')
text=text.replace('LEFT West facing RIGHT','LEFT West facing LEFT').replace('RIGHT temple implant visible on viewerLEFT near frontal','RIGHT temple implant initially hidden on the FAR side in West and appearing only as face nears South frontal on viewerLEFT')
text=text.replace('mostly faces RIGHT','mostly faces LEFT').replace('FRONT-RIGHT','FRONT-LEFT').replace('diagonally RIGHT','diagonally LEFT').replace('head slightly RIGHT','head slightly LEFT').replace('West RIGHT side','West LEFT side').replace('never West/left-facing or rear view','never East/right-facing or rear view')
text=text.replace('Preserve original visible temple implant and authentic ankle hardware','Preserve BARE visible temple in West-side poses; original right temple implant is hidden far-side early and gradually emerges near frontal on viewerLEFT. Preserve authentic ankle hardware,never mirror East')
text+='\nWest endpoint begins with its own near/actorLEFT supporting leg; South endpoint supports actorRIGHT boot on viewerLEFT. Transfer weight naturally through these whole yaw poses to approach the exact South endpoint,not a mirrored East foot pose. Same rigid crate rotates with body and connected supporting hands.\n'
p=S/f'{pair}-01.prompt.txt';assert not p.exists();p.write_text(text,encoding='utf-8')
refs=[S/f'{pair}-body-primary.png',S/f'{pair}-cargo-endpoints.png',ROOT/g['ownOriginalMasters']['west']['path'],ROOT/g['ownOriginalMasters']['south']['path']]
(S/f'{pair}-01.request.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation; not started','promptSha256':sha(p),'orderedReferences':[{'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in refs],'sourceFrames':[g[k][f] for k in ['primaryIdles','stagedEndpoints'] for f in ['west','south']],'guideDependencies':[{'path':'tools/prepare_marsh_carry_turn_material_guides.py','sha256':sha(ROOT/'tools/prepare_marsh_carry_turn_material_guides.py')}],'sheetGrid':[4,1],'transparentBackground':True,'intermediateYawsFromWestDegrees':[22.5,45,67.5],'neutralOccupiedTargetHeight':147},indent=2)+'\n')
print('Frozen own West-front-left yaws;guide board positions unchanged,far-side implant and weight transfer explicit.')
