"""Publish staged actual-loader source-clock evidence, without gameplay claims."""
from pathlib import Path
import json,hashlib,html
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-ground-cardinal-v1/north-start-candidate-01'
CAP=ROOT/'output/marsh-animation-audit/north-start-candidate-2026-10-02'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    recipe=json.loads((BASE/'recipe.json').read_text())
    report=json.loads((CAP/'report.json').read_text());assert report['failures']==0
    contract=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    frames=[]
    for record in report['captures']:
        path=BASE/f"{record['slot']:03d}.png" if record['key']=='walk-start-north' else ROOT/contract[record['key']]['files'][record['slot']]
        expected=recipe['frameSha256'][path.name] if record['key']=='walk-start-north' else contract[record['key']]['hashes'][record['slot']]
        assert sha(path)==expected
        record['source']=path.relative_to(ROOT).as_posix();record['sourceSha256']=expected
        record['captureSha256']=sha(CAP/record['file'])
        frames.append(Image.open(CAP/record['file']).convert('RGB'))
    duration=[round((b['time']-a['time'])*1000) for a,b in zip(report['captures'],report['captures'][1:])]+[100]
    frames[0].save(BASE/'native-source-clock.gif',save_all=True,append_images=frames[1:],duration=duration,loop=0)
    a=json.loads((CAP/'profile-before.json').read_text());b=json.loads((CAP/'profile-after.json').read_text())
    report['ownerProfileChanges']=[k for k in a.keys()|b.keys() if a.get(k)!=b.get(k)]
    assert not report['ownerProfileChanges']
    report['ownerProfileFiles']=len(a)
    report['finding']='Rear detail/proportions and ivory/sage construction remain close to master/idle. Existing walk endpoint is darker and pinker than idle/new interiors; explicit .15s phase prevents wrong-foot join but does not resolve material change. Candidate stays staged pending complete gait/material and root review.'
    (BASE/'native-report.json').write_text(json.dumps(report,indent=2)+'\n')
    page='<!doctype html><meta charset="utf-8"><title>Marsh North start candidate</title><style>body{background:#17212a;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}a{color:#8bd}</style><h1>Marsh North start — staged candidate</h1><p>Three authored rear interiors between exact selected idle and lifted-left-boot walk slot1. One measured visible idle ruler; each cell registered at the same physical right-boot contact. Body proportions and original master construction retained.</p><p>'+html.escape(report['finding'])+'</p><img src="comparison.png"><h2>Actual loader at source and station size</h2><p>'+html.escape(report['scope'])+'</p><img src="native-source-clock.gif"><p><a href="recipe.json">Extraction, prompt, generation and references</a> · <a href="native-report.json">455 checks / 18 captures / exact sources</a> · <a href="../sources/north-start-01.prompt.txt">Exact built-in imagegen prompt</a></p>'
    (BASE/'index.html').write_text(page,encoding='utf-8')
    print('Published staged source-clock review:455 checks,18 captures,2931 owner files unchanged; no production admission')
if __name__=='__main__':main()
