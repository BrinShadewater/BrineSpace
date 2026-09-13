"""Extract an explicitly reviewed video cycle using one fixed registration recipe."""
from pathlib import Path
import argparse
import hashlib
import json
import imageio.v2 as imageio
import numpy as np
from PIL import Image
from rebuild_bill_art import binary

ROOT=Path(__file__).resolve().parents[1]

def extract(recipe_path):
    recipe_path=Path(recipe_path).resolve()
    recipe=json.loads(recipe_path.read_text())
    source=(ROOT/recipe['source']).resolve()
    out=(ROOT/recipe['output']).resolve()
    if not out.is_relative_to(ROOT/'character'):raise ValueError('Cycle output must stay inside character assets')
    slots=recipe['sourceFrames'];durations=recipe['durations']
    if len(slots)!=len(durations) or not slots:raise ValueError('One duration required per source frame')
    if not all(isinstance(n,int) and n>=0 for n in slots):raise ValueError('Invalid frame index')
    if not all(n>0 for n in durations):raise ValueError('Durations must be positive')
    root_offsets=recipe.get('rootDisplacementPixels',[[0,0] for _ in slots])
    if len(root_offsets)!=len(slots) or any(not isinstance(v,list) or len(v)!=2 or any(type(n) is not int for n in v) for v in root_offsets):
        raise ValueError('Root displacement requires one integer pixel pair per frame')
    if root_offsets[0]!=[0,0]:raise ValueError('Root displacement must begin at zero')
    reader=imageio.get_reader(str(source),format='ffmpeg');meta=reader.get_meta_data()
    if list(meta['size'])!=recipe['sourceSize'] or meta['fps']!=recipe['fps']:raise ValueError('Source metadata differs from reviewed recipe')
    out.mkdir(parents=True,exist_ok=True)
    scale=recipe['scale'];position=tuple(recipe['position']);size=tuple(recipe['canvas']);poses=[];records=[]
    for slot,index in enumerate(slots):
        registered_position=tuple(position[i]-root_offsets[slot][i] for i in range(2))
        rgb=np.asarray(reader.get_data(index))[:,:,:3];r,g,b=rgb.astype(int).transpose(2,0,1)
        keep=~((r>g+35)&(b>g+35));rgba=np.dstack([rgb,keep.astype(np.uint8)*255]);rgba[~keep]=0
        raw=Image.fromarray(rgba);Image.fromarray(rgb).save(out/f'raw-{index:03}.png')
        dense=binary(raw.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.BOX),True)
        bounds=dense.getbbox()
        if bounds is None:raise ValueError(f'Empty source pose {index}')
        if bounds[0]+registered_position[0]<0 or bounds[1]+registered_position[1]<0 or bounds[2]+registered_position[0]>size[0] or bounds[3]+registered_position[1]>size[1]:
            raise ValueError(f'Registration would clip source pose {index}')
        pose=Image.new('RGBA',size);pose.alpha_composite(dense,registered_position)
        pose.save(out/f"{recipe['state']}-{slot:03}.png");poses.append(pose)
        records.append(dict(slot=slot,sourceFrame=index,bounds=pose.getbbox(),rootDisplacementPixels=root_offsets[slot]))
    reader.close()
    sheet=Image.new('RGB',(size[0]*len(poses),size[1]),'#293b40');previews=[]
    for i,pose in enumerate(poses):
        sheet.paste(pose,(i*size[0],0),pose)
        preview=Image.new('RGB',size,'#293b40');preview.paste(pose,(0,0),pose);previews.append(preview)
    sheet.save(out/'contact.png');previews[0].save(out/'stationary-loop.gif',save_all=True,append_images=previews[1:],duration=durations,loop=0)
    report=dict(recipe,sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),recipeSha256=hashlib.sha256(recipe_path.read_bytes()).hexdigest(),records=records,status='prepared_selection_tracked_in_ledger')
    (out/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'Extracted {len(poses)} fixed-registration poses; visual and selection evidence remain separate.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('recipe');extract(parser.parse_args().recipe)
