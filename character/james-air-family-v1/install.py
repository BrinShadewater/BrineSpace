from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
assert json.loads((P/'packaging-validation.json').read_text())['passed']
for name in ['native-staged','native-behaviour']:
 report=json.loads((P/(name+'-validation.json')).read_text());assert report['exitCode']==0 and report['realProfileUnchanged']
evidence=json.loads((P/'behaviour-evidence.json').read_text());assert evidence['failures']==0 and len(evidence['results'])==8
assert all(s['actualLowAir'] and s['actualRecovery'] and s['distressSlots']==6 and s['recoverySlots']==6 for s in evidence['results'])
assert all((P/('native-behaviour-'+m+'.png')).exists() for m in ['bare','helmet'])
def atomic(file,fn):
 before=file.read_bytes();after=fn(before);tmp=file.with_name(file.name+'.james.tmp');tmp.write_bytes(after)
 if file.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(file))
 tmp.replace(file)
def loader(data):
 if b'res://character/james-air-family-v1/bare-manifest.json' in data:return data
 marker=b'\t\t\t\tpush_error("James water cargo turns shared helmet mismatch")';assert data.count(marker)==1;nl=b'\r\n' if b'\r\n' in data else b'\n'
 block=nl.join([b'\t\t\tplayer.load_manifest("res://character/james-air-family-v1/bare-manifest.json", true)',b'\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-air-family-v1/helmet-manifest.json"):',b'\t\t\t\tpush_error("James air actions shared helmet mismatch")'])
 return data.replace(marker,marker+nl+block,1)
atomic(R/'scripts/grid_canvas.gd',loader)
def registry(data):
 m=json.loads(data);m['actionOverrides']['branforth-air']='character/james-air-family-v1/bare-manifest.json';m['equipmentActionOverrides']['branforth-air']='character/james-air-family-v1/helmet-manifest.json';return (json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode()
atomic(R/'character/ACTIVE_ASSETS.json',registry)
selected=json.loads((P/'clearance.json').read_text())
def clearance(data):
 m=json.loads(data)
 for mode in ['bare','helmet']:
  for d in ['east','south','west','north']:
   key='swim-distress-'+d;old=m['life'][mode][key];new=selected['life'][mode][key];m['life'][mode][key]=[min(old[0],new[0]),min(old[1],new[1]),max(old[2],new[2]),max(old[3],new[3])]
 return (json.dumps(m,indent=2)+'\n').encode()
atomic(R/'character/chief-engineer-branforth-v2/clearance.json',clearance)
for mode in ['bare','helmet']:
 def status(data):
  m=json.loads(data);m['status']='installed_owner_review_pending';return (json.dumps(m,indent=2)+'\n').encode()
 atomic(P/(mode+'-manifest.json'),status)
(P/'selection.json').write_text(json.dumps(dict(status='installed_owner_review_pending',runtimeInstalled=True,fullSetComplete=False,statesPerMode=8,refsPerMode=48,visualReview='Fresh source,82px paired contacts and96 actual state captures reviewed'),indent=2)+'\n')
print('Installed8 distress/recovery states in both modes;96 refs; owner review pending')
