"""Select reviewed whole South damage sources provisionally; no art rewrite."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def main():
    dry=ROOT/'character/marsh-south-collapse-material-v1'
    injury=ROOT/'character/marsh-south-injury-material-v1'
    for base,checks in [(dry,249),(injury,404)]:
        evidence=json.loads((base/'actor-review-v1/verification.json').read_text())
        assert evidence['checks']==checks and evidence['failures']==0 and evidence['visualReviewed']
    catalog=ROOT/'character/marsh-v2/catalog.json';data=json.loads(catalog.read_text())
    entries=['../marsh-south-collapse-material-v1/candidate-01/manifest.json','../marsh-south-injury-material-v1/candidate-01/manifest.json']
    for entry in entries:
        if entry not in data['body']:data['body'].append(entry)
    catalog.write_text(json.dumps(data,indent=2)+'\n')
    for base in [dry,injury]:
        selection={'normalAdmission':True,'status':'provisional whole-body material selection; full normal save/Continue verification pending','manifest':'candidate-01/manifest.json','manifestSha256':hashlib.sha256((base/'candidate-01/manifest.json').read_bytes()).hexdigest(),'artAcceptance':'Improved matte ivory/sage boots/body. Head/torso, prone foreshortening and moving/family polish remain open.','fullGoalComplete':False}
        (base/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
    print('Normal catalog selects three reviewed South damage states provisionally; full save/Continue proof pending.')
if __name__=='__main__':main()
