import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
root=Path.cwd();base=root/'character/james-west-carry-walk-keys-v1';out=base/'release-hazard-review-v346';out.mkdir(exist_ok=True)
audit=base/'selected-family-audit-v333'
inventory=json.loads((audit/'selected-inventory.json').read_text())
provenance=json.loads((audit/'pixel-provenance.json').read_text())
rows=[];checks=0
for gear in ['bare','diving-helmet']:
    selected={r['key']:r for r in inventory['gears'][gear]}
    sources={r['key']:r for r in provenance['gears'][gear]}
    for direction in ['west','east','north','south']:
        board=Image.new('RGB',(1536,4*430),(47,58,63));draw=ImageDraw.Draw(board)
        for row,family in enumerate(['swim-distress','recover-air','death-ground','death-water']):
            key=family+'-'+direction;entry=selected[key]
            draw.text((8,row*430+5),f'{gear} / {key} / selected source poses',fill='white')
            for index,matches in enumerate(sources[key]['sourceMatches']):
                path=root/matches[0];im=Image.open(path).convert('RGBA')
                assert hashlib.sha256(im.tobytes()).hexdigest()==entry['pixelHashes'][index];checks+=1
                meta=entry['metadata'][index];scale=148/meta['standingHeight'];pivot=meta['pivot']
                if scale!=1:im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
                tile=Image.new('RGBA',(256,400));offset=(round(128-pivot[0]*scale),round(224-pivot[1]*scale))
                bounds=im.getbbox();assert 0<=bounds[0]+offset[0] and bounds[2]+offset[0]<=256 and 0<=bounds[1]+offset[1] and bounds[3]+offset[1]<=400
                tile.alpha_composite(im,offset)
                board.paste(tile,(index*256,row*430+24),tile)
                draw.text((index*256+5,row*430+407),f'{index}: {entry["durationsMs"][index]:g}ms',fill='white')
            rows.append({'gear':gear,'key':key,'poses':entry['frameCount'],'board':f'{gear}-{direction}.png'})
        board.save(out/f'{gear}-{direction}.png')
(out/'review.json').write_text(json.dumps({'pixelChecks':checks,'failures':0,'rows':rows,'scope':'Existing normal-loader V333 pixel inventory resolved to unchanged source images. All six source poses per directional hazard/recovery/death clip. Static registered source review; no new native hazard/controller or continuous motion acceptance.'},indent=2))
print(f'Prepared eight hazard/death/recovery boards; {checks} exact selected pose pixel matches')
