from pathlib import Path
from PIL import Image, ImageDraw
import json,re,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
grid=r/'scripts/grid_canvas.gd';text=grid.read_text(encoding='utf-8');text=text.split('elif actor == "branforth":',1)[1].split('\n\t\tset(actor+',1)[0]
banks={False:{},True:{}};files=[grid]
for match in re.finditer(r'player\.load_(equipment_manifest|manifest)\((?:"diving-helmet",\s*)?"(res://character/[^"]+\.json)"',text):
    gear=match[1]=='equipment_manifest';f=r/match[2].removeprefix('res://');files.append(f)
    data=json.loads(f.read_bytes())
    for state in data.get('states',[]):banks[gear][state['id']]=(f,data,state)
def load(gear,state,slot):
    f,data,s=banks[gear][state];ref=s['frameFiles'][slot];source=r/ref[6:] if ref.startswith('res://') else f.parent/ref;files.append(source)
    im=Image.open(source).convert('RGBA');pivot=data.get('pivot',[128,224]);h=data.get('standingHeight',148)
    assert h==148,(f,h)
    out=Image.new('RGBA',(256,256));out.alpha_composite(im,(round(128-pivot[0]),round(224-pivot[1])))
    return out,source.relative_to(r).as_posix()
rows=[];records=[]
for gear in [False,True]:
    for direction,index in [('south',0),('west',4)]:
        candidate=r/'character/james-carry-headcaps-v1/frames'/f'{index:03}.png' if not gear else p/'frames'/f'{index:03}.png'
        files.append(candidate);items=[(Image.open(candidate).convert('RGBA'),'candidate '+direction)]
        for state,slot in [('idle-'+direction,0),('carry-'+direction,0),('carry-'+direction,-1),('unload-'+direction,0)]:
            im,source=load(gear,state,slot);items.append((im,state+(' last' if slot<0 else ' first')));records.append({'gear':gear,'state':state,'slot':slot,'source':source})
        board=Image.new('RGBA',(1280,300),(48,59,63,255));d=ImageDraw.Draw(board)
        for i,(im,label) in enumerate(items):board.alpha_composite(im,(i*256,35));d.text((i*256+5,10),('helmet ' if gear else 'bare ')+label,fill='white')
        rows.append(board)
out=Image.new('RGBA',(1280,1200))
for i,row in enumerate(rows):out.alpha_composite(row,(0,i*300))
out.convert('RGB').save(p/'normal-cargo-joins.png')
(p/'join-inputs.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},'sources':records,'visualReviewPending':True,'scope':'Literal ordered loader source audit, static common-ruler comparisons; no normal native dispatch or watched cadence.'},indent=2)+'\n',encoding='utf-8')
print('Four gear/direction rows, sixteen selected source references; fixed pivot translation only.')
