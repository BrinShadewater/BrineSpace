"""Recover original CRLF catalogue bytes against two prior frozen hash authorities."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-v2/supplemental/cargo-unload-matched-v1'
read=lambda p:json.loads(p.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
p=BASE/'admission.json';r=read(p)
inventory=read(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-cargo/inventory.json')
prior=read(ROOT/'output/marsh-animation-audit/cargo-normal-v1-2026-10-03/inputs-after.json')
expected=inventory['catalog']['sha256'];assert expected==prior['character/marsh-v2/catalog.json']
serialized=json.dumps(r['catalogBefore'],indent=2)+'\n'
candidates=[serialized.encode(),serialized.replace('\n','\r\n').encode()]
matches=[b for b in candidates if sha(b)==expected];assert len(matches)==1
(BASE/'catalog-before.json').write_bytes(matches[0])
old=r['catalogBeforeSha256'];r['catalogBeforeSha256']=expected
r['postNativeReceiptCorrection']={'oldNormalizedLfHash':old,'originalByteHash':expected,'recoveredFile':'catalog-before.json','method':'Exact JSON serialized CRLF bytes match independent pre-alias inventory and preceding frozen input hash.','scope':'Provenance metadata corrected after native interval. Before JSON content, current catalogue/runtime/art unchanged.'}
p.write_text(json.dumps(r,indent=2)+'\n')
print('Original catalogue CRLF bytes recovered and hash verified against2prior authorities;provenance corrected')
