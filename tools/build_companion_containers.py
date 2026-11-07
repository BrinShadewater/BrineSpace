from pathlib import Path
from PIL import Image
import numpy as np
root=Path(__file__).resolve().parents[1]/'character/companions/encounters'
source=Image.open(root/'source.png').convert('RGBA')
# Authored sheet has a broad horizontal gutter above its taller second row.
for row,identity in enumerate(['river','josh']):
    cells=[]
    for col in range(2):
        tile=source.crop((round(col*source.width/2),0 if row==0 else 550,round((col+1)*source.width/2),550 if row==0 else source.height))
        pixels=np.array(tile);pixels[pixels[:,:,:3].min(axis=2)>225,3]=0
        tile=Image.fromarray(pixels);cells.append(tile.crop(tile.getbbox()))
    scale=(74 if row==0 else 94)/cells[0].width
    for tile,label in zip(cells,['closed','open']):
        tile=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.NEAREST)
        canvas=Image.new('RGBA',(160,160))
        canvas.alpha_composite(tile,((160-tile.width)//2,144-tile.height))
        canvas.save(root/f'{identity}-{label}.png')
print('4 recovery container states packaged')
