"""Deterministic placement of generated overlay over existing tread pixels."""
from pathlib import Path
import json, hashlib, argparse
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--clip',choices=['tread-south','tread-east','tread-north','tread-west','swim-east','swim-west','swim-north','swim-south','death-water-east','death-ground-east'],default='tread-south')
clip=parser.parse_args().clip
view='front' if clip in ['tread-south','swim-south'] else 'east'
if clip in ['tread-north','swim-north']: view='north'
if clip in ['tread-west','swim-west']: view='west'
if clip=='death-ground-east': view='front'
helmet_path=root/'equipment'/view/'overlay.png'
helmet=Image.open(helmet_path).convert('RGBA')
placements={'bill':[34,13],'veld':[34,13],'branforth':[34,13]} if clip=='tread-south' else {'bill':[54,22],'veld':[54,22],'branforth':[54,22]}
if clip=='tread-east':
    placements={'bill':[38,12],'veld':[39,12],'branforth':[39,12]}
if clip=='tread-north':
    placements={'bill':[34,13],'veld':[34,13],'branforth':[34,13]}
if clip=='tread-west':
    placements={'bill':[30,12],'veld':[29,12],'branforth':[29,12]}
if clip=='swim-west':
    placements={'bill':[15,23],'veld':[12,20],'branforth':[12,23]}
if clip=='swim-north':
    placements={'bill':[34,8],'veld':[34,6],'branforth':[34,10]}
if clip=='swim-south':
    placements={'bill':[34,31],'veld':[34,31],'branforth':[34,31]}
death_positions={'bill':[[54,22],[54,22],[55,21],[55,21],[55,21],[56,21]],'veld':[[52,22],[53,22],[54,22],[55,21],[55,21],[56,20]],'branforth':[[53,22],[54,22],[55,20],[55,21],[56,22],[56,22]]}
sheet=Image.new('RGB',(1104,636),'#1d252a');draw=ImageDraw.Draw(sheet)
if clip=='death-ground-east':
    death_positions={'bill':[[34,8],[37,16],[44,29],[48,43],[53,62],[55,62]],'veld':[[33,8],[39,18],[36,27],[44,43],[50,62],[54,62]],'branforth':[[33,8],[37,15],[43,28],[45,41],[52,60],[55,62]]}
rotations=[0,-10,-20,-35,-90,-90] if clip=='death-ground-east' else [0]*6
evidence={}
def foreground_regions(clip, index):
    if clip=='swim-south' and index in [0,4,5]:
        return [[39,53,54,63]]
    if clip=='swim-north' and index in [0,5]:
        return [[34,0,58,13]]
    if clip=='swim-north' and index==4:
        return [[28,8,38,25],[54,8,64,25]]
    return []
for row,(actor,position) in enumerate(placements.items()):
    pack=root/'pilot'/f'{actor}-{clip}'
    out=root/'equipment/fitting'/f'{actor}-{clip}';out.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((pack/'manifest.json').read_text())
    equipped_manifest={**manifest,'status':'equipment_fitting_pilot','equipment':'diving-helmet'}
    (out/'manifest.json').write_text(json.dumps(equipped_manifest,indent=2)+'\n')
    source_hashes=[]
    previews=[]
    for i,relative in enumerate(manifest['states'][0]['frameFiles']):
        path=pack/relative;body=Image.open(path).convert('RGBA')
        source_hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
        frame_position=death_positions[actor][i] if clip.startswith('death-') else position
        foreground_rects = foreground_regions(clip, i)
        foreground = [(rect, body.crop(tuple(rect))) for rect in foreground_rects]
        frame_helmet=helmet.rotate(rotations[i],resample=Image.Resampling.NEAREST,expand=True)
        body.alpha_composite(frame_helmet,tuple(frame_position))
        for rect, limb in foreground:
            body.alpha_composite(limb, tuple(rect[:2]))
        body.save(out/f'frame_{i:03}.png')
        enlarged=body.resize((184,184),Image.Resampling.NEAREST)
        preview=Image.new('RGB',(184,184),'#1d252a');preview.paste(enlarged,(0,0),enlarged);previews.append(preview)
        sheet.paste(enlarged,(i*184,row*212+22),enlarged)
    draw.text((5,row*212+4),actor+' / '+clip+' / helmet fitting pilot',fill='white')
    options={'loop':0} if manifest['states'][0]['loop'] else {}
    previews[0].save(out/'preview.gif',save_all=True,append_images=previews[1:],duration=manifest['states'][0]['frameDurationsMs'],**options)
    evidence[actor]={'overlayTopLeft':death_positions[actor] if clip.startswith('death-') else position,'sourceFrameSha256':source_hashes,'status':'fitting_pilot_not_runtime','hairMask':'none; visual occlusion review required','overlayRotationDegrees':rotations}
    evidence[actor]['foregroundRects'] = [foreground_regions(clip, i) for i in range(len(source_hashes))]
sheet.save(root/'equipment/fitting'/f'{clip}-contact.png')
(root/'equipment/fitting'/f'{clip}-registration.json').write_text(json.dumps({'overlayView':view,'overlaySha256':hashlib.sha256(helmet_path.read_bytes()).hexdigest(),'characters':evidence},indent=2)+'\n')
print('18 helmet fitting frames composed; runtime acceptance pending')
