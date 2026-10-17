"""Reuse the synchronized water comparison UI with bare and canonical helmet tracks."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-swim-east-coherent-v1'
p=json.loads((HERE/'manifest.json').read_text());files=p['states'][0]['frameFiles']
tracks=[{'label':'Canonical shared helmet · east stroke','files':files},{'label':'Master-relative bare · east stroke','files':['../bill-swim-east-coherent-v1/'+f for f in files]}]
# Review template contains JSON data between two unique source delimiters.
html=(BARE/'index.html').read_text(encoding='utf-8');start=html.index('const tracks=')+len('const tracks=');end=html.index(';let time=',start)
html=html[:start]+json.dumps(tracks)+html[end:]
html=html.replace('Bill east swim master pass','Bill paired east swim master pass').replace('Bill — east swimming master pass','Bill — bare and shared-helmet swimming').replace('Six authored swimming poses, fixed anatomical scale and one frozen suit grade. Shared 960ms comparison clock and water anchor. Candidate staged; equipment fitting, water transitions and native selection remain.','Six authored swimming poses with the exact selected helmet/face component and preserved moving body. Shared 960ms clock and water anchor. Candidates staged; tread/start/stop joins and native selection remain.')
(HERE/'index.html').write_text(html,encoding='utf-8');print('Built paired canonical helmet/bare swimming review')
