from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
assert json.loads((P/'package-verification.json').read_text())['failures']==0
for name in ['native-staged','native-staged-routes']:
    v=json.loads((P/(name+'-validation.json')).read_text());assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'],name
e=json.loads((P/'native-staged-routes-evidence.json').read_text());assert e['failures']==0 and len(e['results'])==2 and all(r['arrived'] for r in e['results'])
def atomic(path,fn):
    before=path.read_bytes();after=fn(before)
    if before==after:return
    tmp=path.with_name(path.name+'.north-water.tmp');tmp.write_bytes(after)
    if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
    tmp.replace(path)
def loader(b):
    if b'res://character/james-water-north-polish-v1/bare-manifest.json' in b:return b
    marker=b'\t\t\t\tpush_error("James North rest polish shared helmet mismatch")';assert b.count(marker)==1
    nl=b'\r\n' if b'\r\n' in b else b'\n'
    block=nl.join([b'\t\t\tplayer.load_manifest("res://character/james-water-north-polish-v1/bare-manifest.json", true)',b'\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-water-north-polish-v1/helmet-manifest.json"):',b'\t\t\t\tpush_error("James North water polish shared helmet mismatch")'])
    return b.replace(marker,marker+nl+block,1)
atomic(R/'scripts/grid_canvas.gd',loader)
def registry(b):
    m=json.loads(b);m['actionOverrides']['branforth-north-water-polish']='character/james-water-north-polish-v1/bare-manifest.json';m['equipmentActionOverrides']['branforth-north-water-polish']='character/james-water-north-polish-v1/helmet-manifest.json';return (json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode()
atomic(R/'character/ACTIVE_ASSETS.json',registry)
for mode in ['bare','helmet']:
    def status(b):
        m=json.loads(b);m['status']='installed_owner_review_pending';return (json.dumps(m,indent=2)+'\n').encode()
    atomic(P/(mode+'-manifest.json'),status)
m=json.loads((P/'selection.json').read_text());m.update(status='installed_owner_review_pending',runtimeInstalled=True,packageChecks=211,sourceLeadIn='../james-water-north-v1/source-lead-in-v7.png');m['pending']=['Normal installed native playback/route checks','Owner and full-set motion/journey acceptance'];(P/'selection.json').write_text(json.dumps(m,indent=2)+'\n')
print('Installed paired North tread/start/stop overrides; clocks, clearances and selected swim loop unchanged')
