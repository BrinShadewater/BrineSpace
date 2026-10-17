from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];name='walk00-case-v2-fleck';source=p/'walk00-case-v2.png'
crop=[112,112,160,160]
Image.open(source).convert('RGBA').crop(crop).resize((576,576),Image.Resampling.LANCZOS).save(p/f'{name}-target.png')
prompt='''Repair this fixed48x48native crop enlarged12x; maintain exact framing and transparent margins. Remove ONLY the tiny solitary GOLD/YELLOW DOT above the near glove and just left of silver wrist cuff, near crop native x15,y18 (world127,130). This upper dot is a phantom reference artifact. Replace it with continuous neutral matte graphite torso cloth behind wrist, natural subdued folds, no hole or alpha loss. Keep the actual rectangular LOWER belt meter exactly unchanged, its yellow bars, housing and position (crop x16..22,y25..38); also preserve case size and waist height, both hands, silver cuff, belt wrench, shoulder/torso and hip shape. No other yellow screen or fleck above glove, no black cavity or purple shift. Return repaired ORIGINAL full square crop; only this upper yellow fleck disappears.'''
(p/f'{name}-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[source,p/f'{name}-target.png',p/f'{name}-prompt.txt',Path(__file__)]
(p/f'{name}-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':crop,'admissionRegion':[124,126,130,134],'baseFile':source.name,'scope':'Tiny upper gold fleck repair, actual lower belt meter outside admission exact.'},indent=2)+'\n',encoding='utf-8')
print('Tiny fleck repair prepared; lower belt meter protected.')
