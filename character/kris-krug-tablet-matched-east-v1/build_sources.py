from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib

ROOT=Path(__file__).resolve().parent
atlas=Image.open(ROOT/'source-atlas.png').convert('RGBA')
ROOT.joinpath('frames').mkdir(exist_ok=True)
pieces=[]
for row in range(2):
    for col in range(4):
        x0=round(col*atlas.width/4);x1=round((col+1)*atlas.width/4)
        y0=round(row*atlas.height/2);y1=round((row+1)*atlas.height/2)
        cell=atlas.crop((x0,y0,x1,y1))
        box=cell.getchannel('A').point(lambda a:255 if a>32 else 0).getbbox()
        assert box
        box=(max(0,box[0]-3),max(0,box[1]-3),min(cell.width,box[2]+3),min(cell.height,box[3]+3))
        pieces.append((cell.crop(box),(x0+box[0],y0+box[1],x0+box[2],y0+box[3])))
neutral=pieces[0][0]
b=neutral.getchannel('A').point(lambda a:255 if a>180 else 0).getbbox()
scale=147/(b[3]-b[1])
records=[]
board=Image.new('RGB',(1000,490),'#30373c');d=ImageDraw.Draw(board)
labels=['neutral','tablet beside thigh','raise','support','consult','tap','finger lift','lower']
for i,(piece,bounds) in enumerate(pieces):
    a=piece.getchannel('A');box=a.point(lambda a:255 if a>180 else 0).getbbox()
    floor=box[3]-1
    # Whole source boot-support midpoint, same scale across all poses.
    pixels=a.load();xs=[x for y in range(max(0,floor-3),floor+1) for x in range(piece.width) if pixels[x,y]>180]
    anchor=(min(xs)+max(xs))/2
    resized=piece.resize((round(piece.width*scale),round(piece.height*scale)),Image.Resampling.NEAREST)
    position=(round(92-anchor*scale),round(172-floor*scale))
    frame=Image.new('RGBA',(184,184));frame.alpha_composite(resized,position)
    frame.save(ROOT/f'frames/{i:02}.png')
    enlarged=frame.resize((230,230),Image.Resampling.NEAREST)
    x=(i%4)*250;y=(i//4)*245
    board.paste(enlarged,(x,y),enlarged);d.text((x+10,y+231),labels[i],fill='white')
    records.append({'key':i,'label':labels[i],'source_bounds':bounds,'source_anchor':[anchor,floor],'position':position,'sha256':hashlib.sha256((ROOT/f'frames/{i:02}.png').read_bytes()).hexdigest()})
board.save(ROOT/'source-review.png')
(ROOT/'source-contract.json').write_text(json.dumps({'status':'whole-source pose candidate, not selected or engine-integrated','reference':'character/kris-krug-masters-v1/identity-east-source.png','scale':scale,'canvas':[184,184],'pivot':[92,172],'standingHeight':147,'alpha_extrema':atlas.getchannel('A').getextrema(),'source_sha256':hashlib.sha256((ROOT/'source-atlas.png').read_bytes()).hexdigest(),'processing':'Whole crops; one neutral-derived scale; sole support registration. No RGB edits or anatomy patches.','poses':records},indent=2),encoding='utf-8')
print('Saved 8 complete poses, fixed shared scale, source alpha preserved.')
