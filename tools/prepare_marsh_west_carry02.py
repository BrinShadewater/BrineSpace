"""Correct board-position labels without changing West anatomical directions."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-west-carry-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'carry-01.request.json').read_text());assert r['status']=='frozen before generation' and sha(S/'carry-01.prompt.txt')==r['promptSha256']
p=S/'carry-02.prompt.txt';assert not p.exists()
text=(S/'carry-01.prompt.txt').read_text().replace('use RIGHT guide figure for NEAR-leg contact/support and LEFT guide figure for FAR-leg contact/support','use LEFT guide figure for NEAR-leg contact/support and RIGHT guide figure for FAR-leg contact/support').replace('NEAR support/contact, matches RIGHT stance guide','NEAR support/contact, matches LEFT stance guide').replace('FAR support/contact, matches LEFT stance guide','FAR support/contact, matches RIGHT stance guide')
p.write_text(text,encoding='utf-8');r.update(status='frozen before generation',promptSha256=sha(p),supersedesUnusedRequest='carry-01.request.json',reason='Correct guide board positions only: left figure near-leading, right figure far-leading; West screen directions unchanged.')
(S/'carry-02.request.json').write_text(json.dumps(r,indent=2)+'\n')
print('Corrected West reference board-position labels frozen before generation; unused01 preserved.')
