from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
older=json.loads((r/'character/james-west-cargo-coherent-video-v2/inputs.json').read_bytes())
assert hashlib.sha256((p/'minimax-before.py.txt').read_bytes()).hexdigest()==older['preCallSha256']['tools/minimax_video.py']
job=json.loads((p/'generation.json').read_bytes());assert job['task_id']=='448164031005009'
section='''### James exact endpoint-conditioned video submission — October 2, 2026

Maintained tools/minimax_video.py now supports optional --last-image: switches
only that explicit mode to documented Hailuo02/6s768P, estimatedUSD0.28. Default
Fast2.3/6s768P/USD0.19 unchanged. Validates equal endpoint dimensions/formats/size
before POST, records both path/hash inputs without base64/key, preserves exclusive
ledger and no paid retry. Six offline mocked tests pass: default, endpoint payload,
bad dimensions/no POST, duplicate/no POST, ambiguous failure lock, key redaction.
Unchanged previous helper bytes preserved as minimax-before.py.txt; prior V2 hash
records describe that version, not newly modified helper. No unrelated native tests.

Actual bare carry-turnEastWest010 and unloadWest0 endpoints uniformly4x on equal
1024white canvases, no grade/crop/translation. Both whole inputs inspected. Exact
prompt/source/helper/test hashes frozen. One exclusive job448164031005009, last
verified Processing. New source is unselected; fixed-endpoint conditioning does
not prove anatomy, material, motion or native acceptance. No owner profile access.
Official docs https://platform.minimax.io/docs/api-reference/video-generation-fl2v
and pricing https://platform.minimax.io/docs/guides/pricing-paygo rechecked in prior
interval; estimatedUSD0.28, verified billing unknown. Reserved transfer untouched.

Next poll SAME job, inspect all decoded raw frames and both actual joins before
extraction/equipment/runtime work. Cap/V9/riseV6/caseV7 remain selected. Full James
master/context/cardinal and cross-family goal incomplete; five guides plus direct
video skill/mirror updated. Evidence:character/james-west-endpoint-video-v1.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James continuous V2 source terminal');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
guide='''
## Explicit first/last endpoint mode — October 2, 2026

For a demonstrated endpoint-join failure, optional `--last-image` uses the official
first/last API with MiniMax-Hailuo-02,6s768P at estimatedUSD0.28; ordinary one-image
submissions retain Fast2.3 and USD0.19. It is an explicit scoped source attempt,
not a blanket model migration. Both images must have identical dimensions and
supported formats; freeze actual runtime source hashes and equal registration.
`python tools/minimax_video.py submit --image <first.png> --last-image <last.png> --prompt-file <prompt.txt> --output <new-candidate>`
Records include both path/hash inputs, never their base64 payload or credentials.
Existing exclusive ledger/no automatic paid retry/poll/download rules remain.
Six offline mocked payload/ledger/error/redaction tests pass in
character/james-west-endpoint-video-v1/test_submission.py. Exact endpoints still
do not prove unchanged anatomy, proportions, material or natural motion between
them; inspect every raw frame before extraction and normal admission.
Official API:https://platform.minimax.io/docs/api-reference/video-generation-fl2v
Pricing:https://platform.minimax.io/docs/guides/pricing-paygo
'''
for path in [r/'skills/brinespace-character-pipeline/references/direct-video.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/direct-video.md')]:
    old=path.read_bytes()
    if b'## Explicit first/last endpoint mode' not in old:atomic(path,old+guide.encode())
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James fixed-endpoint video

## Objective and acceptance
Full James matched masters/style/camera/size/height/proportions/matte material,
then cross-family polish. Incomplete; actual source joins and motion must match.

## Accepted decisions and constraints
Cap/V9/riseV6/caseV7 still selected. Reserved transfer untouched. Exact source
endpoints and registration frozen; no normalization, source success not acceptance.

## Current state
Maintained helper optional end-image mode; six mocked tests pass, old helper snapshot
retained. Here first-input.png,last-input.png,prompt.txt,input hashes and exclusive
generation.json; job448164031005009 last verified Processing, unselected.
Five guides and direct-video skill/mirror updated. No profile/native writes.

## Verification
Both actual whole endpoint input images inspected. Uniform4x white composition,
equal1024canvases, no grade/crop/translation. Frozen source/helper/tests hashes.
Six tests cover default/endpoint payload, invalid dimensions, duplicate lock,
ambiguous failure/no retry and key redaction. EstimatedUSD0.28, billing unknown.
Prior V2 tested helper snapshot hash exact; its job terminal and rejected.

## Next action
Poll SAME job448164031005009; never resubmit this ledger. Inspect every decoded
raw frame and both actual endpoints before extraction/equipment/native admission.
Full cardinal/context/master and cross-family polish open. Goal active, no blocker.
''',encoding='utf-8')
print('Endpoint mode6offline tests/current job recorded;five guides and direct-video mirrors updated.')
