from pathlib import Path
from PIL import Image,ImageDraw
import json,re,hashlib,collections
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'selected-family-audit-v333'
inventory=json.loads((o/'selected-inventory.json').read_bytes())
grid=(r/'scripts/grid_canvas.gd').read_text()
loader=grid[grid.index('func _load_replacement_crew_animations()'):grid.index('func _load_major_bill_animations()')]
paths=[]
cat=r/'character/chief-engineer-branforth-v2/catalog.json';catalog=json.loads(cat.read_bytes())
paths += [cat.parent/str(f) for f in catalog['body']+catalog['equipment']]
paths += [r/f[6:] for f in re.findall(r'"(res://[^"\n]+\.json)"',loader) if '/james-' in f or '/crew-runtime-matte-v1/branforth/' in f]
paths=list(dict.fromkeys(paths))
refs={};bindings={str(cat.relative_to(r)):hashlib.sha256(cat.read_bytes()).hexdigest()};missing=[]
for manifest in paths:
    if not manifest.is_file():missing.append(str(manifest.relative_to(r)));continue
    data=json.loads(manifest.read_bytes());bindings[str(manifest.relative_to(r))]=hashlib.sha256(manifest.read_bytes()).hexdigest()
    for state in data.get('states',[]):
        for f in state.get('frameFiles',[]):
            path=r/f[6:] if f.startswith('res://') else manifest.parent/f
            refs.setdefault(path,[]).append(dict(manifest=str(manifest.relative_to(r)),key=state['id']))
pixels={};byhash=collections.defaultdict(list)
for path in refs:
    image=Image.open(path).convert('RGBA');h=hashlib.sha256(image.tobytes()).hexdigest();pixels[path]=h;byhash[h].append(path)
    bindings[str(path.relative_to(r))]=hashlib.sha256(path.read_bytes()).hexdigest()
unmatched=[];pose_count=0;reconciled={}
for gear,rows in inventory['gears'].items():
    rec=[]
    for row in rows:
        candidates=[]
        for i,h in enumerate(row['pixelHashes']):
            found=byhash.get(h,[]);pose_count+=1
            if not found:unmatched.append(dict(gear=gear,key=row['key'],slot=i,pixelHash=h))
            candidates.append([str(f.relative_to(r)) for f in found])
        rec.append(dict(key=row['key'],sourceMatches=candidates))
    reconciled[gear]=rec
(o/'pixel-provenance.json').write_text(json.dumps(dict(gears=reconciled,unmatched=unmatched,missingManifests=missing,scope='Exact selected RGBA hashes to matching source files; duplicate-source paths are equivalent matches, not proof of which path was last loaded.',bindings=bindings),indent=2)+'\n')
directions=['east','south','west','north'];families=['idle','walk','interact','inspect','repair','weld','carry','unload']
matrix=[]
for family in families:
    for direction in directions:
        key=family+'-'+direction
        matrix.append(dict(family=family,direction=direction,key=key,gears={g:next((dict(frameCount=row['frameCount'],durationMs=sum(row['durationsMs']),loop=row['loop']) for row in rows if row['key']==key),None) for g,rows in inventory['gears'].items()}))
core_missing=[dict(key=row['key'],gear=g) for row in matrix for g,val in row['gears'].items() if val is None]
representative=[]
for gear,rows in inventory['gears'].items():
    items=[]
    for family in families:
        for direction in directions:
            key=family+'-'+direction;row=next((x for x in rows if x['key']==key),None)
            if not row:continue
            for i in [0,row['frameCount']//2,row['frameCount']-1]:
                matches=byhash.get(row['pixelHashes'][i],[])
                if not matches:continue
                same=[f for f in matches if any(s['key']==key for s in refs[f])];path=(same or matches)[-1]
                items.append((Image.open(path).convert('RGBA'),f'{key} {i}',path,i,key))
    for start in range(0,len(items),24):
        board=Image.new('RGB',(1536,1120),(48,59,64));d=ImageDraw.Draw(board)
        for j,(im,label,path,i,key) in enumerate(items[start:start+24]):
            # Fixed source registration to a common displayed standing density;
            # scales whole canvases using declared metadata, never per-pose bounds.
            row=next(x for x in rows if x['key']==key);m=row['metadata'][i];scale=148/m['standingHeight'];size=tuple(round(v*scale) for v in im.size)
            image=im.resize(size,Image.Resampling.LANCZOS) if size!=im.size else im
            offset=(round(128-m['pivot'][0]*scale),round(224-m['pivot'][1]*scale))
            tile=Image.new('RGBA',(256,256));tile.alpha_composite(image,offset)
            x=(j%6)*256;y=(j//6)*280;board.paste(tile,(x,y+20),tile);d.text((x+5,y+2),label,fill='white')
            representative.append(dict(gear=gear,key=key,slot=i,source=str(path.relative_to(r)),pixelHash=row['pixelHashes'][i],scale=scale,offset=offset))
        board.save(o/f'{gear}-family-{start//24:02}.png')
summary=dict(states={g:len(rows) for g,rows in inventory['gears'].items()},poses={g:sum(row['frameCount'] for row in rows) for g,rows in inventory['gears'].items()},sourceFilesHashed=len(refs),manifestsInspected=len(paths),matchedSelectedSlots=pose_count-len(unmatched),unmatchedSelectedSlots=len(unmatched),missingManifests=missing,coreCoverage=matrix,coreMissing=core_missing,representativeSlots=representative,normalChanged=False,fullGoalComplete=False,visualAcceptance=False)
(o/'family-coverage.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['states','poses','sourceFilesHashed','manifestsInspected','matchedSelectedSlots','unmatchedSelectedSlots','coreMissing']}))
