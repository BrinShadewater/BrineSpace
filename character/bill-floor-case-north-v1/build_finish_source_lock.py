from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];hashes={}
for gear,key in [('bare',''),('helmet','diving-helmet')]:
 manifest=json.loads((R/f'character/bill-unload-north-rise-v1/{gear}-manifest.json').read_text())
 row=next(s for s in manifest['states'] if s['id']=='unload-north')
 hashes[key]=[hashlib.sha256(Image.open(R/path.removeprefix('res://')).convert('RGBA').tobytes().hex().encode()).hexdigest() for path in row['frameFiles']]
s='extends RefCounted\n## Canonical decoded RGBA, all14 authored sources per gear.\nconst HASHES='+json.dumps(hashes)+'\n'
s+='''static func matches(player,gear:String)->bool:
 if not HASHES.has(gear):return false
 var rows:Variant=player.rows_for(gear).get("unload-north")
 if not rows is Array or rows.size()!=14:return false
 for index in 14:
  if not rows[index] is Texture2D or rows[index].get_image().get_data().hex_encode().sha256_text()!=HASHES[gear][index]:return false
 return true
'''
(P/'finish_sources.gd').write_text(s,encoding='utf-8');(P/'finish_sources.gd.uid').write_text('uid://q5n4r6s8t2v5w\n')
print('28 exact decoded-source bindings written.')
