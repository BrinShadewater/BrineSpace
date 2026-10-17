from pathlib import Path
import hashlib,json,re
from PIL import Image

def capture_registration(evidence='world-evidence.json',output='source-registration-evidence.json'):
    p=Path(__file__).resolve().parent;r=p.parents[1]
    branch=(r/'scripts/grid_canvas.gd').read_text().split('elif actor == "branforth":',1)[1].split('\n\t\tset(actor+',1)[0]
    banks={'bare':{},'helmet':{}}
    for kind,rel in re.findall(r'player\.(load_manifest|load_equipment_manifest)\([^\n]*?"res://([^"\n]+\.json)"',branch):
        path=r/rel;pack=json.loads(path.read_bytes());mode='bare' if kind=='load_manifest' else 'helmet'
        for state in pack.get('states',[]):
            if state['id'] in ['idle-west','walk-west','unload-west']:
                banks[mode][state['id']]=[(r/f.removeprefix('res://') if f.startswith('res://') else path.parent/f,state.get('pivot',pack.get('pivot')),state.get('standingHeight',pack.get('standingHeight')),path) for f in state.get('frameFiles',[])]
    matches={}
    for record in json.loads((p/evidence).read_bytes())['results']:
        if 'label' not in record:continue
        image=Image.open(r/record['source'].removeprefix('res://')).convert('RGBA');mode=record['label'].split('-')[0]
        found=[]
        for key,items in banks[mode].items():
            for index,(path,pivot,height,manifest) in enumerate(items):
                source=Image.open(path).convert('RGBA')
                if image.size==source.size and image.tobytes()==source.tobytes():
                    found.append({'key':key,'index':index,'source':str(path.relative_to(r)),'sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'manifest':str(manifest.relative_to(r)),'manifestSha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'pivot':pivot,'standingHeight':height})
        assert found,record['label'];matches[record['label']]=found[0]
    (p/output).write_text(json.dumps({'scope':'Captured source RGBA exactly matches current selected West idle/walk/unload manifest frames. Registered presentation metadata traced to current manifest, post-run source/manifest hashes; no retroactive native texture-metadata or prelaunch full source freeze claim.','matches':matches},indent=2)+'\n')
    print('All'+str(len(matches))+'captured source images match selected originals and registered manifest pivots/ruler.')

if __name__=='__main__':capture_registration()
