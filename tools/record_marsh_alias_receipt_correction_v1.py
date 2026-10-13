"""Bind corrected catalogue-byte provenance without rerunning unchanged native art."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-v2/supplemental/cargo-unload-matched-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=BASE/'verification.json';r=json.loads(p.read_text())
r['admissionReceiptSha256']=sha(BASE/'admission.json')
r['postNativeProvenanceCorrection']={'beforeCatalogueFile':'catalog-before.json','sha256':sha(BASE/'catalog-before.json'),'scope':'Before catalogue hash initially normalized LF. Recovered exact CRLF bytes match two independent pre-alias frozen hashes. Installer now hashes/copies original bytes before mutation. Only installer and admission receipt changed after native test; other5306bounded inputs unchanged. Native probe/current catalogue/manifests/art unchanged.','currentFingerprint':'output/marsh-animation-audit/cargo-unload-alias-player-v1-2026-10-03/inputs-after-receipt-correction.json'}
p.write_text(json.dumps(r,indent=2)+'\n')
inventory=ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-cargo-alias/inventory.json'
r=json.loads(inventory.read_text());r['heldReviewEvidence']['aliasVerificationSha256']=sha(p)
inventory.write_text(json.dumps(r,indent=2)+'\n')
note='''
### Marsh alias catalogue-byte provenance correction — October 3, 2026

Final provenance check found before-catalogue hash was computed from normalized
LF JSON rather than original Windows CRLF file bytes. Reconstructed exact CRLF
catalog-before.json matches both pre-alias inventory and previous frozen input
hash; correction and method recorded. Installer now copies/hashes raw original
bytes before mutation. After native proof, only installer and admission receipt
changed among5308bounded inputs;5306others (including current catalogue, manifests,
art, runtime and native probe) remain identical. Native test's original before/
after interval remains unchanged evidence. Corrected receipt bound in verification.
Lesson: provenance checks must hash actual bytes, not reserialized JSON; semantic
equivalence and newline normalization cannot be reported as byte equality.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for q in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with q.open('rb') as f:f.seek(max(0,q.stat().st_size-100000));tail=f.read().decode('utf-8',errors='ignore')
    if '### Marsh alias catalogue-byte provenance correction' not in tail:
        with q.open('a',encoding='utf-8') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('Corrected byte provenance bound;5306other inputs unchanged;lesson appended to pipeline/bible/status/skill')
