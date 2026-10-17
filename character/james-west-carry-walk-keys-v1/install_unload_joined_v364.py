import copy,hashlib,json,sys
from pathlib import Path
root=Path.cwd();out=root/'character/james-west-carry-walk-keys-v1/north-unload-installed-rise-v364'
sys.path.insert(0,str(root/'character/james-cargo-north-v1'))
from unload_timing import add_midrise,INDICES
folder=root/'character/james-cargo-material-joined-v1'
hashes={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (folder/'frames').rglob('*.png')}
reg_path=folder/'registration.json';reg=json.loads(reg_path.read_text());(out/'joined-registration-before.json').write_bytes(reg_path.read_bytes())
for gear in ['bare','helmet']:
    path=folder/(gear+'-manifest.json');(out/('joined-'+gear+'-manifest-before.json')).write_bytes(path.read_bytes())
    data=json.loads(path.read_text());state=next(s for s in data['states'] if s['id']=='unload-north')
    add_midrise(state);old=reg[gear]['unload-north'];reg[gear]['unload-north']=[copy.deepcopy(old[i]) for i in INDICES]
    path.write_text(json.dumps(data,indent=2)+'\n')
reg_path.write_text(json.dumps(reg,indent=2)+'\n')
assert all(hashlib.sha256((root/f).read_bytes()).hexdigest()==digest for f,digest in hashes.items())
installation=json.loads((out/'installation.json').read_text());installation['joinedSourceFrameHashes']=hashes;installation['joinedSourceFramesUnchanged']=True;installation['activeOverrideUpdated']=True
(out/'installation.json').write_text(json.dumps(installation,indent=2)+'\n')
failed=out/'first-overridden-run';failed.mkdir(exist_ok=True)
for f in list(out.glob('normal-*'))+[out/'normal.log']:
    if f.is_file():f.rename(failed/f.name)
print(json.dumps({'activeOverrideUpdated':True,'joinedFramesUnchanged':len(hashes),'newArtwork':0}))
