from pathlib import Path
import json
P=Path(__file__).resolve().parent
packs={gear:json.loads((P/(gear+'-manifest.json')).read_text())['states'] for gear in ['bare','helmet']}
template=(P.parent/'bill-reading-entry-south-v1/build_review.py').read_text()
html=template.split("html='''",1)[1].split("'''",1)[0]
html=html.replace('Bill south tablet transitions','Bill north reading').replace('Bill — south tablet transitions','Bill — north seated reading')
html=html.replace('Take out tablet, read, put it away. Exact seated/reading endpoint joins and native selected helmet. Candidate preview; live stage wiring remains pending.','North reading candidate: gentle head dips and forearm motion, with the tablet held in front of his body and occluded from this rear view. Shared north seated ruler, master matte grade and selected native helmet. Runtime selection and entry/exit joins remain pending.')
(P/'index.html').write_text(html.replace('DATA',json.dumps(packs)),encoding='utf-8')
out='/output/bill-reading-north-sofa-v1/'
images=''.join(f'<figure><figcaption>{gear} · {stage}</figcaption><img src="{out}{gear}-{stage}-03.png"></figure>' for gear in ['bare','helmet'] for stage in ['sit','read','rise'])
(P/'sofa-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill north chair reading review</title><style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}img{width:100%;max-width:1280px}figure{margin:24px 0}a{color:#92d9dc}</style><h1>Bill — north chair reading candidate</h1><p>Actual north lounge chair route and sitting stages, with candidate reading textures injected as the seated presentation. This checks furniture fit and renderer bindings; live reading-service selection remains pending. Observation sofas keep their south-facing art when the room rotates.</p><a href="index.html">Animation preview</a>'+images,encoding='utf-8')
