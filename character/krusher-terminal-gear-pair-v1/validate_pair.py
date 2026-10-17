from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;provenance=json.loads((P/'provenance.json').read_text());checks=0;errors=[]
def check(ok,name):
    global checks
    checks+=1
    if not ok:errors.append(name)
for path,h in provenance['sourceHashes'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'source unchanged '+path)
for variant,record in provenance['masters'].items():check(hashlib.sha256((R/record['path']).read_bytes()).hexdigest()==record['sha256'],'master unchanged '+variant)
for record in provenance['records']:
    a=np.array(Image.open(P/record['output']).convert('RGBA'));source=np.array(Image.open(R/record['source']).convert('RGBA'));master=np.array(Image.open(R/provenance['masters'][record['variant']]['path']).convert('RGBA'))
    check(a.shape==(184,184,4),record['output']+' canvas');check(np.array_equal(a[:62],master[:62]),record['output']+' fixed upper head/helmet');check(np.array_equal(a[62:],source[62:]),record['output']+' exact shared pose body')
for variant in ['bare','helmet']:
    manifest=json.loads((P/f'{variant}-manifest.json').read_text());bare=json.loads((P/'bare-manifest.json').read_text());check(manifest['pivot']==[92,172],variant+' pivot')
    check(hashlib.sha256((P/f'frames/{variant}/idle.png').read_bytes()).hexdigest()==manifest['canonicalIdleSha256'],variant+' exact locomotion idle file')
    for state,original in zip(manifest['states'],bare['states']):
        check(state['frameDurationsMs']==original['frameDurationsMs'],variant+state['id']+' timings');apng=Image.open(P/f'review/{variant}-{state["id"]}.png');check(apng.n_frames==state['frameCount'],variant+state['id']+' count')
        for i,path in enumerate(state['frameFiles']):
            apng.seek(i);check(np.array_equal(np.array(apng.convert('RGBA')),np.array(Image.open(P/path).convert('RGBA'))),path+' APNG');check(round(apng.info['duration'])==state['frameDurationsMs'][i],path+' duration')
    rise,typing,lower=manifest['states'];check(rise['frameFiles'][0]==lower['frameFiles'][-1],variant+' idle aliases');check(rise['frameFiles'][-1]==typing['frameFiles'][0]==typing['frameFiles'][-1]==lower['frameFiles'][0],variant+' held aliases')
result={'checks':checks,'errors':errors,'visualAcceptance':False,'scope':'bare/helmet west terminal paired sources, exact body/upper gear, package/joins'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
