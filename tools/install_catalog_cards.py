"""Install reviewed native catalog stills into all three card consumers."""
import hashlib,json,re,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/(sys.argv[2] if len(sys.argv)>2 else 'assets/room-catalog-refresh-v1/cards')
records=json.loads((ROOT/(sys.argv[1] if len(sys.argv)>1 else 'output/room-catalog-2026-09-08/runtime.json')).read_text())
OUT.mkdir(parents=True,exist_ok=True)
mapping={}
manifest=[]
for r in records:
    if r['id'] in ('corridor','corner','tee_corridor'): continue
    src=ROOT/r['images'][0].removeprefix('res://')
    dest=OUT/(r['id']+'.png')
    if dest.exists(): assert dest.read_bytes()==src.read_bytes(), 'Preserve earlier card revision'
    else: shutil.copyfile(src,dest)
    mapping[r['id']]='res://'+dest.relative_to(ROOT).as_posix()
    manifest.append({'id':r['id'],'path':mapping[r['id']],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'previous_card':r['card_before'],'renderer':r['view']})
for name in ('scripts/room_card_art.gd','scripts/grid_canvas.gd'):
    p=ROOT/name
    text=p.read_text(encoding='utf-8')
    for rid,target in mapping.items():
        pattern=r'("'+re.escape(rid)+r'":\s*\[?")res://[^"\n]+\.png(")'
        text,count=re.subn(pattern,lambda m:m[1]+target+m[2],text)
        assert count in ((1,) if name.endswith('room_card_art.gd') else (1,2)),(name,rid,count)
    p.write_text(text,encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(f'Installed {len(manifest)} cards across primary, grid and variant consumers; corridor variants retained.')
