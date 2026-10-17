from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1];cargo=P.parent/'james-water-cargo-family-v1'
for folder in [cargo,P]:
 assert json.loads((folder/'packaging-validation.json').read_bytes())['passed']
 native=json.loads((folder/'native-staged-validation.json').read_bytes());assert native['exitCode']==0 and native['realProfileUnchanged']
route=json.loads((P/'route-evidence.json').read_bytes());native=json.loads((P/'native-routes-validation.json').read_bytes())
assert route['failures']==0 and native['exitCode']==0 and native['realProfileUnchanged']
assert len(route['results'])==24 and all(s['completed'] and s['entered'] and len(s['seenSlots']) in [6,11] for s in route['results'])
assert all((P/('native-route-'+m+'-'+k+'.png')).exists() for m in ['bare','helmet'] for k in ['quarters','halves'])
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
def loader(data):
 marker=b'\t\t\t\tpush_error("James water turns shared helmet mismatch")';assert data.count(marker)==1
 nl=b'\r\n' if b'\r\n' in data else b'\n';lines=[]
 for family,label in [('james-water-cargo-family-v1','James water cargo'),('james-water-cargo-turn-family-v1','James water cargo turns')]:
  if ('res://character/'+family+'/bare-manifest.json').encode() in data:continue
  lines.extend([('\t\t\tplayer.load_manifest("res://character/'+family+'/bare-manifest.json", true)').encode(),('\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/'+family+'/helmet-manifest.json"):').encode(),('\t\t\t\tpush_error("'+label+' shared helmet mismatch")').encode()])
 return data.replace(marker,marker+nl+nl.join(lines),1) if lines else data
atomic(R/'scripts/grid_canvas.gd',loader)
def registry(data):
 m=json.loads(data)
 for key,family in [('branforth-water-cargo','james-water-cargo-family-v1'),('branforth-water-cargo-turns','james-water-cargo-turn-family-v1')]:
  m['actionOverrides'][key]='character/'+family+'/bare-manifest.json';m['equipmentActionOverrides'][key]='character/'+family+'/helmet-manifest.json'
 return (json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode()
atomic(R/'character/ACTIVE_ASSETS.json',registry)
selected=json.loads((P/'clearance.json').read_bytes())
def clearance(data):
 m=json.loads(data)
 for field in ['actions','life']:
  for mode in ['bare','helmet']:
   for key,new in selected[field][mode].items():
    if not (key.startswith(('salvage-','swim-pickup-','swim-carry-')) if field=='actions' else key.startswith('cargo-turn-')):continue
    old=m[field][mode].get(key,new);m[field][mode][key]=[min(old[0],new[0]),min(old[1],new[1]),max(old[2],new[2]),max(old[3],new[3])]
 return (json.dumps(m,indent=2)+'\n').encode()
atomic(R/'character/chief-engineer-branforth-v2/clearance.json',clearance)
for folder,refs in [(cargo,72),(P,92)]:
 for mode in ['bare','helmet']:
  def status(data):
   m=json.loads(data);m['status']='installed_owner_review_pending';return (json.dumps(m,indent=2)+'\n').encode()
  atomic(folder/(mode+'-manifest.json'),status)
 selection=json.loads((folder/'selection.json').read_bytes());selection.update(status='installed_owner_review_pending',runtimeInstalled=True,fullSetComplete=False,refsPerMode=refs)
 (folder/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
print('Installed 24 cargo/activity/turn states, 328 references in both modes; owner review pending')
