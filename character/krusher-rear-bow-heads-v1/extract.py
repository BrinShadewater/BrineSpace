"""Replay accepted crop boxes with a single shared ruler; verify exact exports."""
from pathlib import Path
from PIL import Image
import hashlib,json,io
P=Path(__file__).resolve().parent
spec=json.loads((P/'extraction.json').read_text());raw=P/'generated-strip.png'
assert hashlib.sha256(raw.read_bytes()).hexdigest()==spec['rawSha256']
image=Image.open(raw).convert('RGBA')
for row in spec['records']:
 crop=image.crop(row['sourceBox']);scale=spec['commonScale']
 size=(round(crop.width*scale),round(crop.height*scale));assert list(size)==row['size']
 native=crop.resize(size,Image.Resampling.LANCZOS);buffer=io.BytesIO();native.save(buffer,format='PNG')
 assert hashlib.sha256(buffer.getvalue()).hexdigest()==row['sha256'],row['file']
 (P/row['file']).write_bytes(buffer.getvalue())
print(json.dumps({'exactHeadExports':len(spec['records']),'sharedRuler':spec['commonScale']}))
