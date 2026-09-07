"""Fit generated helmets to original dry frames without modifying those frames."""
from pathlib import Path
import hashlib, json, argparse
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
CREW = {'bill':'major-bill-v2','veld':'dr-veld-v1','branforth':'chief-engineer-branforth-v1'}
parser = argparse.ArgumentParser()
parser.add_argument('--state',choices=['idle','walk','run','interact','kneel','repair','stand'],default='idle')
parser.add_argument('--direction',choices=['south','east','north','west'],default='south')
args = parser.parse_args()
clip = args.state + '-' + args.direction
view = 'front' if args.direction=='south' else args.direction
overlay_path = ROOT/'equipment'/view/'overlay.png'
overlay = Image.open(overlay_path).convert('RGBA')
sheet = Image.new('RGB',(1104,636),'#1d252a')
draw = ImageDraw.Draw(sheet)
for row,(actor,folder) in enumerate(CREW.items()):
    source_manifest = ROOT.parent/folder/'final/manifest.json'
    source = json.loads(source_manifest.read_text())
    state = next((s for s in source['states'] if s['id']==clip), None)
    if state is None:
        draw.text((5,row*212+4),actor+' / '+clip+' / MISSING BASE ANIMATION',fill='white')
        print(actor+' / '+clip+': missing base animation; no equipment frames produced')
        continue
    assert len(state['frameFiles']) == 6, 'Review sheet expects six phases'
    out = ROOT/'equipment/dry'/f'{actor}-{clip}'
    out.mkdir(parents=True,exist_ok=True)
    evidence = []
    files = []
    for i,relative in enumerate(state['frameFiles']):
        path = (source_manifest.parent/relative).resolve()
        body = Image.open(path).convert('RGBA')
        position = {'bill':(34,10),'veld':(34,7),'branforth':(34,9)}[actor]
        if args.direction=='east': position = {'bill':(35,9),'veld':(35,7),'branforth':(35,9)}[actor]
        if args.direction=='west': position = {'bill':(33,9),'veld':(33,7),'branforth':(33,9)}[actor]
        if args.direction=='north': position = {'bill':(34,9),'veld':(34,7),'branforth':(34,9)}[actor]
        if clip in ['kneel-east','stand-east','repair-east']:
            kneel_positions = {
                'bill':[(35,9),(35,11),(34,18),(34,28),(35,30),(34,30)],
                'veld':[(35,7),(31,14),(31,25),(31,29),(32,34),(31,31)],
                'branforth':[(35,9),(35,19),(34,26),(34,30),(34,32),(34,32)],
            }[actor]
            position = kneel_positions[i if args.state=='kneel' else 5-i]
            if args.state=='repair': position = kneel_positions[-1]
        # Keep the east visor over the face rather than ahead of it, including
        # lowered action poses so switching dry states does not shift the shell.
        if args.direction=='east': position=(position[0]-2,position[1])
        body.alpha_composite(overlay,position)
        name = f'frame_{i:03}.png'
        body.save(out/name)
        files.append(name)
        evidence.append({'source':str(path.relative_to(ROOT.parent)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'overlayTopLeft':position})
        large=body.resize((184,184),Image.Resampling.NEAREST)
        sheet.paste(large,(i*184,row*212+22),large)
    draw.text((5,row*212+4),actor+' / dry '+clip+' / pilot',fill='white')
    manifest={'status':'dry_equipment_fitting_pilot','equipment':'diving-helmet','frameWidth':92,'frameHeight':92,'pivot':source['pivot'],'states':[{**state,'frameFiles':files}]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'registration.json').write_text(json.dumps({'overlay':str(overlay_path.relative_to(ROOT)).replace('\\','/'),'overlaySha256':hashlib.sha256(overlay_path.read_bytes()).hexdigest(),'frames':evidence},indent=2)+'\n')
sheet.save(ROOT/'equipment/dry'/f'{clip}-contact.png')
print(clip+' dry helmet frames fitted; visual/runtime review required')
