"""Package authored Margot sources without regenerating other companion assets."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'character/margot-v1'

def clean(tile):
    pixels = np.array(tile.convert('RGBA'))
    rgb = pixels[:, :, :3].astype(int)
    background = (rgb[:, :, 0] > rgb[:, :, 1] + 65) & (rgb[:, :, 2] > rgb[:, :, 1] + 65)
    pixels[background, 3] = 0
    out = Image.fromarray(pixels)
    box = out.getbbox()
    assert box and box[0] > 0 and box[1] > 0 and box[2] < out.width and box[3] < out.height, box
    return out.crop(box)

states, clips = [], {}
for filename, directions in [('south.png', ['south']), ('other-directions.png', ['west', 'north', 'east'])]:
    source = Image.open(PACK / 'sources' / filename)
    for row, direction in enumerate(directions):
        strip = source.crop((0,round(row*source.height/len(directions)),source.width,round((row+1)*source.height/len(directions))))
        rgb = np.array(strip.convert('RGB')).astype(int)
        ink = ~((rgb[:,:,0]>rgb[:,:,1]+65)&(rgb[:,:,2]>rgb[:,:,1]+65))
        edges=[0]
        for col in range(1,6):
            start=round(col*source.width/6)-24
            counts=ink.sum(axis=0)[start:start+48]
            edges.append(start+int(np.median(np.where(counts==counts.min())[0])))
        edges.append(source.width)
        cells = [clean(strip.crop((edges[col],0,edges[col+1],strip.height))) for col in range(6)]
        # Upright tail increases south view height; match cat body scale by direction.
        height = 34 if direction == 'south' else 28
        scale = height / max(tile.height for tile in cells)
        for state, indices, durations in [('idle', [0,1], [650,650]), ('walk', [2,3,4,5], [160]*4)]:
            paths, frames = [], []
            for frame, index in enumerate(indices):
                tile = cells[index]
                tile = tile.resize((round(tile.width*scale), round(tile.height*scale)), Image.Resampling.NEAREST)
                canvas = Image.new('RGBA', (92,92))
                canvas.alpha_composite(tile, ((92-tile.width)//2,86-tile.height))
                path = PACK / 'frames' / f'{state}-{direction}' / f'frame_{frame:03}.png'
                path.parent.mkdir(parents=True, exist_ok=True)
                canvas.save(path); frames.append(canvas)
                paths.append(path.relative_to(PACK).as_posix())
            states.append(dict(id=f'{state}-{direction}', frameFiles=paths, frameDurationsMs=durations, loop=True))
            clips[f'{state}-{direction}'] = frames
manifest = dict(character='margot', frameWidth=92, frameHeight=92, pivot=[46,86], strideDistanceCells={'walk':0.07}, states=states, mirrored=False,
                sourceHashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (PACK/'sources').glob('*.png')})
(PACK/'manifest.json').write_text(json.dumps(manifest,indent=2))
previews=[]
for i in range(4):
    preview=Image.new('RGBA',(368,92),(30,43,48,255))
    for col,direction in enumerate(['south','west','north','east']):preview.alpha_composite(clips[f'walk-{direction}'][i],(92*col,0))
    previews.append(preview.resize((1104,276),Image.Resampling.NEAREST).convert('RGB'))
previews[0].save(PACK/'walk-review.gif',save_all=True,append_images=previews[1:],duration=160,loop=0)
previews[0].save(PACK/'contact-sheet.png')

source=Image.open(PACK/'sources/pods.png')
cells=[clean(source.crop((round(col*source.width/4),0,round((col+1)*source.width/4),source.height))) for col in range(4)]
# Only the occupied pet-pod region comes from V2. Human pods retain original pixels.
revised=Image.open(PACK/'sources/pods-v2.png')
cells[2]=clean(revised.crop((round(2*revised.width/4),0,round(3*revised.width/4),revised.height)))
pod_scale=29/cells[2].width
for index,(name,tile) in enumerate(zip(['human-a','human-b','closed','open'],cells)):
    scale=62/tile.width if index<2 else pod_scale
    tile=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.NEAREST)
    assert tile.height<=144 and tile.width<=160
    canvas=Image.new('RGBA',(160,160))
    canvas.alpha_composite(tile,((160-tile.width)//2,144-tile.height))
    canvas.save(ROOT/'character/companions/encounters'/f'margot-{name}.png')
print('Margot: 8 clips, 24 frames, 4 pod assets packaged')
