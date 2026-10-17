from pathlib import Path
import json
P=Path(__file__).resolve().parent
path=P/'neutral-native-review-evidence.json';data=json.loads(path.read_text())
assert len(data['boards'])==14 and data['nativeSourcePairs']==126
data['visualReview']='all14boards-reviewed'
data['visualCriteria']=['all126source/native presentations inspected','neutral first/last reader entrance remains empty-handed','attached gloves/waist and unchanged head/helmet through bounded patch poses','source standing-master comparison and native sofa/floor visibility inspected']
data['visualLimits']='Static chronological boards; not continuous recorded native motion, world mortality, ordinary RunSave future Continue or final owner acceptance.'
path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'boardsReviewed':14,'sourceNativePairs':126}))
