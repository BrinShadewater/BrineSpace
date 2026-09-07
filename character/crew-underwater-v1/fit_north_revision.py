"""Fit the rear helmet to measured north revision poses."""
from pathlib import Path
import hashlib,json,argparse
from PIL import Image
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--actor',choices=['bill','branforth'],default='bill')
parser.add_argument('--version',choices=['v2','v3'],default='v2')
args=parser.parse_args()
actor=args.actor
assert args.version!='v3' or actor=='branforth'
pack=ROOT/'revisions'/f'{actor}-swim-north-{args.version}'
out=pack/'helmet';out.mkdir(exist_ok=True)
overlay_path=ROOT/'equipment/north/overlay.png'
overlay=Image.open(overlay_path).convert('RGBA')
manifest=json.loads((pack/'manifest.json').read_text(encoding='utf-8'))
manifest['equipment']='diving-helmet'
evidence={'status':'integrated_provisional_fitting','overlay':overlay_path.relative_to(ROOT).as_posix(),'overlaySha256':hashlib.sha256(overlay_path.read_bytes()).hexdigest(),'frames':[]}
if args.version=='v3': evidence['status']='candidate_projection_fitting_not_integrated'
sheet=Image.new('RGB',(1248,224),'#1d252a')
for i,file in enumerate(manifest['states'][0]['frameFiles']):
    body=Image.open(pack/file).convert('RGBA');frame=body.copy();pos=(40,15)
    frame.alpha_composite(overlay,pos)
    regions=[(0,0,104,23)] if i in [0,5] else []
    if i == 1: regions=[(34,28,44,43),(61,28,71,43)]
    if i == 4: regions=[(37,22,45,36),(60,22,68,36)]
    if actor == 'branforth':
        regions=[(0,0,104,23)] if i in [0,4,5] else ([(34,22,44,39),(61,22,71,39)] if i == 1 else [])
    if args.version=='v3':
        regions=[(0,0,104,17),(35,17,43,38),(62,17,70,38)] if i in [0,4,5] else ([(34,12,43,38),(62,12,71,38)] if i==1 else [])
    for rect in regions:frame.alpha_composite(body.crop(rect),rect[:2])
    frame.save(out/file)
    evidence['frames'].append({'bodySha256':hashlib.sha256((pack/file).read_bytes()).hexdigest(),'overlayTopLeft':pos,'foregroundRects':regions})
    large=frame.resize((208,224),Image.Resampling.NEAREST);sheet.paste(large,(i*208,0),large)
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(out/'registration.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
sheet.save(out/'contact.png')
print(f'Six {actor} north helmet candidates fitted')
