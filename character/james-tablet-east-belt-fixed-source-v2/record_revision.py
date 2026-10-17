from pathlib import Path
import json,os
P=Path(__file__).resolve().parent;R=P.parents[1];g=json.loads((P/'generation.json').read_text())
note='''

## James East raw color pulse and controlled lighting revision — October 1, 2026

Full141-frame v1 body/head/tool review confirms separate tablet motion and belt
wrench continuity, but raw82/83 shift skin/suit yellow then green. Background RGB
shifts before key/resample/grade; separate FFmpeg invocation matches imageio RGB
exactly, same decoder implementation. Color tags remain unknown throughout; this
is not proof from independent decoder implementations. Reject source for visible
temporal color pulse. One pooled fixed grade cannot remove changing illumination;
do not remove poses or normalize each frame to hide it. Keep raw/evidence.

One controlled james-tablet-east-belt-fixed-source-v2 submission keeps exact East
master and action wording, adding constant neutral diffuse light/white balance
only. Saved task447781086630402; poll its ledger, never resubmit that folder.
Generation status lives in generation.json. Unselected until full source review,
master ruler/material, shared helmet/endpoints and native NPC/Continue checks.
Old selected East wrench transformation remains. Full James goal stays active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James East raw color pulse and controlled lighting revision' in data:continue
    enc=note.encode('utf-8');updated=enc.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+enc
    tmp=path.with_name(path.name+'.james-lighting-revision.tmp');tmp.write_bytes(updated);os.replace(tmp,path)
print(json.dumps({'taskId':g.get('task_id'),'status':g['status'],'guidesUpdated':5,'productionInstalled':False}))
