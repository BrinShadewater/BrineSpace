"""Provisionally select held-reviewed/native-verified complete run05 sources."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
evidence=json.loads((BASE/'actor-review-v2/verification.json').read_text());assert evidence['checks']==444 and evidence['failures']==0 and evidence['visualReviewed'] and evidence['actorPlayerRestores']==6
catalog=ROOT/'character/marsh-v2/catalog.json';data=json.loads(catalog.read_text());entry='../marsh-south-run-material-v1/candidate-05/manifest.json'
if entry not in data['body']:data['body'].append(entry)
catalog.write_text(json.dumps(data,indent=2)+'\n')
selection={'normalAdmission':True,'status':'provisional complete run05; full normal checkpoint/Continue validation pending','manifest':'candidate-05/manifest.json','manifestSha256':hashlib.sha256((BASE/'candidate-05/manifest.json').read_bytes()).hexdigest(),'artAcceptance':'Master-matched fitted body/material and alternating leg phases reviewed; continuous contacts, full-family/equipment joins and polish remain open.','fullGoalComplete':False};(BASE/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
print('Normal catalog provisionally selects run-south05; full checkpoint proof pending.')
