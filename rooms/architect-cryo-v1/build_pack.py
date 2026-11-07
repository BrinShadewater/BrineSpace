"""Rebuild identity variants from preserved sources using project cleanup only."""
from pathlib import Path
import hashlib
import importlib.util
import json
from PIL import Image

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('room_cleanup',ROOT.parents[1]/'tools/room_art_pipeline.py')
cleanup=importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)
for identity in ['veld','branforth']:
    source=ROOT/f'{identity}-source.png'
    raw=Image.open(source)
    clean=cleanup.clear_exterior(raw)
    clean.save(ROOT/f'{identity}-cleaned.png')
    dest=ROOT/identity
    dest.mkdir(exist_ok=True)
    frames=[]
    for i in range(6):
        x,y=(i%3)*418,(i//3)*586
        frame=clean.crop((x,y,x+418,y+627))
        frame.save(dest/f'wake-{i}.png')
        frames.append(frame)
    sheet=Image.new('RGBA',(1254,1254))
    for i,frame in enumerate(frames): sheet.paste(frame,((i%3)*418,(i//3)*627))
    sheet.save(dest/'contact-sheet.png')
    frames[0].save(dest/'preview.gif',save_all=True,append_images=frames[1:],duration=[1170,1170,1160,1170,1170,1160],loop=0,disposal=2)
    manifest={'name':identity+'-cryo-v1','frameWidth':418,'frameHeight':627,'pivot':[210,560],
        'source':'../'+source.name,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'sourceDimensions':list(raw.size),'sourceMode':raw.mode,'durationSeconds':7.0,
        'cleanup':'Project clear_exterior: remove edge-connected neutral pixels; no stretching/mirroring',
        'states':[{'id':'wake-south','frameCount':6,'frameFiles':[f'wake-{i}.png' for i in range(6)],'fps':6/7,'loop':False}]}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(identity,'built',raw.size,clean.getchannel('A').getextrema())
