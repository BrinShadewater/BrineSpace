from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,re
p=Path(__file__).resolve().parent;r=p.parents[1]
grid=r/'scripts/grid_canvas.gd';code=grid.read_text(encoding='utf-8')
block=code[code.index('player.load_manifest("res://character/crew-runtime-matte-v1/branforth/'):code.index('func _load_major_bill_animations')]
selected=None;manifests=[]
for line in block.splitlines():
    match=re.search(r'player\.load_manifest\("res://(character/[^\"]+\.json)"',line)
    if not match:continue
    path=r/match[1];m=json.loads(path.read_bytes())
    for state in m['states']:
        if state['id']=='idle-west':selected=(path,m,state);manifests.append(path)
assert selected
path,m,state=selected;f=state['frameFiles'][0];idle_path=r/f[6:] if f.startswith('res://') else path.parent/f
idle=Image.open(idle_path).convert('RGBA');registered=Image.new('RGBA',(256,256))
offset=(128-round(m['pivot'][0]),224-round(m['pivot'][1]));registered.alpha_composite(idle,offset)
sources=[('current selected West idle',registered,idle_path),('actual turn West endpoint',Image.open(r/'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png').convert('RGBA'),r/'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png'),('actual cargo West endpoint',Image.open(r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png').convert('RGBA'),r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png'),('guided middle trial',Image.open(p/'guided-middle-frames/003.png').convert('RGBA'),p/'guided-middle-frames/003.png')]
board=Image.new('RGB',(1280,640),'#303b40');d=ImageDraw.Draw(board)
for j,(label,im,_) in enumerate(sources):
    d.text((j*320+4,8),label,fill='white');board.paste(im,(j*320+32,24),im)
    upper=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(upper,(j*320,290),upper)
board.save(p/'selected-master-endpoints.png')
inventory={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in [grid,*manifests,idle_path,*[s[2] for s in sources[1:]]]}
report={'selectedIdleManifest':path.relative_to(r).as_posix(),'selectedIdleFrame':idle_path.relative_to(r).as_posix(),'idlePivot':m['pivot'],'idleStandingHeight':m['standingHeight'],'commonCanvasOffset':list(offset),'inputSha256':inventory,'unchangedAfterRead':all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inventory.items()),'visualReviewPending':True,'scope':'Current normal literal idle override order; common anatomicalH148/pivot registration, no source resizing/face alignment. Static family identity diagnostic, not motion/native/owner acceptance.'}
(p/'endpoint-identity-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['selectedIdleManifest','selectedIdleFrame','idlePivot','idleStandingHeight','commonCanvasOffset','unchangedAfterRead']}))
