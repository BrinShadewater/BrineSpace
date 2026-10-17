"""Provisionally select held-reviewed/native-verified complete run02 sources."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-run-material-v1'
evidence=json.loads((BASE/'actor-review-v1/verification.json').read_text());assert evidence['checks']==444 and evidence['failures']==0 and evidence['visualReviewed'] and evidence['actorPlayerRestores']==6
catalog=ROOT/'character/marsh-v2/catalog.json';data=json.loads(catalog.read_text());entry='../marsh-west-run-material-v1/candidate-02/manifest.json'
if entry not in data['body']:data['body'].append(entry)
catalog.write_text(json.dumps(data,indent=2)+'\n')
selection={'normalAdmission':True,'status':'provisional complete run02; full normal checkpoint/Continue validation pending','manifest':'candidate-02/manifest.json','manifestSha256':hashlib.sha256((BASE/'candidate-02/manifest.json').read_bytes()).hexdigest(),'artAcceptance':'Master-matched fitted body/material and alternating leg phases reviewed; continuous contacts, full-family/equipment joins and polish remain open.','fullGoalComplete':False};(BASE/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
print('Normal catalog provisionally selects run-west02; full checkpoint proof pending.')
