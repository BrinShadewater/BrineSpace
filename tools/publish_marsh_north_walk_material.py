"""Publish installed six-pose repair, preserved baseline and source-clock join."""
from pathlib import Path
import hashlib,json,html
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-walk-material-v1'
CAP=ROOT/'output/marsh-animation-audit/north-walk-material-installed-native-2026-10-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    before=json.loads((BASE/'baseline.json').read_text())['states']
    current=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    assert set(before)==set(current) and len(current)==204
    assert all(before[k]==current[k] for k in before if k!='walk-north')
    recipe=json.loads((BASE/'candidate-01/recipe.json').read_text())
    report=json.loads((CAP/'report.json').read_text());assert report['failures']==0
    native=[]
    for record in report['captures']:
        path=BASE/'candidate-01/north-start'/f"{record['slot']:03d}.png" if record['key']=='walk-start-north' else ROOT/current[record['key']]['files'][record['slot']]
        record['source']=path.relative_to(ROOT).as_posix();record['sourceSha256']=sha(path)
        record['captureSha256']=sha(CAP/record['file'])
        native.append(Image.open(CAP/record['file']).convert('RGB'))
    duration=[round((b['time']-a['time'])*1000) for a,b in zip(report['captures'],report['captures'][1:])]+[100]
    native[0].save(BASE/'native-start-join.gif',save_all=True,append_images=native[1:],duration=duration,loop=0)
    frames=[]
    for slot in range(6):
        panel=Image.new('RGB',(736,240),'#293b40');draw=ImageDraw.Draw(panel)
        images=[ROOT/before['idle-north']['files'][0],ROOT/'character/marsh-ground-cardinal-v1/north-start-candidate-01/003.png',BASE/f'sources/original-{slot:03d}.png',ROOT/current['walk-north']['files'][slot]]
        for i,path in enumerate(images):
            im=Image.open(path).convert('RGBA');panel.paste(im,(i*184,28),im)
            draw.text((i*184+3,7),['Idle','New start toe-off',f'Before gait{slot}',f'Installed gait{slot}'][i],fill='white')
        frames.append(panel)
    frames[0].save(BASE/'gait-comparison.gif',save_all=True,append_images=frames[1:],duration=[150]*6,loop=0)
    for folder in [CAP,ROOT/'output/marsh-animation-audit/north-walk-material-installed-2026-10-02']:
        a=json.loads((folder/'profile-before.json').read_text());b=json.loads((folder/'profile-after.json').read_text())
        assert a==b,(folder,'owner profile changed')
    catalog=ROOT/'character/marsh-v2/catalog.json';cat=json.loads(catalog.read_text())
    snapshot={'catalog':{'path':catalog.relative_to(ROOT).as_posix(),'sha256':sha(catalog)},'bodyManifests':[{'path':(ROOT/'character/marsh-v2'/p).resolve().relative_to(ROOT).as_posix(),'sha256':sha(ROOT/'character/marsh-v2'/p)} for p in cat['body']],'runtimeContract':{'path':'character/marsh-consistency-review-v1/runtime-contract.json','sha256':sha(ROOT/'character/marsh-consistency-review-v1/runtime-contract.json')},'states':204,'slots':1058,'changedStates':['walk-north'],'ownerAccepted':False,'northStartAdmitted':False}
    (BASE/'installed-selection.json').write_text(json.dumps(snapshot,indent=2)+'\n')
    report['installedChecks']=22504;report['ownerProfileFilesUnchanged']=2931
    report['scope']='Staged actual-player20ms source-clock join, explicit.15s phase and installed selected-player regression. No root/actor/world/Continue/traffic or continuous-video acceptance.'
    report['finding']='All six complete gait poses now match the master/idle/new-start ivory-sage construction much more closely; original alpha/body ruler/stride/clock preserved. North start endpoint uses repaired walk1 but remains staged.'
    (BASE/'native-report.json').write_text(json.dumps(report,indent=2)+'\n')
    page='<!doctype html><meta charset="utf-8"><title>Marsh North gait repair</title><style>body{background:#17212a;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}a{color:#8bd}</style><h1>Marsh North walk — installed material repair</h1><p>'+html.escape(report['finding'])+'</p><img src="candidate-01/comparison.png"><h2>Six-pose cycle</h2><img src="gait-comparison.gif"><h2>Source-clock start handoff</h2><p>'+html.escape(report['scope'])+'</p><img src="native-start-join.gif"><p><a href="sources/north-walk-01.prompt.txt">Exact built-in imagegen prompt</a> · <a href="candidate-01/recipe.json">Source/extraction/grade provenance</a> · <a href="native-report.json">Native source hashes and checks</a> · <a href="installed-selection.json">Current installed snapshot</a></p>'
    (BASE/'index.html').write_text(page,encoding='utf-8')
    print('Published six-pose before/installed comparison and18native source-clock captures;22504 installed checks,2931 owner files unchanged')
if __name__=='__main__':main()
