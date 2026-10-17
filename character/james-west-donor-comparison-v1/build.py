from pathlib import Path
import re,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
code=(r/'scripts/grid_canvas.gd').read_text();block=code[code.index('player.load_manifest("res://character/crew-runtime-matte-v1/branforth/'):code.index('func _load_major_bill_animations')]
bank={'bare':{},'helmet':{}};hashes={}
def digest(path):hashes[path.relative_to(r).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
digest(r/'scripts/grid_canvas.gd')
for line in block.splitlines():
    match=re.search(r'player\.(load_manifest|load_equipment_manifest)\([^\n]*?"res://(character/[^\"]+\.json)"',line)
    if not match:continue
    mode='bare' if match[1]=='load_manifest' else 'helmet';path=r/match[2];m=json.loads(path.read_bytes())
    states=[s for s in m['states'] if s['id'] in ['carry-turn-south-west','carry-turn-north-west','carry-turn-east-west','carry-settle-west','carry-west','idle-west','unload-west']]
    if states:digest(path)
    for s in states:bank[mode][s['id']]={'path':path,'m':m,'s':s}
def load(entry,i):
    file=entry['s']['frameFiles'][i];path=r/file[6:] if file.startswith('res://') else (entry['path'].parent/file).resolve();digest(path)
    im=Image.open(path).convert('RGBA');assert entry['m']['standingHeight']==148
    pivot=entry['m']['pivot'];out=Image.new('RGBA',(256,256));out.alpha_composite(im,(128-int(pivot[0]),224-int(pivot[1])));return out,path
def flat(im):
    bg=Image.new('RGBA',(256,256),'#303b40');bg.alpha_composite(im);return bg.convert('RGB')
report={'gears':{},'pages':[],'inputSha256':hashes,'visualReviewPending':True,'selected':False,'scope':'Current normal literal override order, same H148/pivot registration; no resize, fitted pose or composite new artwork. Existing near-West whole source poses against exact settle endpoints and standing reference.'}
for gear in bank:
    frames=[];rows=[];seen={}
    for label,key,i in [('entry','carry-settle-west',0),('exit','carry-settle-west',-1),('standing','idle-west',0)]:
        im,path=load(bank[gear][key],i);frames.append((label,im));rows.append({'role':label,'source':path.relative_to(r).as_posix()})
    for key in ['carry-turn-south-west','carry-turn-north-west','carry-turn-east-west']:
        entry=bank[gear][key];n=len(entry['s']['frameFiles'])
        for i in range(n-4,n):
            im,path=load(entry,i);upper=im.crop((96,56,176,136));sha=hashlib.sha256(upper.tobytes()).hexdigest()
            if sha in seen:
                rows.append({'source':path.relative_to(r).as_posix(),'key':key,'index':i,'upperExactAliasOf':seen[sha]});continue
            label=key.removeprefix('carry-turn-')+f' {i}';seen[sha]=label;frames.append((label,im));rows.append({'source':path.relative_to(r).as_posix(),'key':key,'index':i,'upperRGBASha256':sha})
    for start in range(0,len(frames),6):
        board=Image.new('RGB',(1536,550),'#303b40');d=ImageDraw.Draw(board)
        for j,(label,im) in enumerate(frames[start:start+6]):
            board.paste(flat(im),(j*256,24));d.text((j*256+4,4),gear+' '+label,fill='white')
            board.paste(flat(im).crop((96,56,160,120)).resize((256,256),Image.Resampling.NEAREST),(j*256,290))
        name=f'{gear}-{start:02d}.png';board.save(p/name);report['pages'].append(name)
    report['gears'][gear]={'sourceRows':rows,'wholePresentations':len(frames),'distinctUpperDonorImages':len(seen)}
report['inputHashesUnchanged']=all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in hashes.items())
(p/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'pages':report['pages'],'presentations':sum(v['wholePresentations'] for v in report['gears'].values()),'inputs':len(hashes)}))
