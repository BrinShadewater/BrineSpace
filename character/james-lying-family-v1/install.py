from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
path=R/'scripts/grid_canvas.gd'
def loader(b):
 s=b.decode();needle='\t\t\t\tpush_error("James bunk shared helmet mismatch")'
 if 'res://character/james-lying-family-v1/bare-manifest.json' in s:return b
 assert s.count(needle)==1
 ending='\r\n' if '\r\n' in s else '\n'
 insert=ending.join(['','\t\t\tplayer.load_manifest("res://character/james-lying-family-v1/bare-manifest.json", true)','\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-lying-family-v1/helmet-manifest.json"):','\t\t\t\tpush_error("James directional lying shared helmet mismatch")'])
 return s.replace(needle,needle+insert).encode()
atomic(path,loader)
path=R/'character/ACTIVE_ASSETS.json'
def registry(b):
 m=json.loads(b);m['actionOverrides']['branforth-lying']='character/james-lying-family-v1/bare-manifest.json';m['equipmentActionOverrides']['branforth-lying']='character/james-lying-family-v1/helmet-manifest.json';return (json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode()
atomic(path,registry)
# Installation is evidence of selection, not owner acceptance or completed polish.
path=P/'selection.json'
def selected(b):
 m=json.loads(b);m.update(status='installed_owner_review_pending',runtimeInstalled=True,helmetPaired=True);m['checks']['helmetPackaging']=408;m['pending']=['Continuous cross-animation material/motion polish','Coherent north sleep breathing','Other ordinary bed layouts/facings','Full-set coverage then consistency pass'];return (json.dumps(m,indent=2)+'\n').encode()
atomic(path,selected)
print('Installed 12 directional lying states in both modes, 144 frame references')
