from pathlib import Path
from PIL import Image,ImageDraw
import json
p=Path(__file__).resolve().parent
r=p.parents[1]
packs={m:json.loads((p/(m+'-manifest.json')).read_bytes()) for m in ['bare','helmet']}
records=[]
for direction in ['south','north','west']:
    states={m:next(s for s in packs[m]['states'] if s['id']=='inspect-'+direction) for m in packs}
    clock=states['bare']['frameDurationsMs']
    assert clock==states['helmet']['frameDurationsMs']
    frames=[]
    for i in range(len(clock)):
        frame=Image.new('RGBA',(368,208),(48,59,63,255))
        draw=ImageDraw.Draw(frame)
        for col,mode in enumerate(['bare','helmet']):
            path=r/states[mode]['frameFiles'][i].removeprefix('res://')
            im=Image.open(path).convert('RGBA')
            frame.alpha_composite(im,(col*184,24))
            draw.text((col*184+4,5),mode+' / '+direction+' diagnostics',fill='white')
        frames.append(frame)
    path=p/(direction+'-paired-preview.apng')
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=clock,loop=0,disposal=0,blend=0)
    with Image.open(path) as decoded:
        assert decoded.n_frames==len(frames)
        for i,expected in enumerate(frames):
            decoded.seek(i)
            assert decoded.convert('RGBA').tobytes()==expected.tobytes()
            assert abs(decoded.info['duration']-clock[i])<.001
    records.append(dict(direction=direction,pairedSourceFrames=len(frames),decodedRgbaExact=True,sourceClockExact=True,durationMs=sum(clock)))
(p/'preview-review.json').write_text(json.dumps(dict(records=records,scope='Lossless source-clock paired previews; creation/decode does not prove uninterrupted visual motion review.'),indent=2)+'\n')
print(json.dumps(records))
