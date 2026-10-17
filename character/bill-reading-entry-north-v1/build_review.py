from pathlib import Path
import json
P=Path(__file__).resolve().parent
packs={}
for gear in ['bare','helmet']:
    states=json.loads((P/(gear+'-manifest.json')).read_text())['states']
    read=json.loads((P.parent/'bill-reading-north-v1'/(gear+'-manifest.json')).read_text())['states'][0]
    read['frameFiles']=['../bill-reading-north-v1/'+file for file in read['frameFiles']]
    packs[gear]=[states[0],read,read,states[1]]
template=(P.parent/'bill-reading-entry-south-v1/build_review.py').read_text()
html=template.split("html='''",1)[1].split("'''",1)[0]
html=html.replace('Bill south tablet transitions','Bill north tablet transitions').replace('Bill — south tablet transitions','Bill — north tablet transitions')
html=html.replace('Take out tablet, read, put it away. Exact seated/reading endpoint joins and native selected helmet. Candidate preview; live stage wiring remains pending.','Take out the tablet from the right belt pouch, read, then put it away. Exact selected north seated and new reading endpoints; fixed source rulers, shared matte grade and native helmet. Candidate preview; live north stage wiring and selection remain pending.')
html=html.replace('<p><a href="sofa-review.html">Native observation sofa review</a></p>','<p><a href="../bill-reading-north-v1/sofa-review.html">North reading loop in the actual lounge chair</a></p>')
(P/'index.html').write_text(html.replace('DATA',json.dumps(packs)),encoding='utf-8')
