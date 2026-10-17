from pathlib import Path
import json
P=Path(__file__).resolve().parent;path=P/'world-review-evidence.json';data=json.loads(path.read_text());assert len(data['boards'])==20 and data['nativeSourcePairs']==228
data['visualReview']='all20boards-reviewed'
data['visualCriteria']=['all228source-native pairs inspected','matching paused saved source and native sofa/floor position','all recorded reference/resumed source-change presentations inspected','both gear/prop branches retain reviewed matte body/head and attached shell','supported-to-floor full silhouette visible in registered crop']
data['visualLimits']='Chronological saved/future native boards; four separate complete30fps native sequences also inspected as contact sheets. Prescribed world mortality/paused-world actor stepping, not natural hazards/traffic/title/new-process or final owner acceptance.'
path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print('All20world boards /228source-native pairs reviewed')
