"""Inventory existing bought exterior props and produce masked audition sheets.
Does not alter source pixels, owner marks or the master registry.
"""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/procedural-sites-2026-09-23'
CATALOG = ROOT / 'rooms/tileset-library/exterior.json'

def classified(entry):
    title = entry.get('title', '').lower()
    indoor = r'planter|potted|aquarium|specimen|tank|basin|ornament|display|cabinet|trough|machine|panel|pump|filter|skimmer|chiller|net,|water dosing|control|platform|tile.*wall'
    natural = r'^(sea anemone|seagrass|seaweed|kelp|coral|sea sponge|tube sponge|boulder|rock (pile|pool|cave|spire)|sand (floor|pile)|deep water|driftwood|rubble|shell|barnacle|mussel|limpet|urchin|starfish|seabed|algae|reef|stone (pile|cluster)|crystal|ice patch|dust patch)'
    exterior_detail = r'^(tide pool|deep water|sea (fern|fan|flowers|lettuce)|tube coral|brain coral|plate coral|seashell|skull rock|sand and rock|rock,|rock slab|stone (ruins|rubble|column)|trench opening|wreck timbers|anchor with chain|chain with hook|shelf fungus)'
    return bool(re.search(exterior_detail,title) or (entry.get('tileset')=='Reef' and title.startswith('egg cluster')) or (re.search(natural,title) and not re.search(indoor,title)))

def cut(entry):
    source = ROOT / entry['source'].removeprefix('res://')
    image = Image.open(source).convert('RGBA')
    mask = Image.new('L', image.size)
    draw = ImageDraw.Draw(mask)
    for poly in entry['pieces']:
        draw.polygon([tuple(p) for p in poly], fill=255)
    from PIL import ImageChops
    image.putalpha(ImageChops.multiply(image.getchannel('A'),mask))
    x,y,w,h=map(int,entry['region'])
    return image.crop((x,y,x+w,y+h))

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    entries=json.loads((ROOT/'rooms/tileset-library/props.json').read_text())
    exterior={e['id']:{'title':e.get('title',''),'tileset':e.get('tileset',''),'role':'exterior scenery'} for e in entries if classified(e)}
    CATALOG.write_text(json.dumps({'version':1,'assets':exterior},indent=2)+'\n')
    candidates=['uw1-186','uw1-188','uw1-146','uw1-193','uw1-145','uw1-147','uw1-191','mat-130','mat-131','mat-81','mb-210','mb-106']
    selected=[e for id in candidates for e in entries if e['id']==id]
    sheet=Image.new('RGB',(1000,120*len(selected)), '#16272b')
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for i,e in enumerate(selected):
        y=i*120
        draw.text((10,y+8),e['id']+' '+e.get('title',''),font=font,fill='white')
        sprite=cut(e)
        sprite.thumbnail((105,75),Image.Resampling.NEAREST)
        for j,bg in enumerate(['#899b92','#243b42','#463451']):
            panel=Image.new('RGBA',(160,85),bg)
            panel.alpha_composite(sprite,((160-sprite.width)//2,(85-sprite.height)//2))
            sheet.paste(panel,(450+j*175,y+25))
    sheet.save(OUT/'bought-candidates.png')
    comparisons=[
        ('Low rocks','uw1-188','sub-biomes-v1/brine-seep-stones-v1.png','Provisional: low profile, restrained material'),
        ('Coral','uw1-193','sub-biomes-v1/coral-lace-coral-v1.png','Retain original: upright silhouette and edge fragments'),
        ('Kelp','uw1-145','sub-biomes-v1/kelp-ribbon-kelp-v1.png','Retain original: tall side-view stems'),
        ('Driftwood','mat-130','driftwood-v1/waterlogged-timber-v1.png','Provisional: grounded horizontal silhouette'),
    ]
    board=Image.new('RGB',(1100,780),'#15262b');d=ImageDraw.Draw(board)
    d.text((20,10),'Existing / bought candidate — equal 0.55-cell width at 0.5 zoom',font=font,fill='white')
    for row,(role,id,path,decision) in enumerate(comparisons):
        y=45+row*180
        d.text((20,y),role+' | '+id+' | '+decision,font=font,fill='white')
        old=Image.open(ROOT/'legacy/default/assets/environment'/path).convert('RGBA')
        new=cut(next(e for e in entries if e['id']==id))
        for col,bg in enumerate(['#8b9a91','#233b41']):
            for side,sprite in enumerate([old,new]):
                sprite=sprite.copy()
                sprite=sprite.resize((106,max(1,round(sprite.height*106/sprite.width))),Image.Resampling.NEAREST)
                panel=Image.new('RGBA',(240,135),bg)
                panel.alpha_composite(sprite,((240-sprite.width)//2,(135-sprite.height)//2))
                x=20+col*530+side*250
                board.paste(panel,(x,y+30))
                d.text((x+8,y+33),'Existing' if side==0 else 'Bought',font=font,fill='white')
    board.save(OUT/'scenery-comparison.png')
    decisions={id:{'role':role,'baseline':path,'decision':decision} for role,id,path,decision in comparisons}
    decisions.update({'mb-210':{'role':'low rocks','decision':'Provisional: broad, low grey rubble'},'mat-131':{'role':'driftwood','decision':'Provisional: low broken timber'},'uw1-146':{'role':'coral','decision':'Rejected: upright branching silhouette'},'uw1-191':{'role':'sponge','decision':'Rejected pending edge-pixel cleanup'},'uw1-147':{'role':'seagrass','decision':'Rejected: pale stray foot pixels'},'mat-81':{'role':'coral','decision':'Rejected: busy, saturated mixed cluster'},'mb-106':{'role':'wreckage','decision':'Rejected: tall wall fragment'},'uw1-186':{'role':'rocks','decision':'Reserve candidate: taller than selected low boulders'}})
    for id,decision in decisions.items():
        entry=next(e for e in entries if e['id']==id)
        decision['source']=entry['source']
        decision['source_sha256']=hashlib.sha256((ROOT/entry['source'].removeprefix('res://')).read_bytes()).hexdigest()
    (OUT/'audition-decisions.json').write_text(json.dumps(decisions,indent=2)+'\n')
    (OUT/'inventory.json').write_text(json.dumps({'exterior_count':len(exterior),'candidate_ids':candidates},indent=2))
    print(f'{len(exterior)} classified exterior assets; {len(selected)} audition candidates')

if __name__=='__main__': main()
