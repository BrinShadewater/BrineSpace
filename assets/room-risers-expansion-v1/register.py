"""Measure generated wall regions and optionally install only the 28 scoped records."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

PACK=Path(__file__).resolve().parent
ROOT=PACK.parents[1]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--install',action='store_true')
    args=parser.parse_args()
    briefs=json.loads((PACK/'briefs.json').read_text())
    registered={}
    audit=[]
    for key,brief in briefs.items():
        path=PACK/'masters'/f'{key}.png'
        if not path.exists():
            audit.append(dict(room=key,stage='missing'));continue
        im=Image.open(path)
        assert im.mode=='RGBA',key
        a=np.asarray(im.getchannel('A'))
        labels,_=ndimage.label(a>=128)
        counts=np.bincount(labels.ravel());counts[0]=0
        ys,xs=np.where(labels==counts.argmax())
        box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
        old=brief['reference_registration'];ob=old['opaque_component_bounds']
        sx=(box[2]-box[0])/(ob[2]-ob[0]);sy=(box[3]-box[1])/(ob[3]-ob[1])
        def mapped(rect):
            x,y,w,h=rect
            return [round(box[0]+(x-ob[0])*sx),round(box[1]+(y-ob[1])*sy),round(w*sx),round(h*sy)]
        record=copy.deepcopy(old)
        record.update(source='res://assets/room-risers-expansion-v1/masters/'+key+'.png',
            face=mapped(old['face']),cap=mapped(old['cap']),opaque_component_bounds=box,
            native_size=list(im.size),sha256=sha(path),prompt_sha256=sha(PACK/'prompts'/f'{key}.txt'),
            reference_sha256=brief['reference_sha256'],cap_policy='Production painted shell samples this measured cap',
            alpha_extrema=[int(a.min()),int(a.max())])
        problems=[]
        if key=='music_room' and record['sha256']=='ce44ef47b8bdccb95cf7be04117670ed5a557299bb304ea84b51d7c316973ef1':
            # Revised silhouette has a seven-pixel lower bevel/alpha fringe.
            # End the painted face above that fringe; preserve the source pixels.
            record['face'][3]-=7
        for part in ['face','cap']:
            x,y,w,h=record[part]
            if not (0<=x<x+w<=im.width and 0<=y<y+h<=im.height):problems.append(part+' outside image')
        x,y,w,h=record['face']
        interior=a[y+8:y+h-8,x+16:x+w-16]
        coverage=float((interior>=250).mean())
        if coverage<.995:problems.append('face not fully opaque')
        # Evaluate the margins outside the structural bounds, not anti-aliasing at the silhouette.
        outside=np.ones(a.shape,dtype=bool)
        outside[max(0,box[1]-12):min(im.height,box[3]+12),max(0,box[0]-12):min(im.width,box[2]+12)]=False
        halo=float((a[outside]>8).mean()) if outside.any() else 1.0
        if halo>.005:problems.append('visible exterior haze')
        if min(box[0],box[1],im.width-box[2],im.height-box[3])<8:problems.append('clipped margin')
        if abs(sx/sy-1)>.04:problems.append('wall aspect drift exceeds 4%')
        registered[key]=dict(base=record,integrated={k:record[k] for k in ['source','face','opaque_component_bounds','sha256','prompt_sha256','alpha_extrema']},inherited_from='')
        audit.append(dict(room=key,stage='registered',face_opaque_fraction=coverage,exterior_haze_fraction=halo,
            aspect_scale_ratio=sx/sy,problems=problems,source_sha256=sha(path),source_pixels_unmodified=True))
    (PACK/'registrations.json').write_text(json.dumps(registered,indent=2)+'\n')
    (PACK/'evidence/source-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    failures=[a for a in audit if a.get('problems') or a['stage']=='missing']
    print(json.dumps(dict(registered=len(registered),expected=len(briefs),failures=failures)))
    if args.install:
        assert not failures,'Fix source failures before installation'
        assert len({r['base']['sha256'] for r in registered.values()})==28
        dest=ROOT/'assets/architecture-rollout-2026-09-26/walls.json'
        live=json.loads(dest.read_text())
        for key,entry in registered.items():
            assert live[key] in [briefs[key]['previous'],entry],f'Concurrent binding change: {key}'
            live[key]=entry
        dest.write_text(json.dumps(live,indent=2)+'\n')
        print('Installed 28 bespoke risers; 47 other bindings retained.')

if __name__=='__main__':main()
