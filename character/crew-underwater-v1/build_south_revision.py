"""Rebuild Bill's south camera correction from its preserved generated source."""
from pathlib import Path
import hashlib
import argparse
import json
import numpy as np
from PIL import Image, ImageDraw, ImageChops

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--actor', choices=['bill','veld','branforth'], default='bill')
parser.add_argument('--direction', choices=['south','north'], default='south')
parser.add_argument('--north-candidate', choices=['02','03'], default='02')
args = parser.parse_args()
actor, direction = args.actor, args.direction
assert direction == 'south' or actor in ['bill','branforth'], 'North source measurements pending for this actor'
source = ROOT / f'generated/{actor}-swim-{direction}-candidate-02.png'
if actor == 'branforth' and direction == 'south': source = ROOT / 'generated/branforth-swim-south-candidate-03.png'
out = ROOT / f'revisions/{actor}-swim-{direction}-v2'
if args.north_candidate == '03':
    assert actor == 'branforth' and direction == 'north'
    source = ROOT / 'generated/branforth-swim-north-candidate-03.png'
    out = ROOT / 'revisions/branforth-swim-north-v3'
out.mkdir(exist_ok=True)
raw = Image.open(source).convert('RGBA')
pixels = np.array(raw)
rgb = pixels[:, :, :3].astype(np.int16)
pixels[(rgb[:, :, 0] > rgb[:, :, 1] + 35) & (rgb[:, :, 2] > rgb[:, :, 1] + 35)] = 0
mask = (pixels[:, :, 3] > 0).sum(axis=0) > 3
edges = np.diff(np.r_[False, mask, False].astype(int))
groups = [(int(a), int(b)) for a, b in zip(np.where(edges == 1)[0], np.where(edges == -1)[0]) if b-a > 25]
components = None
if len(groups) != 6:
    # Separate connected silhouettes when their x projections overlap.
    remaining = Image.fromarray(np.where(pixels[:,:,3] > 0,255,0).astype('uint8'))
    components = []
    while remaining.getbbox():
        ys,xs = np.nonzero(np.array(remaining))
        marked = remaining.copy()
        ImageDraw.floodfill(marked,(int(xs[0]),int(ys[0])),0)
        component = ImageChops.subtract(remaining,marked)
        if np.count_nonzero(np.array(component)) > 500:
            components.append(component)
        remaining = marked
    components.sort(key=lambda mask: mask.getbbox()[0])
    assert len(components) == 6, len(components)
    groups = [(mask.getbbox()[0],mask.getbbox()[2]) for mask in components]
clean = Image.fromarray(pixels)
# Shoulder centers measured on the 1693 x 929 source preview, not bounding centers.
anchors = [(121,520),(420,520),(721,520),(1003,520),(1294,520),(1568,520)]
preview_width, preview_scale = 1693, 0.2
if actor == 'veld':
    anchors = [(122,530),(440,530),(744,550),(1010,538),(1270,530),(1536,530)]
    preview_width, preview_scale = 1672, 0.16
if actor == 'branforth':
    anchors = [(123,515),(423,515),(728,515),(1000,515),(1285,515),(1555,515)]
    preview_width, preview_scale = 1692, 0.2
if actor == 'branforth' and direction == 'north':
    preview_width, preview_scale = 1672, 14/60
    if args.north_candidate == '03': preview_scale = 14/48
factor = raw.width / preview_width
scale = preview_scale / factor
pivot = (52,76)
if direction == 'north':
    anchors = [(138,440),(432,440),(737,440),(1007,440),(1277,440),(1555,440)]
    pivot = (52,36)
    if actor == 'branforth': anchors = [(123,446),(416,447),(726,444),(999,454),(1293,443),(1546,433)]
    if args.north_candidate == '03': anchors = [(167,440),(434,440),(721,439),(987,439),(1255,440),(1517,440)]
frames, registrations = [], []
for i, ((left,right), (sx,sy)) in enumerate(zip(groups,anchors)):
    isolated = clean.copy()
    if components is not None: isolated.putalpha(components[i])
    box = isolated.crop((left,0,right,raw.height)).getbbox()
    crop = (left+box[0],box[1],left+box[2],box[3])
    body = isolated.crop(crop)
    body = body.resize((round(body.width*scale),round(body.height*scale)),Image.Resampling.BOX)
    data = np.array(body); data[data[:,:,3] < 128] = 0; data[data[:,:,3] >= 128,3] = 255
    body = Image.fromarray(data)
    pos = (round(pivot[0]-(sx*factor-crop[0])*scale),round(pivot[1]-(sy*factor-crop[1])*scale))
    assert pos[0] > 0 and pos[1] > 0 and pos[0]+body.width < 104 and pos[1]+body.height < 112
    frame = Image.new('RGBA',(104,112)); frame.alpha_composite(body,pos)
    frame.save(out/f'frame_{i:03}.png'); frames.append(frame)
    registrations.append({'crop':crop,'shoulderSource':[sx*factor,sy*factor],'paste':pos})
manifest = {'status':'integrated_provisional_stroke_revision','frameWidth':104,'frameHeight':112,'pivot':pivot,'strideDistanceCells':{'swim':0.16},'states':[{'id':'swim-'+direction,'frameFiles':[f'frame_{i:03}.png' for i in range(6)],'frameDurationsMs':[160]*6,'loop':True}]}
if args.north_candidate == '03': manifest['status'] = 'candidate_projection_revision_not_integrated'
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(out/'source-contract.json').write_text(json.dumps({'source':source.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':scale,'registration':registrations},indent=2)+'\n',encoding='utf-8')
sheet = Image.new('RGB',(1248,224),'#1d252a')
for i,frame in enumerate(frames):
    large=frame.resize((208,224),Image.Resampling.NEAREST);sheet.paste(large,(i*208,0),large)
sheet.save(out/'contact.png')
print(f'Six {actor} {direction} revision frames packaged; rebuild fittings and verify runtime status separately')
