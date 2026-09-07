"""Deterministic swim pilot extraction; leaves existing crew packs untouched."""
from pathlib import Path
import json
import argparse
import hashlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--character', choices=['bill','veld','branforth'], default='branforth')
parser.add_argument('--state', choices=['swim','tread','death-water'], default='swim')
parser.add_argument('--direction', choices=['east','west','north','south'], default='east')
args = parser.parse_args()
clip = args.character + '-' + args.state + '-' + args.direction
source = ROOT / 'generated' / (clip + '.png')
data = np.array(Image.open(source).convert('RGBA'))
rgb = data[:, :, :3].astype(np.int16)
key = (rgb[:, :, 0] > rgb[:, :, 1] + 35) & (rgb[:, :, 2] > rgb[:, :, 1] + 35)
data[key] = 0
occupied = (data[:, :, 3] > 0).sum(axis=0) > 3
edges = np.diff(np.r_[False, occupied, False].astype(int))
groups = [(int(a), int(b)) for a, b in zip(np.where(edges == 1)[0], np.where(edges == -1)[0]) if b-a > 25]
assert len(groups) == 6, groups
registration = json.loads((ROOT/'registration.json').read_text())[args.character if args.state == 'swim' and args.direction == 'east' else clip]
assert hashlib.sha256(source.read_bytes()).hexdigest() == registration['sourceSha256'], 'Source changed: re-review anchors'
scale = registration['targetHeadHeight'] / registration['headHeight']
frames = []
out = ROOT / 'pilot' / clip
out.mkdir(parents=True, exist_ok=True)
for i, (left, right) in enumerate(groups):
    pose = Image.fromarray(data[:, left:right])
    box = pose.getbbox()
    pose = pose.crop(box)
    pose = pose.resize((round(pose.width*scale), round(pose.height*scale)), Image.Resampling.BOX)
    pose.putalpha(pose.getchannel('A').point(lambda a: 255 if a >= 128 else 0))
    frame = Image.new('RGBA', (92,92))
    sx, sy = registration['shoulders'][i]
    px, py = registration['anchor']
    x = round(px-(sx-left-box[0])*scale)
    y = round(py-(sy-box[1])*scale)
    assert x >= 1 and y >= 1 and x+pose.width < 92 and y+pose.height < 92, (clip,i,x,y,pose.size)
    frame.alpha_composite(pose, (x,y))
    frame.save(out / f'frame_{i:03}.png')
    frames.append(frame)
sheet = Image.new('RGB', (1104, 206), '#1d252a')
draw = ImageDraw.Draw(sheet)
for i, frame in enumerate(frames):
    large = frame.resize((184,184), Image.Resampling.NEAREST)
    sheet.paste(large, (i*184,22), large)
    draw.text((i*184+5,4), f'Phase {i+1}', fill='white')
sheet.save(out/'contact.png')
previews=[]
for frame in frames:
    bg=Image.new('RGB',(184,184),'#1d252a')
    im=frame.resize((184,184),Image.Resampling.NEAREST)
    bg.paste(im,(0,0),im)
    previews.append(bg)
durations = [180,180,220,220,260,500] if args.state == 'death-water' else [160]*6
looping = args.state in ['swim', 'tread']
options = {'loop':0} if looping else {}
previews[0].save(out/'preview.gif',save_all=True,append_images=previews[1:],duration=durations,**options)
manifest = {'status':'packaged_pilot_not_integrated','frameWidth':92,'frameHeight':92,'pivot':registration['anchor'],'strideDistanceCells':{'swim':0.16},'states':[{'id':args.state+'-'+args.direction,'frameFiles':[f'frame_{i:03}.png' for i in range(6)],'frameDurationsMs':durations,'loop':looping}]}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'contract.json').write_text(json.dumps({'status':'pilot_not_integrated','canvas':[92,92],'registration':'authored shoulder-center','anchor':registration['anchor'],'sourceSha256':registration['sourceSha256'],'scale':scale,'frames':6,'frameDurationsMs':durations,'source':str(source.relative_to(ROOT))},indent=2)+'\n')
print(clip + ': six registered frames, binary alpha, no clipping')
