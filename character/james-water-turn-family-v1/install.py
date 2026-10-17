from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
package=json.loads((P/'packaging-validation.json').read_bytes());route=json.loads((P/'route-evidence.json').read_bytes());native=json.loads((P/'native-routes-validation.json').read_bytes())
assert package['passed'] and route['failures']==0 and native['exitCode']==0 and native['realProfileUnchanged']
assert len(route['results'])==24 and all(s['completed'] and s['entered'] and len(s['seenSlots']) in [6,11] for s in route['results'])
assert all((P/('native-route-'+m+'-'+k+'.png')).exists() for m in ['bare','helmet'] for k in ['quarters','halves'])
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
def loader(b):
 if b'res://character/james-water-turn-family-v1/bare-manifest.json' in b:return b
 marker=b'\t\t\t\tpush_error("James directional water shared helmet mismatch")';assert b.count(marker)==1
 nl=b'\r\n' if b'\r\n' in b else b'\n'
 block=nl.join([b'\t\t\tplayer.load_manifest("res://character/james-water-turn-family-v1/bare-manifest.json", true)',b'\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-water-turn-family-v1/helmet-manifest.json"):',b'\t\t\t\tpush_error("James water turns shared helmet mismatch")'])
 return b.replace(marker,marker+nl+block,1)
atomic(R/'scripts/grid_canvas.gd',loader)
def registry(b):
 m=json.loads(b);m['actionOverrides']['branforth-water-turns']='character/james-water-turn-family-v1/bare-manifest.json';m['equipmentActionOverrides']['branforth-water-turns']='character/james-water-turn-family-v1/helmet-manifest.json';return (json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode()
atomic(R/'character/ACTIVE_ASSETS.json',registry)
selected=json.loads((P/'clearance.json').read_bytes())
def clearance(b):
 m=json.loads(b)
 for mode in ['bare','helmet']:
  for d in ['east','south','west','north']:
   old=m['actions'][mode]['transition-'+d];new=selected['actions'][mode]['transition-'+d]
   m['actions'][mode]['transition-'+d]=[min(old[0],new[0]),min(old[1],new[1]),max(old[2],new[2]),max(old[3],new[3])]
 return (json.dumps(m,indent=2)+'\n').encode()
atomic(R/'character/chief-engineer-branforth-v2/clearance.json',clearance)
for mode in ['bare','helmet']:
 def update(b):
  m=json.loads(b);m['status']='installed_owner_review_pending';return (json.dumps(m,indent=2)+'\n').encode()
 atomic(P/(mode+'-manifest.json'),update)
(P/'selection.json').write_text(json.dumps(dict(status='installed_owner_review_pending',runtimeInstalled=True,sourceQuarterCount=4,statesPerMode=12,refsPerMode=92,quarterDurationMs=520,halfDurationMs=680,visualReview='Native82px contacts and four route capture boards viewed',routeScope=route['scope'],fullSetComplete=False),indent=2)+'\n')
print('Installed12 ordinary swim turns in both modes; 184 refs; owner review pending')
