"""Publish retained whole-pose stopping trials and exact native source captures."""
from pathlib import Path
import hashlib,json,html
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-stop-v1'
CAP=ROOT/'output/marsh-animation-audit/north-stop-native-2026-10-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    decisions=json.loads((BASE/'sources/decisions.json').read_text())
    master='character/marsh-motion-polish-v1/sources/north-standing-identity-01.png'
    idle='character/marsh-v2/frames/bare/idle-north/000.png'
    gait1='character/marsh-north-walk-material-v1/candidate-01/001.png'
    gait4='character/marsh-north-walk-material-v1/candidate-01/004.png'
    refs={'north-stop-01':[master,idle,gait1],'north-stop-02':['character/marsh-north-stop-v1/sources/north-stop-01.png',master,idle,gait1],'north-stop-03':['character/marsh-north-stop-v1/sources/north-stop-02.png',master,idle,gait4],'north-stop-04':[gait4,master,idle]}
    refs['north-stop-05']=[gait1,'character/marsh-north-stop-v1/sources/north-stop-02.png',master,idle]
    refs['north-stop-06']=[gait4,'character/marsh-north-stop-v1/sources/north-stop-04.png',master,idle]
    retained=json.loads((BASE/'sources/provenance.json').read_text())
    for key,record in retained.items():
        if key not in refs:refs[key]=[ref['path'] for ref in record['references']]
    for key,record in decisions.items():
        for kind,suffix in [('raw','.png'),('prompt','.prompt.txt')]:
            p=BASE/'sources'/(key+suffix);record[kind]=p.relative_to(ROOT).as_posix();record[kind+'Sha256']=sha(p)
        record['references']=[{'path':p,'sha256':sha(ROOT/p)} for p in refs[key]]
    (BASE/'sources/provenance.json').write_text(json.dumps(decisions,indent=2)+'\n')
    report=json.loads((CAP/'report.json').read_text());assert report['failures']==0
    before=json.loads((CAP/'profile-before.json').read_text())
    assert before==json.loads((CAP/'profile-after.json').read_text())
    states=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    branches={'walk-stop-north':'candidate-02','walk-stop-right-north':'candidate-04'}
    for record in report['captures']:
        source=BASE/branches[record['key']]/f"{record['slot']:03d}.png" if record['key'] in branches else ROOT/states[record['key']]['files'][record['slot']]
        record['source']=source.relative_to(ROOT).as_posix();record['sourceSha256']=sha(source)
        record['captureSha256']=sha(CAP/record['file'])
    for branch,folder in branches.items():
        records=[c for c in report['captures'] if c['branch']==branch]
        images=[Image.open(CAP/c['file']).convert('RGB') for c in records]
        duration=[round((b['time']-a['time'])*1000) for a,b in zip(records,records[1:])]+[150]
        images[0].save(BASE/f'{folder}-native.gif',save_all=True,append_images=images[1:],duration=duration,loop=0)
    report['ownerProfileFilesUnchanged']=len(before)
    report['visualFinding']='Revised silhouette/material fits adjacent idle/gait much more closely than initial broad trial. Opposite branch04 has correct screen-right lift; branch03 repeats wrong leg. First new interior in both retained candidates flexes/lifts more than preceding gait endpoint; soften the entry before motion admission. Contact/phase/root behavior remains unverified.'
    report['mediaScope']='Native source/pivot samples and reconstructed pose-change holds; no actor/root movement or continuous native video.'
    (BASE/'native-report.json').write_text(json.dumps(report,indent=2)+'\n')
    page='<!doctype html><meta charset="utf-8"><title>Marsh North stop trials</title><style>body{background:#17212a;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}a{color:#8bd}</style><h1>Marsh North stop — unselected source trials</h1><p>'+html.escape(report['visualFinding'])+'</p><p>'+html.escape(report['scope'])+'</p>'
    for folder in branches.values():page+=f'<h2>{folder}</h2><img src="{folder}/comparison.png"><img src="{folder}-native.gif"><p><a href="{folder}/recipe.json">Extraction, reference hashes and exact generation provenance</a></p>'
    page+='<h2>Rejected width trial</h2><img src="candidate-01/comparison.png"><p><a href="sources/decisions.json">Retained trial decisions</a> · <a href="native-report.json">Native checks, source/capture hashes and limitations</a></p>'
    (BASE/'index.html').write_text(page,encoding='utf-8')
    print('Published two staged stop families,14native source samples,337checks;first-interior motion refinement remains')
if __name__=='__main__':main()
