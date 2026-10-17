from pathlib import Path
import json
P=Path(__file__).resolve().parent
packs={}
for gear in ['bare','helmet']:
    states=json.loads((P/(gear+'-manifest.json')).read_text())['states']
    for state in states:state['frameFiles']=['/'+file.removeprefix('res://') for file in state['frameFiles']]
    by_id={state['id']:state for state in states}
    packs[gear]=[by_id[name] for name in ['sit-down-north','read-seated-enter-north','read-seated-north','read-seated-north','read-seated-exit-north','sit-rise-north']]
template=(P.parent/'bill-reading-entry-south-v1/build_review.py').read_text()
html=template.split("html='''",1)[1].split("'''",1)[0]
html=html.replace('Bill south tablet transitions','Bill north seated reading').replace('Bill — south tablet transitions','Bill — north seated reading')
html=html.replace('Take out tablet, read, put it away. Exact seated/reading endpoint joins and native selected helmet. Candidate preview; live stage wiring remains pending.','Selected north seated/reading family: sit, take out the tablet, read, put it away and stand. Both gear states use the master matte grade and native helmet. The preview shortens the reading hold; the live tablet budget remains 12 seconds. North reading stages are tested explicitly at the real lounge chair; the lounge still chooses resting.')
html=html.replace('sofa-review.html','native-reading-review.html').replace('Native observation sofa review','Native north chair stage review')
(P/'reading.html').write_text(html.replace('DATA',json.dumps(packs)),encoding='utf-8')
out='/output/bill-seated-north-selected-reading-chair-v1/'
images=''.join(f'<figure><figcaption>{gear} · {stage}</figcaption><img src="{out}{gear}-{stage}-02.png"></figure>' for gear in ['bare','helmet'] for stage in ['sit','enter','read','exit','rise'])
(P/'native-reading-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill north selected stage review</title><style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}a{color:#92d9dc}img{width:100%;max-width:1280px}figure{margin:24px 0}</style><h1>Bill — north seated reading stages</h1><p>Normal-loader art, real north chair geometry and approach. Reading stages are scripted after the actual lounge sitting chooser; this is renderer/clock/contact/restore evidence, not autonomous lounge reading.</p><a href="reading.html">Animation preview</a>'+images,encoding='utf-8')
