import hashlib,json,sys
from pathlib import Path
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';out=bank/'north-unload-installed-rise-v364';out.mkdir(exist_ok=True)
source=root/'character/james-cargo-north-v1'
sys.path.insert(0,str(source))
from unload_timing import add_midrise
media={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (source/'frames').rglob('*.png')}
records=[]
for gear in ['bare','helmet']:
    path=source/(gear+'-manifest.json');original=path.read_bytes()
    (out/(gear+'-manifest-before.json')).write_bytes(original)
    data=json.loads(original);state=next(s for s in data['states'] if s['id']=='unload-north')
    add_midrise(state);data['status']='installed_north_cargo_reused_rise_v364'
    path.write_text(json.dumps(data,indent=2)+'\n')
    records.append({'path':str(path.relative_to(root)),'beforeSha256':hashlib.sha256(original).hexdigest(),'afterSha256':hashlib.sha256(path.read_bytes()).hexdigest()})
assert all(hashlib.sha256((root/f).read_bytes()).hexdigest()==digest for f,digest in media.items())
(out/'installation.json').write_text(json.dumps({'version':364,'selected':True,'manifests':records,'sourceFrameHashes':media,'allSourceFramesUnchanged':True,'totalMs':520,'packageRebuilt':False},indent=2)+'\n')
print(json.dumps({'installedGears':2,'sourceFramesUnchanged':len(media),'newArtwork':0,'totalMs':520}))
