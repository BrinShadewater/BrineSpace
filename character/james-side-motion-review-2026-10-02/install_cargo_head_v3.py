from pathlib import Path
import json,copy,shutil,os,uuid,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];D=R/'character/james-east-cargo-heads-v3'
assert not D.exists(),'Do not repeat installation blindly'
guard=json.loads((P/'validate-turn-v3-validation.json').read_bytes());assert guard['exitCode']==0 and guard['realProfileUnchanged']
backup=P/'before-cargo-head-selection';backup.mkdir()
for path in [R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json']:shutil.copy2(path,backup/path.name)
D.mkdir();hashes={};slots=0
for mode in ['bare','helmet']:
    cargo=json.loads((P/('east-family-v2-'+mode+'-manifest.json')).read_bytes());turn=json.loads((P/('east-turn-v3-'+mode+'-manifest.json')).read_bytes());pack=copy.deepcopy(cargo);pack['states']+=copy.deepcopy(turn['states']);pack['name']='James compact East cargo and connected turns '+mode;pack['status']='selected_native_loader_check_pending_actual_task_review'
    for state in pack['states']:
        paths=[]
        for i,rel in enumerate(state['frameFiles']):
            source=(P/rel).resolve();path=D/'frames'/mode/state['id']/(str(i).zfill(3)+'.png');path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,path);paths.append(path.relative_to(D).as_posix());hashes[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest();slots+=1
        state['frameFiles']=paths;state.setdefault('provenance',{})['headFamily']='Original cargo/turn poses with master-matched generated head/neck extracts, explicit pose anchors and exact reverse/shared sources. Both gears reviewed at source and native scales; actual hauling lifecycle remains pending.'
    (D/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2))
def atomic(path,old,new):
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
grid=R/'scripts/grid_canvas.gd';old=grid.read_bytes();needle=b'\t\t\t\tpush_error("James matched cargo helmet mismatch")';assert old.count(needle)==1
new=old.replace(needle,needle+b'\n\t\t\tplayer.load_manifest("res://character/james-east-cargo-heads-v3/bare-manifest.json", true)\n\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-east-cargo-heads-v3/helmet-manifest.json"):\n\t\t\t\tpush_error("James compact East cargo head pair mismatch")');atomic(grid,old,new)
registry=R/'character/ACTIVE_ASSETS.json';old=registry.read_bytes();data=json.loads(old)
for field,mode in [('actionOverrides','bare'),('equipmentOverrides','helmet')]:
    assert field in data,field
    data[field]['branforth-east-cargo-heads']='character/james-east-cargo-heads-v3/'+mode+'-manifest.json'
atomic(registry,old,(json.dumps(data,indent=2)+'\n').encode())
(D/'selection-evidence.json').write_text(json.dumps({'sourceReferences':slots,'statesPerGear':9,'sourceHashes':hashes,'productionSelected':True,'normalLoaderNativeAcceptance':False,'actualTaskAcceptance':False,'fullGoalComplete':False},indent=2))
print(json.dumps({'selectedStatesPerGear':9,'copiedSources':slots,'productionFolder':D.relative_to(R).as_posix(),'actualTaskAcceptance':False}))
