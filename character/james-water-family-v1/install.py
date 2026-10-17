from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
report=json.loads((P/'route-evidence.json').read_bytes());native=json.loads((P/'native-routes-validation.json').read_bytes())
assert report['failures']==0 and native['exitCode']==0 and native['realProfileUnchanged']
assert {(s['mode'],s['initialFacing']) for s in report['results'] if s.get('arrived')}=={(m,d) for m in ['bare','helmet'] for d in ['east','south','west','north']}
assert (P/'native-route-contact.png').exists()
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
def loader(b):
 if b'res://character/james-water-family-v1/bare-manifest.json' in b:return b
 marker=b'\t\t\t\tpush_error("James directional lying shared helmet mismatch")'
 assert b.count(marker)==1
 newline=b'\r\n' if b'\r\n' in b else b'\n'
 block=newline.join([b'\t\t\tplayer.load_manifest("res://character/james-water-family-v1/bare-manifest.json", true)',b'\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-water-family-v1/helmet-manifest.json"):',b'\t\t\t\tpush_error("James directional water shared helmet mismatch")'])
 return b.replace(marker,marker+newline+block,1)
atomic(R/'scripts/grid_canvas.gd',loader)
def registry(b):
 m=json.loads(b);m['actionOverrides']['branforth-water']='character/james-water-family-v1/bare-manifest.json';m['equipmentActionOverrides']['branforth-water']='character/james-water-family-v1/helmet-manifest.json';return (json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode()
atomic(R/'character/ACTIVE_ASSETS.json',registry)
selected=json.loads((P/'clearance.json').read_bytes())
def clearance(b):
 m=json.loads(b)
 for mode in ['bare','helmet']:
  for d in ['east','south','west','north']:
   for action in ['swim','tread']:m[action][mode][d]=selected[action][mode][d]
   m['actions'][mode]['transition-'+d]=selected['actions'][mode]['transition-'+d]
 return (json.dumps(m,indent=2)+'\n').encode()
atomic(R/'character/chief-engineer-branforth-v2/clearance.json',clearance)
def selection(b):
 m=json.loads(b);m.update(status='installed_owner_review_pending',runtimeInstalled=True,routeVerification='route-evidence.json',routeVisualReview='Fresh camera-following grid captures reviewed at native station scale; original UI-obscured contact retained');return (json.dumps(m,indent=2)+'\n').encode()
atomic(P/'selection.json',selection)
print('Installed16 water states in both modes, paired registry and selected pixel clearance')
