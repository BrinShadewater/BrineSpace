from pathlib import Path
import json,re,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
grid=r/'scripts/grid_canvas.gd';code=grid.read_text();block=code[code.index('player.load_manifest("res://character/crew-runtime-matte-v1/branforth/'):code.index('func _load_major_bill_animations')]
bank={'bare':{},'helmet':{}};hashes={'scripts/grid_canvas.gd':hashlib.sha256(grid.read_bytes()).hexdigest()};loads=[]
def digest(path):hashes[path.relative_to(r).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
for line in block.splitlines():
    match=re.search(r'player\.(load_manifest|load_equipment_manifest)\([^\n]*?"res://(character/[^\"]+\.json)"',line)
    if not match:continue
    gear='bare' if match[1]=='load_manifest' else 'helmet';path=r/match[2];data=json.loads(path.read_bytes())
    relevant=[s for s in data['states'] if s['id'].startswith('carry-turn-') or s['id'].startswith('idle-') or s['id'] in ['carry-north','carry-south','carry-east','carry-west']]
    if not relevant:continue
    digest(path);loads.append({'gear':gear,'manifest':match[2],'states':[s['id'] for s in relevant]})
    for state in relevant:bank[gear][state['id']]={'manifest':path,'data':data,'state':state}
def source(entry,file):
    return r/file[6:] if file.startswith('res://') else (entry['manifest'].parent/file).resolve()
def registered(entry,file):
    path=source(entry,file);digest(path);im=Image.open(path).convert('RGBA');data=entry['data']
    assert float(data['standingHeight'])==148
    assert list(im.size)==[int(data['frameWidth']),int(data['frameHeight'])]
    pivot=data['pivot'];offset=(128-int(pivot[0]),224-int(pivot[1]))
    out=Image.new('RGBA',(256,256));out.alpha_composite(im,offset);return out,path
def diagnostic(im):
    mask=np.asarray(im)[:,:,3]>=32;yy,xx=np.where(mask);top=int(yy.min());bottom=int(yy.max()+1)
    hy,hx=np.where(mask[top:top+24]);fy,fx=np.where(mask[204:232])
    return {'alpha32CrownAboveRoot':224-top,'lowestAlpha32Row':bottom-1,
     'top24UnionWidthProxy':int(hx.max()-hx.min()+1),
     'footWindowUnionBounds':[int(fx.min()),int(fy.min()+204),int(fx.max()+1),int(fy.max()+205)]}
def flat(im):
    bg=Image.new('RGBA',(256,256),'#303b40');bg.alpha_composite(im);return bg.convert('RGB')
report={'selectedRuntimeLoadOrder':loads,'states':{},'masters':{},'boards':[],'visualReviewPending':True,
 'scope':'Read-only selected dry carry turns, both gears, actual grid literal load override order; no native execution or natural scheduling. Alpha crown/head-band/foot union diagnostics are not anatomical segmentation or visual acceptance. Registered at actual pivots/H148 without any resize or per-pose fitting.'}
turns=sorted(k for k in bank['bare'] if k.startswith('carry-turn-'))
assert len(turns)==12,turns
for gear in bank:
    for direction in ['north','south','east','west']:
        key='idle-'+direction;entry=bank[gear][key];im,path=registered(entry,entry['state']['frameFiles'][0])
        report['masters'][gear+'/'+direction]={'source':path.relative_to(r).as_posix(),'manifest':entry['manifest'].relative_to(r).as_posix(),'diagnostic':diagnostic(im)}
    for state_id in turns:
        entry=bank[gear][state_id];state=entry['state'];poses=[];paths=[];stats=[]
        for file in state['frameFiles']:
            im,path=registered(entry,file);poses.append(im);paths.append(path.relative_to(r).as_posix());stats.append(diagnostic(im))
        reverse_id='carry-turn-'+'-'.join(reversed(state_id.removeprefix('carry-turn-').split('-')))
        rev=bank[gear][reverse_id];rev_paths=[source(rev,file) for file in rev['state']['frameFiles']]
        reverse_exact=[hashlib.sha256((r/file).read_bytes()).hexdigest() for file in paths]==[hashlib.sha256(path.read_bytes()).hexdigest() for path in reversed(rev_paths)]
        report['states'][gear+'/'+state_id]={'manifest':entry['manifest'].relative_to(r).as_posix(),'frames':paths,'durationsMs':state['frameDurationsMs'],'diagnostics':stats,'reverseId':reverse_id,'reverseSourcePixelsExact':reverse_exact}
        # Both paths still documented; omit only a byte-identical reversed bank.
        if reverse_exact and state_id>reverse_id:continue
        n=len(poses);rows=(n+3)//4
        board=Image.new('RGB',(1024,280+rows*280),'#303b40');d=ImageDraw.Draw(board)
        for j,direction in enumerate(['north','south','east','west']):
            master=bank[gear]['idle-'+direction];im,_=registered(master,master['state']['frameFiles'][0]);board.paste(flat(im),(j*256,22));d.text((j*256+4,4),gear+' master '+direction,fill='white')
        for j,im in enumerate(poses):
            x=j%4*256;y=280+j//4*280;board.paste(flat(im),(x,y+22));v=stats[j]
            d.text((x+4,y+4),f'{state_id} {j:02d} crown{v["alpha32CrownAboveRoot"]}',fill='white')
            d.line((x+100,y+22+224,x+150,y+22+224),fill='#45aaaa')
        name=f'{gear}-{state_id}.png';board.save(p/name);report['boards'].append(name)
report['inputSha256']=hashes
report['endpointFamilies']={}
for gear in bank:
    for direction in ['north','south','east','west']:
        candidates=[];seen=set()
        for state_id in turns:
            a,b=state_id.removeprefix('carry-turn-').split('-')
            if direction not in [a,b]:continue
            entry=bank[gear][state_id];index=0 if direction==a else -1
            file=entry['state']['frameFiles'][index];im,path=registered(entry,file)
            pixelhash=hashlib.sha256(im.tobytes()).hexdigest()
            if pixelhash in seen:continue
            seen.add(pixelhash);candidates.append((state_id,im,path,pixelhash))
        m=bank[gear]['idle-'+direction];master,_=registered(m,m['state']['frameFiles'][0])
        c=bank[gear]['carry-'+direction];carry,_=registered(c,c['state']['frameFiles'][0])
        slots=[('standing master',master),('selected carry frame0',carry)]+[(name,im) for name,im,_,_ in candidates]
        board=Image.new('RGB',(256*len(slots),550),'#303b40');d=ImageDraw.Draw(board)
        for j,(name,im) in enumerate(slots):
            board.paste(flat(im),(j*256,24));d.text((j*256+4,4),name,fill='white')
            board.paste(flat(im).crop((84,64,148,128)).resize((256,256),Image.Resampling.NEAREST),(j*256,290))
        name=f'endpoints-{gear}-{direction}.png';board.save(p/name)
        report['endpointFamilies'][gear+'/'+direction]={'board':name,'distinctRegisteredTurnEndpointImages':len(candidates),'sources':[{'state':name,'source':path.relative_to(r).as_posix(),'registeredRGBAsha256':sha,'diagnostic':diagnostic(im)} for name,im,path,sha in candidates]}
report['checks']={'turnStatesPerGear':len(turns),'frameReferences':sum(len(s['frames']) for s in report['states'].values()),'allInputHashesUnchanged':all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in hashes.items())}
(p/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'checks':report['checks'],'boards':report['boards']}))
