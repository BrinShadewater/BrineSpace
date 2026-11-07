"""Admit reviewed West whole-body damage sources as provisional normal art."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def main():
    sources=[('marsh-west-collapse-material-v1','candidate-02',249),('marsh-west-injury-material-v1','candidate-01',404)]
    for folder,candidate,checks in sources:
        evidence=json.loads((ROOT/'character'/folder/'actor-review-v1/verification.json').read_text())
        assert evidence['checks']==checks and evidence['failures']==0 and evidence['visualReviewed']
    catalog=ROOT/'character/marsh-v2/catalog.json';data=json.loads(catalog.read_text())
    for folder,candidate,checks in sources:
        entry=f'../{folder}/{candidate}/manifest.json'
        if entry not in data['body']:data['body'].append(entry)
    catalog.write_text(json.dumps(data,indent=2)+'\n')
    for folder,candidate,checks in sources:
        base=ROOT/'character'/folder;manifest=base/candidate/'manifest.json'
        selection={'normalAdmission':True,'status':'provisional whole-body selection; full normal save/Continue verification pending','manifest':f'{candidate}/manifest.json','manifestSha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'artAcceptance':'Warm ivory/sage exact complete bodies, ivory boot uppers and charcoal sole material retained. First dip/head/torso/prone foreshortening and full moving/family polish remain open.','fullGoalComplete':False}
        (base/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
    print('Selected three West damage states provisionally in normal catalog.')
if __name__=='__main__':main()
