from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
assert json.loads((P/'packaging-validation.json').read_text())['passed']
for name in ['native-staged','native-staged-berth-bare','native-staged-berth-helmet']:
    v=json.loads((P/(name+'-validation.json')).read_text())
    assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'],name
assert all((P/('native-berth-'+mode+'-contact.png')).exists() for mode in ['bare','helmet'])
def atomic(file,fn):
    before=file.read_bytes();after=fn(before)
    if before==after:return
    tmp=file.with_name(file.name+'.james.tmp');tmp.write_bytes(after)
    if file.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(file))
    tmp.replace(file)
def loader(b):
    if b'res://character/james-north-rest-polish-v1/bare-manifest.json' in b:return b
    marker=b'\t\t\t\tpush_error("James death actions shared helmet mismatch")';assert b.count(marker)==1
    nl=b'\r\n' if b'\r\n' in b else b'\n'
    block=nl.join([b'\t\t\tplayer.load_manifest("res://character/james-north-rest-polish-v1/bare-manifest.json", true)',b'\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-north-rest-polish-v1/helmet-manifest.json"):',b'\t\t\t\tpush_error("James North rest polish shared helmet mismatch")'])
    return b.replace(marker,marker+nl+block,1)
atomic(R/'scripts/grid_canvas.gd',loader)
def registry(b):
    m=json.loads(b);m['actionOverrides']['branforth-north-rest']='character/james-north-rest-polish-v1/bare-manifest.json';m['equipmentActionOverrides']['branforth-north-rest']='character/james-north-rest-polish-v1/helmet-manifest.json'
    return (json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode()
atomic(R/'character/ACTIVE_ASSETS.json',registry)
for mode in ['bare','helmet']:
    def status(b):
        m=json.loads(b);m['status']='installed_owner_review_pending';return (json.dumps(m,indent=2)+'\n').encode()
    atomic(P/(mode+'-manifest.json'),status)
(P/'selection.json').write_text(json.dumps(dict(status='installed_owner_review_pending',runtimeInstalled=True,statesPerMode=3,refsPerMode=18,fullSetComplete=False,source='character/james-lying-north-v1/source-lying-v6.png',sourcePoses=dict(lieDown=[0,1,2,3,4,6],sleep=[6,7,8,9,10,6],getUp=[6,4,3,2,1,0]),visualReview='Full paired pose board, fixed82/54/27 sample and36 actual retained q0 berth poses reviewed; owner review pending'),indent=2)+'\n')
print('Selected3 North rest states in both modes; current East bunk and other facings unchanged')
