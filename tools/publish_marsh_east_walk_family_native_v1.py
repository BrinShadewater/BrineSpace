"""Publish bounded staged-player evidence after checking the isolated interval."""
from pathlib import Path
import hashlib, json, shutil
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/'output/marsh-animation-audit/east-walk-family-detail-player-v2-2026-10-03'
OUT = ROOT/'character/marsh-east-walk-family-detail-v1/native'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
a = json.loads((RUN/'inputs-before.json').read_text())
assert a == json.loads((RUN/'inputs-after.json').read_text())
owner = json.loads((RUN/'owner-before.json').read_text())
assert owner == json.loads((RUN/'owner-after.json').read_text())
r = json.loads((RUN/'report.json').read_text())
assert (r['checks'],r['failures'],r['slots'],r['playerRestores']) == (46,0,6,6)
assert len(r['captures']) == 6
assert int((RUN/'engine-exit.txt').read_text()) == 0
assert not any(x in (RUN/'engine.log').read_text() for x in ['ERROR:','WARNING:','SCRIPT ERROR'])
OUT.mkdir(exist_ok=True)
images, captures = [], []
for capture in r['captures']:
    p = RUN/capture['file']
    im = Image.open(p).convert('RGB')
    assert im.size == (672,490)
    shutil.copyfile(p, OUT/p.name)
    captures.append({'path':(OUT/p.name).relative_to(ROOT).as_posix(),'sha256':sha(p)})
    images.append(im)
pages = []
for number in range(2):
    board = Image.new('RGB',(672,1470))
    for row, im in enumerate(images[number*3:number*3+3]):
        board.paste(im,(0,490*row))
    path = OUT/f'page-{number}.png'
    board.save(path)
    pages.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'reviewed':False})
report = {'report':r,'inputCount':len(a),'ownerNonLogCount':len(owner),
    'intervalStable':True,'engineExit':0,'captures':captures,'pages':pages,
    'runReportSha256':sha(RUN/'report.json'), 'normalAdmission':False,
    'scope':'Normal body/equipment player with staged candidate override in test instances; exact six sources and diagnostic native-density/station-size comparison. No main/grid/world floor contact or native natural actor/cadence/save acceptance.'}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(f"46checks/0failures,6captures/restores;{len(a)}inputs/{len(owner)}owner files unchanged")
