from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib

p = Path(__file__).resolve().parent
r = p.parents[1]
out = p / 'arrival-pacing-v326'
out.mkdir(exist_ok=True)
turn_root = r / 'character/james-cargo-half-turns-v1'
unload_root = r / 'character/james-cargo-material-joined-v1'
clocks = [100,140,160,160,140,80,140,160,160,140,100,80,100,100,90,80,70]
report = dict(durationMs=sum(clocks), clocks=clocks, normalChanged=False, gears={})
for gear in ['bare','helmet']:
    tm = json.loads((turn_root / f'{gear}-manifest.json').read_bytes())
    um = json.loads((unload_root / f'{gear}-manifest.json').read_bytes())
    turn = next(s for s in tm['states'] if s['id']=='carry-turn-south-north')
    unload = next(s for s in um['states'] if s['id']=='unload-north')
    paths = [turn_root/f for f in turn['frameFiles']]
    paths += [paths[-1]] + [unload_root/f for f in unload['frameFiles'][1:]]
    frames = [Image.open(f).convert('RGBA') for f in paths]
    assert len(frames)==17 and frames[10].tobytes()==frames[11].tobytes()
    hashes = [hashlib.sha256(f.read_bytes()).hexdigest() for f in paths]
    for i,f in enumerate(paths):
        (out/f'{gear}-{i:02}.png').write_bytes(f.read_bytes())
    for speed, factor in [('normal',1),('quarter',4)]:
        target=out/f'{gear}-{speed}.png'
        frames[0].save(target,save_all=True,append_images=frames[1:],duration=[c*factor for c in clocks],loop=0,disposal=0,blend=0)
        decoded=Image.open(target); measured=[]; sources=[]
        for i in range(decoded.n_frames):
            decoded.seek(i); measured.append(decoded.info['duration'])
            sources.append(decoded.convert('RGBA').tobytes())
        expected=frames[:11]+frames[12:]
        assert sources==[f.tobytes() for f in expected]
        assert measured==[c*factor for c in clocks[:10]+[180]+clocks[12:]]
    board=Image.new('RGB',(1536,810),(48,59,64)); d=ImageDraw.Draw(board)
    elapsed=0
    for i,im in enumerate(frames):
        x=(i%6)*256;y=(i//6)*270
        board.paste(im,(x,y+14),im)
        d.text((x+7,y+2),f'{i:02} {"turn" if i<11 else "unload"} {elapsed}ms / {clocks[i]}ms',fill='white')
        d.line((x+56,y+238,x+200,y+238),fill=(109,140,147))
        elapsed+=clocks[i]
    board.save(out/f'{gear}-chronology.png')
    report['gears'][gear]=dict(sources=[str(f.relative_to(r)) for f in paths],sha256=hashes,semanticSlots=17,decodedAPNGFrames=16)
(out/'inputs-and-packaging.json').write_text(json.dumps(report,indent=2)+'\n')
print('Paired source-exact arrival previews:17 semantic slots each,16 decoded frames,2000ms normal/8000ms quarter. Whole-source chronology boards built.')
