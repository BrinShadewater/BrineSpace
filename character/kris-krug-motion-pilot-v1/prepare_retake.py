from pathlib import Path
import json
from PIL import Image

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'kris-krug-motion-pilot-v2'
OUT.mkdir(exist_ok=True)
contract=json.loads((ROOT/'input-contract.json').read_text())
contract['chroma']='magenta'
contract['states']=['walk-east','tablet-east']
contract['budget']='Two corrective background trials, estimated USD0.38; cumulative five attempts USD0.95, not verified billing'
atlas=Image.open(ROOT.parent/'kris-krug-masters-v1/source-atlas.png').convert('RGBA')
body=atlas.crop(contract['whole_source_bounds'])
image=Image.new('RGB',tuple(contract['input_size']),'#ff00ff')
image.paste(body,tuple(contract['body_position']),body)
for state in contract['states']:
    dest=OUT/state;dest.mkdir(exist_ok=True)
    assert not (dest/'generation.json').exists()
    prompt=(ROOT/state/'prompt.txt').read_text().replace('bright green chroma background','bright magenta chroma background')
    prompt+=' No background color reflected on skin, hair or suit: graphite grey cloth retains exact neutral coloration, with no green or magenta flashes.'
    image.save(dest/'master-input.png');(dest/'prompt.txt').write_text(prompt,encoding='utf-8')
(OUT/'input-contract.json').write_text(json.dumps(contract,indent=2),encoding='utf-8')
print('Two magenta-background corrective sources prepared; canonical body/prompt actions retained.')
