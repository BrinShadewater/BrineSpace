"""Deterministically package the authored 6x4 companion motion sheets."""
from pathlib import Path
import json
import numpy as np
from collections import deque
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
for identity, height, directions in [('river', 44, ['south','west','north','east']), ('josh', 70, ['south','west','north','east'])]:
    pack = ROOT / 'character' / f'{identity}-v1'
    source = Image.open(pack/'sources/motion.png').convert('RGBA')
    ink=np.array(source)[:,:,:3].min(axis=2)<180
    rows=[0]
    for i in range(1,4):
        start=int(i*source.height/4)-45
        counts=ink.sum(axis=1)[start:start+90]
        rows.append(start+int(np.median(np.where(counts==counts.min())[0])))
    rows.append(source.height)
    states = []
    previews = []
    for row, direction in enumerate(directions):
        cells = []
        for col in range(6):
            tile = source.crop((round(col*source.width/6),rows[row],round((col+1)*source.width/6),rows[row+1]))
            pixels = np.array(tile)
            # White-background source contract. Retain ivory subject panels.
            white = (pixels[:,:,:3].min(axis=2)>230)
            pixels[white,3]=0
            seen=np.zeros(pixels.shape[:2],dtype=bool)
            for y,x in zip(*np.where(pixels[:,:,3]>0)):
                if seen[y,x]: continue
                todo=deque([(y,x)]); seen[y,x]=True; component=[]
                while todo:
                    cy,cx=todo.popleft(); component.append((cy,cx))
                    for ny,nx in [(cy-1,cx),(cy+1,cx),(cy,cx-1),(cy,cx+1)]:
                        if 0<=ny<tile.height and 0<=nx<tile.width and not seen[ny,nx] and pixels[ny,nx,3]:
                            seen[ny,nx]=True; todo.append((ny,nx))
                if len(component)<100:
                    for cy,cx in component: pixels[cy,cx,3]=0
            tile = Image.fromarray(pixels)
            box=tile.getbbox()
            assert box and box[0]>0 and box[1]>0 and box[2]<tile.width and box[3]<tile.height, (identity,row,col,box)
            cells.append(tile.crop(box))
        scale=height/max(t.height for t in cells)
        for state, indices, durations in [('idle',[0,1],[650,650]),('walk',[2,3,4,5],[160]*4)]:
            paths=[]
            for frame,index in enumerate(indices):
                tile=cells[index]
                tile=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.NEAREST)
                canvas=Image.new('RGBA',(92,92))
                canvas.alpha_composite(tile,((92-tile.width)//2,86-tile.height))
                path=pack/'frames'/f'{state}-{direction}'/f'frame_{frame:03}.png'
                path.parent.mkdir(parents=True,exist_ok=True)
                canvas.save(path)
                paths.append(path.relative_to(pack).as_posix())
                if state=='walk': previews.append(canvas)
            states.append(dict(id=f'{state}-{direction}',frameFiles=paths,frameDurationsMs=durations,loop=True))
    (pack/'manifest.json').write_text(json.dumps(dict(character=identity,frameWidth=92,frameHeight=92,pivot=[46,86],strideDistanceCells={'walk':0.10},states=states,source='sources/motion.png',rowDirections=directions,mirrored=False),indent=2))
    frames=[]
    for i in range(4):
        view=Image.new('RGBA',(92*4,92),(30,43,48,255))
        for direction in range(4): view.alpha_composite(previews[direction*4+i],(92*direction,0))
        frames.append(view.resize((736,184),Image.Resampling.NEAREST).convert('RGB'))
    frames[0].save(pack/'walk-review.gif',save_all=True,append_images=frames[1:],duration=160,loop=0)
    print(identity, len(states),'clips / 24 frames / height',height)
