from pathlib import Path
import json
P=Path(__file__).resolve().parent
packs={}
for gear in ['bare','helmet']:
    states=json.loads((P/(gear+'-manifest.json')).read_text())['states']
    by_id={s['id']:s for s in states}
    packs[gear]=[by_id[name] for name in ['sit-down-south','read-seated-enter-south','read-seated-south','read-seated-south','read-seated-exit-south','sit-rise-south']]
    for state in states:
        state['frameFiles']=['/'+f.removeprefix('res://') for f in state['frameFiles']]
template=(P.parent/'bill-reading-entry-south-v1/build_review.py').read_text()
# Reuse the preview UI without executing its source-pack mutation.
html=template.split("html='''",1)[1].split("'''",1)[0]
html=html.replace('Bill south tablet transitions','Bill south seated reading')
html=html.replace('Bill — south tablet transitions','Bill — south seated reading')
html=html.replace('Take out tablet, read, put it away. Exact seated/reading endpoint joins and native selected helmet. Candidate preview; live stage wiring remains pending.','Sit, take out the tablet, read, put it away and stand. Both gear states are selected in the game. This preview shortens the reading hold; the live reading budget remains 12 seconds.')
html=html.replace('sofa-review.html','native-review.html')
(P/'index.html').write_text(html.replace('DATA',json.dumps(packs)),encoding='utf-8')
out='/output/bill-seated-south-selected-sofa-v1/'
images=''.join(f'<figure><figcaption>{gear} · {stage}</figcaption><img src="{out}{gear}-{stage}-02.png"></figure>' for gear in ['bare','helmet'] for stage in ['sit','enter','read','exit','rise'])
(P/'native-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill south selected sofa review</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:24px}a{color:#92d9dc}img{width:100%;max-width:1280px}figure{margin:24px 0}</style><h1>Bill — live south sofa sequence</h1><p>559 native checks pass: normal loader, real sofa route/stages, interruption joins and ten disk restores. Fresh in-game captures, both gear states. The fixture explicitly selects the reading station; this does not prove autonomous goal selection.</p><a href="index.html">Animation preview</a>'+images,encoding='utf-8')
