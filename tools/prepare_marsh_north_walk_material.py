"""Freeze selected North gait and prepare complete-pose material edit sources."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-walk-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    (BASE/'sources').mkdir(parents=True,exist_ok=True)
    contract=ROOT/'character/marsh-consistency-review-v1/runtime-contract.json'
    states=json.loads(contract.read_text())['states'];spec=states['walk-north']
    frozen=BASE/'baseline.json'
    if not frozen.exists():
        frozen.write_text(json.dumps({'runtimeContract':sha(contract),'states':states,'catalogSha256':sha(ROOT/'character/marsh-v2/catalog.json')},indent=2)+'\n')
    baseline=json.loads(frozen.read_text());assert baseline['states']['walk-north']==spec
    sheet=Image.new('RGBA',(1536,1024));plan=[]
    for slot,(path,h) in enumerate(zip(spec['files'],spec['hashes'])):
        image=Image.open(ROOT/path).convert('RGBA');assert sha(ROOT/path)==h
        dest=BASE/'sources'/f'original-{slot:03d}.png'
        if not dest.exists():dest.write_bytes((ROOT/path).read_bytes())
        assert sha(dest)==h
        large=image.resize((460,460),Image.Resampling.NEAREST)
        xy=(slot%3*512+26,slot//3*512+26);sheet.alpha_composite(large,xy)
        plan.append({'slot':slot,'path':path,'sha256':h,'cell':slot,'placedCanvas':[xy[0],xy[1],xy[0]+460,xy[1]+460],'originalBounds':image.getbbox()})
    sheet.save(BASE/'sources/north-walk-edit-input.png')
    selected=None
    catalog=json.loads((ROOT/'character/marsh-v2/catalog.json').read_text())
    for path in catalog['body']:
        data=json.loads((ROOT/'character/marsh-v2'/path).read_text())
        for state in data['states']:
            if state['id']=='walk-north':selected={'manifest':{k:v for k,v in data.items() if k!='states'},'state':state,'path':path}
    assert selected is not None
    (BASE/'edit-plan.json').write_text(json.dumps({'sheet':[1536,1024],'grid':[3,2],'canvasScale':2.5,'poses':plan,'selectedEntry':selected,'registration':'Preserve exact original184canvas/pivot92,172/density148/alpha/timings; coherent whole-body generated colours/detail.'},indent=2)+'\n')
    print('Frozen six selected North gait sources; full body3x2 edit input ready')
if __name__=='__main__':main()
