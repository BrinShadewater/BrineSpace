from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
assert json.loads((P/'package-verification.json').read_text())['failures']==0
v=json.loads((P/'native-staged-behaviour-validation.json').read_text());assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged']
def atomic(path,fn):
    before=path.read_bytes();after=fn(before)
    if before==after:return
    tmp=path.with_name(path.name+'.west-death.tmp');tmp.write_bytes(after)
    if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
    tmp.replace(path)
def loader(b):
    if b'res://character/james-west-water-death-polish-v1/bare-manifest.json' in b:return b
    marker=b'\t\t\t\tpush_error("James North water polish shared helmet mismatch")';assert b.count(marker)==1;nl=b'\r\n' if b'\r\n' in b else b'\n'
    block=nl.join([b'\t\t\tplayer.load_manifest("res://character/james-west-water-death-polish-v1/bare-manifest.json", true)',b'\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-west-water-death-polish-v1/helmet-manifest.json"):',b'\t\t\t\tpush_error("James West water death polish shared helmet mismatch")']);return b.replace(marker,marker+nl+block,1)
atomic(R/'scripts/grid_canvas.gd',loader)
def registry(b):
    m=json.loads(b);m['actionOverrides']['branforth-west-water-death-polish']='character/james-west-water-death-polish-v1/bare-manifest.json';m['equipmentActionOverrides']['branforth-west-water-death-polish']='character/james-west-water-death-polish-v1/helmet-manifest.json';return (json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode()
atomic(R/'character/ACTIVE_ASSETS.json',registry)
for mode in ['bare','helmet']:
    def status(b):
        m=json.loads(b);m['status']='installed_owner_review_pending';return (json.dumps(m,indent=2)+'\n').encode()
    atomic(P/(mode+'-manifest.json'),status)
(P/'selection.json').write_text(json.dumps(dict(status='installed_owner_review_pending',runtimeInstalled=True,fullSetComplete=False,statesPerMode=1,refsPerMode=6,source='../james-death-west-v1/source-water-v4.png',pending=['Final installed player/mortality/disk-restore checks','Owner and full-set motion/journey acceptance']),indent=2)+'\n')
print('Installed paired West water death override; other death states/clocks/swim entry unchanged')
