"""Rebuild the native-density east carrying identity evidence."""
from pathlib import Path
import json, hashlib, argparse
from PIL import Image, ImageDraw
P = Path(__file__).resolve().parent
R = P.parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--inventory',default='character/bill-selected-source-audit-2026-10-01-locomotion-v13/source-inventory.json');parser.add_argument('--output');parser.add_argument('--direction',choices=['east','west','south','north'],default='east');args=parser.parse_args();direction=args.direction
a = json.loads((R/args.inventory).read_text())
if args.output:P=R/args.output;P.mkdir(parents=True,exist_ok=True)
b = Image.new('RGB',(1792,1024),(34,52,62))
dr, evidence = ImageDraw.Draw(b), []
for row,gear in enumerate(['bare','helmet']):
    s = a['selectedStateSources'][gear]['carry-'+direction]
    master = f'character/bill-seated-{"helmet-" if gear=="helmet" else ""}{direction}-coherent-v1/frames/sit-down-{direction}/000.png'
    choices = [(master,[128,224],'Master')]+[(f[6:],s['pivot'],str(i)) for i,f in enumerate(s['sourceFiles'])]
    for col,(file,pivot,caption) in enumerate(choices):
        f = R/file
        im = Image.open(f).convert('RGBA')
        plane = Image.new('RGBA',(256,256))
        plane.alpha_composite(im,(round(128-pivot[0]),round(224-pivot[1])))
        b.paste(plane,(col*256,row*512),plane)
        crop = plane.crop((100,65,166,125)).resize((198,180),Image.Resampling.NEAREST)
        b.paste(crop,(col*256+29,row*512+300),crop)
        dr.text((col*256+10,row*512+260),gear+' '+caption,fill='white')
        evidence.append({'gear':gear,'file':file,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
b.save(P/f'cargo-{direction}-head-audit.png')
(P/f'cargo-{direction}-head-audit.json').write_text(json.dumps({
    'scope':f'All six {direction} carry phases vs masters, registered native heads/shoulders. Pickup/unload not yet audited.',
    'sources':evidence},indent=2)+'\n')
print(f'Rebuilt six-phase paired {direction} carrying identity audit')
