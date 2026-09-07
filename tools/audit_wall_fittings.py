"""Audit wall attachments independently of floor-prop collision envelopes.

Checks source loading, true alpha, aspect-fit containment, and door-bay overlap.
This reports geometry and pixel facts, not art-style approval.
"""
import argparse,json
from pathlib import Path
from PIL import Image

def audit(root,profile_path):
    profile=json.loads((root/profile_path).read_text())
    errors=[]; report=[]
    hull=(-192,-240,192,-192)
    door=(-34,-246,34,-188)
    for item in profile['wall_items']:
        path=root/profile['textures'][item['texture']].removeprefix('res://')
        with Image.open(path) as image:
            if image.mode!='RGBA' or image.getchannel('A').getextrema()!=(0,255):
                errors.append(f'{path.name}: missing transparent exterior or opaque subject')
            x,y,w,h=item['rect']
            scale=min(w/image.width,h/image.height)
            sw,sh=image.width*scale,image.height*scale
            bounds=(x+(w-sw)/2,y+(h-sh)/2,x+(w+sw)/2,y+(h+sh)/2)
            if not (bounds[0]>=hull[0] and bounds[1]>=hull[1] and bounds[2]<=hull[2] and bounds[3]<=hull[3]):
                errors.append(f'{path.name}: outside hull riser')
            if bounds[0]<door[2] and bounds[2]>door[0] and bounds[1]<door[3] and bounds[3]>door[1]:
                errors.append(f'{path.name}: overlaps central hatch bay')
            report.append({'asset':path.name,'source_size':image.size,'world_bounds':bounds,'scale':scale})
    return {'attachments':report,'errors':errors}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('profile',type=Path)
    args=parser.parse_args()
    result=audit(Path(__file__).resolve().parents[1],args.profile)
    print(json.dumps(result,indent=2))
    raise SystemExit(bool(result['errors']))
