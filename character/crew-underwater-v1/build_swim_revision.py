"""Package reviewed stroke revisions without replacing the current runtime packs."""
from pathlib import Path
import json
import hashlib
import argparse
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--actor', choices=['bill','veld','branforth'], default='bill')
parser.add_argument('--direction', choices=['east','west'], default='east')
args=parser.parse_args()
actor,direction=args.actor,args.direction
pivot=(61,44) if direction=='east' else (43,44)
source = ROOT / f'generated/{actor}-swim-{direction}-candidate-02.png'
image = Image.open(source).convert('RGBA')
data = np.array(image)
rgb = data[:, :, :3].astype(np.int16)
data[(rgb[:, :, 0] > rgb[:, :, 1] + 35) & (rgb[:, :, 2] > rgb[:, :, 1] + 35)] = 0
occupied = (data[:, :, 3] > 0).sum(axis=0) > 3
edges = np.diff(np.r_[False, occupied, False].astype(int))
groups = [(int(a), int(b)) for a, b in zip(np.where(edges == 1)[0], np.where(edges == -1)[0]) if b-a > 25]
assert len(groups) == 6, groups
# Authored measurements remain separate for each generated identity source.
profiles = {
    'bill': ((1693,929),54,[(201,463),(494,465),(766,457),(1039,457),(1298,465),(1566,460)]),
    'veld': ((2048,737),56,[(289,346),(659,350),(950,347),(1270,353),(1558,353),(1882,355)]),
    'branforth': ((2048,683),74,[(216,338),(585,345),(929,337),(1250,335),(1585,337),(1902,336)]),
}
if direction=='west':
    profiles={
        'bill':((2048,768),64,[(190,387),(501,393),(839,384),(1151,393),(1481,393),(1792,390)]),
        'veld':((2048,738),61,[(150,389),(495,390),(834,386),(1161,383),(1495,390),(1823,386)]),
        'branforth':((2048,683),70,[(178,345),(514,355),(831,354),(1143,355),(1482,351),(1808,353)]),
    }
preview_size, head_height, shoulders = profiles[actor]
factor = image.width / preview_size[0]
assert abs(image.height / preview_size[1] - factor) < 0.005
scale = 14 / (head_height * factor)
out = ROOT / f'revisions/{actor}-swim-{direction}-v2'
out.mkdir(parents=True, exist_ok=True)
frames = []
placements = []
for index, (left, right) in enumerate(groups):
    pose = Image.fromarray(data[:,left:right])
    box = pose.getbbox()
    pose = pose.crop(box)
    pose = pose.resize((round(pose.width*scale),round(pose.height*scale)),Image.Resampling.BOX)
    pose.putalpha(pose.getchannel('A').point(lambda a:255 if a >= 128 else 0))
    sx,sy = shoulders[index]
    x = round(pivot[0]-(sx*factor-left-box[0])*scale)
    y = round(pivot[1]-(sy*factor-box[1])*scale)
    frame = Image.new('RGBA',(104,92))
    assert x >= 1 and y >= 1 and x+pose.width <104 and y+pose.height<92
    frame.alpha_composite(pose,(x,y))
    frame.save(out/f'frame_{index:03}.png')
    frames.append(frame)
    placements.append({'sourceCrop':[left+box[0],box[1],left+box[2],box[3]],'placement':[x,y],'bounds':frame.getbbox()})
manifest = {'status':'integrated_provisional_stroke_revision','frameWidth':104,'frameHeight':92,'pivot':list(pivot), 'strideDistanceCells':{'swim':0.16},'states':[{'id':'swim-'+direction,'frameFiles':[f'frame_{i:03}.png' for i in range(6)],'frameDurationsMs':[160]*6,'loop':True}]}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'contract.json').write_text(json.dumps({'source':str(source.relative_to(ROOT)), 'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'shouldersInPreview':shoulders,'previewSize':preview_size,'frames':placements,'reasonForCanvas':'Forward reach needs extra canvas; anatomical scale and shoulder pivot retained.'},indent=2)+'\n')
sheet=Image.new('RGB',(104*3*6,92*3+22),'#1d252a')
draw=ImageDraw.Draw(sheet)
previews=[]
for index,frame in enumerate(frames):
    large=frame.resize((312,276),Image.Resampling.NEAREST)
    sheet.paste(large,(index*312,22),large)
    draw.text((index*312+4,4),f'Phase {index+1}',fill='white')
    preview=Image.new('RGB',large.size,'#1d252a')
    preview.paste(large,(0,0),large)
    previews.append(preview)
sheet.save(out/'contact.png')
previews[0].save(out/'preview.gif',save_all=True,append_images=previews[1:],duration=[160]*6,loop=0)
print(actor + ' '+direction+' stroke revision: six registered frames, 104 x 92, no clipping')
