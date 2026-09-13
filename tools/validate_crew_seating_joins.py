"""Validate selected seating/sleeping joins in pivot coordinates, including RGB."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from crew_seating_revision import SELECTED
from crew_sleeping_revision import SELECTED as SLEEPING

ROOT=Path(__file__).resolve().parents[1]
PACKS={'veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2'}

def main():
    errors=[];checks=0
    families=[(a,d,'sit-down','sit-idle','sit-rise') for a,d in SELECTED]+[(a,d,'lie-down','sleep','get-up') for a,d in SLEEPING]
    for actor in sorted({entry[0] for entry in families}):
        art=ROOT/'character'/PACKS[actor]
        catalog=json.loads((art/'catalog.json').read_text());clips={}
        for variant in ['body','equipment']:
            for path in catalog[variant]:
                manifest=art/path;data=json.loads(manifest.read_text())
                for state in data['states']:
                    clips[variant,state['id']]=(manifest.parent,state,data['pivot'])
        def pose(variant,key,index):
            directory,state,pivot=clips[variant,key]
            image=Image.open(directory/state['frameFiles'][index]).convert('RGBA')
            canvas=Image.new('RGBA',(384,320))
            canvas.alpha_composite(image,(round(192-pivot[0]),round(260-pivot[1])))
            array=np.array(canvas);array[array[:,:,3]==0]=0
            return array
        for owner,direction,down_state,idle_state,rise_state in sorted(families):
            if owner!=actor:continue
            for variant in ['body','equipment']:
                down=down_state+'-'+direction;idle=idle_state+'-'+direction;rise=rise_state+'-'+direction
                pairs=[('standing join',down,0,'idle-'+direction,0),('seated join',down,-1,idle,0)]
                count=len(clips[variant,down][1]['frameFiles'])
                pairs += [('reverse '+str(i),down,i,rise,count-1-i) for i in range(count)]
                for label,a,i,b,j in pairs:
                    checks+=1
                    if not np.array_equal(pose(variant,a,i),pose(variant,b,j)):
                        errors.append(f'{actor}/{direction}/{variant}/{down_state}: {label}')
    print(json.dumps({'checks':checks,'errors':errors}))
    return bool(errors)

if __name__=='__main__':raise SystemExit(main())
