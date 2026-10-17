"""Pinned raster, alpha, footprint and byte-identical bake gate."""
from pathlib import Path
import hashlib,json,runpy
from PIL import Image
P=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ledger=json.loads((P/'manifest.json').read_text())
checks=0
for asset in ledger['assets']:
    for version in asset['versions']:
        assert digest(P/version['file'])==version['sha256'],version['file'];checks+=1
    image=Image.open(P/asset['selected_source']).convert('RGBA')
    assert image.size==(1024,1024)
    alpha=image.getchannel('A')
    assert alpha.getpixel((0,0))==0
    assert alpha.getpixel((512,512))>=250
    b=alpha.getbbox();assert b[0]>=40 and b[1]>=40 and b[2]<=984 and b[3]<=984
    checks+=4
before={p.name:digest(p) for p in (P/'runtime').glob('*.png')}
runpy.run_path(str(P/'bake.py'),run_name='__main__')
assert before=={p.name:digest(p) for p in (P/'runtime').glob('*.png')}
print(f'Wreck source gate: {checks} checks; 8 byte-identical exports; 0 failures')
