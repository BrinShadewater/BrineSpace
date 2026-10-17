from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,hashlib
from scipy.ndimage import distance_transform_edt
R=Path.cwd();P=R/'character/krusher-head-fit-v3';raw=Image.open(P/'generated-swim-fit.png').convert('RGBA');(P/'sources').mkdir(exist_ok=True)
regions={
'bare-east':{'box':[440,163,565,287],'polygon':[[446,212],[447,190],[468,171],[499,165],[547,167],[560,190],[552,213],[545,225],[552,241],[543,247],[541,263],[530,280],[503,283],[488,277],[471,267],[459,255],[456,235],[443,229]],'size':[31,31]},
'bare-west':{'box':[810,163,931,287],'polygon':[[810,190],[819,174],[846,167],[885,169],[915,183],[929,201],[929,229],[921,247],[905,262],[888,281],[858,283],[834,269],[829,250],[826,238],[819,233],[822,215]],'size':[30,31]},
'visor-east':{'box':[499,693,560,779],'polygon':[[500,713],[514,700],[546,694],[557,698],[554,711],[553,720],[556,727],[550,733],[551,746],[550,767],[537,775],[519,777],[506,763],[503,740]],'size':[16,23]},
'visor-west':{'box':[811,692,878,779],'polygon':[[824,698],[855,699],[870,714],[872,744],[869,768],[853,778],[835,777],[823,764],[819,750],[818,735],[813,727],[823,720]],'size':[18,23]}}
for k,q in regions.items():
 mask=Image.new('L',raw.size);ImageDraw.Draw(mask).polygon([tuple(x) for x in q['polygon']],fill=255);im=raw.copy();im.putalpha(mask);im=im.crop(tuple(q['box'])).resize(tuple(q['size']),Image.Resampling.NEAREST);im.save(P/'sources'/f'{k}-native.png')
 q['source']='generated-swim-fit.png';q['output']=f'sources/{k}-native.png';q['sourceSHA256']=hashlib.sha256((P/q['source']).read_bytes()).hexdigest();q['outputSHA256']=hashlib.sha256((P/q['output']).read_bytes()).hexdigest()
(P/'extraction.json').write_text(json.dumps({'method':'Explicit authored source polygons and recorded native nearest extraction, no painted new pixels or generated body reuse','regions':regions},indent=2)+'\n')
print('Four generated head/neck sources extracted, with source hashes and explicit regions.')
