from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent;R=H.parents[1];O=R/'output/veld-full-expedition-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
validation=json.loads((O/'validation.json').read_text());report=json.loads((H/'expedition-review-v1/report.json').read_text())
assert validation['passed'] and not validation['realProfileChanges'] and report['failures']==0 and report['checks']==18307
rows=report['journeys'];assert len(rows)==6 and sum(r['restored'] for r in rows)==4
assert {r['rotation'] for r in rows if r['mode']=='delivery'}=={0,1,2,3}
paths=[R/'tools/review_veld_full_expedition_v1.gd',R/'tools/run_veld_full_expedition_validation_v1.py',R/'assets/environment/sub-biomes-v1/sub_biome_view.gd',R/'assets/environment/seabed-v1/seabed_background.gd',R/'scripts/crew_expedition.gd',R/'scripts/run_save.gd',R/'scripts/grid_canvas.gd',O/'native.log',O/'validation.json',H/'expedition-review-v1/report.json',H/'candidate-clearance-profile-v1.json']
for r in rows:
    paths.extend(H/'expedition-review-v1'/c['file'] for c in r['captures'])
for family in ['veld-salvage-pickup-family-coherent-v1','veld-swim-carry-matrix-coherent-v1',H.name]:
    paths.extend(R/'character'/family/(g+'-manifest.json') for g in ['bare','helmet'])
frameHashes=json.loads((H/'route-evidence-v1.json').read_text())['frameHashes']
assert all(sha(R/p)==v for p,v in frameHashes.items())
e=dict(checks=18307,journeys=6,diskRestores=4,installed=False,validation=validation,frameHashes=frameHashes,hashes={p.relative_to(R).as_posix():sha(p) for p in paths},scope='Real dispatch/needs/airlock/exterior/sample/pickup/cargo return/unload,4 rotations,empty and loaded recalls,4 loaded-return disk restores. Dedicated station and explicit candidates; not full traffic/interruption matrix or owner/full-set acceptance.')
(H/'expedition-evidence-v1.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
title='Veld full sample journeys and loaded restores verified — September 30, 2026'
body='''Six actual expedition journeys pass 18,307 checks: four airlock orientations, empty/loaded recalls, all normal phases and six pickup poses, cargo turns, dry unload and exact extraction/delivery credit. Four loaded-return disk restores preserve exact visible pose and paused position. Engine errors zero; 2,914 owner non-log files unchanged, scratch APPDATA. Native exterior pickup/return and dry unload views reviewed. Fixed an exposed retained-seabed mesh lifetime issue: drawing canvases hold their referenced mesh generation across site rebuild until redraw. Initial loader-return fixture error and mesh-error intervals retained; uncached-prop diagnostic did not resolve it. [Handoff](../character/veld-swim-carry-turn-matrix-coherent-v1/EXPEDITION_HANDOFF.md). Staged Veld art/profile remain unselected; further phase interruptions/traffic and final selection proof remain before promotion. Full goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
    p=R/rel;old=p.read_bytes()
    if title.encode() not in old:p.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Expedition restoration and retained mesh ownership — September 30, 2026

Exercise actual dispatch/oxygen/airlock/outbound/work/pickup/return/drain/unload,
not just hand-built exterior phase dictionaries. Match restore pixels and paused
position and reject engine errors even when phase/delivery assertions pass.
Load staged sprite textures once: body load_manifest returns void, and reloading
textures during restore is not restore coverage. Retained draw commands reference
mesh RIDs; when site restoration rebuilds ground meshes, the drawing canvas must
retain its current generation until redraw replaces those commands. Confirm with
the same native restore journey; uncached prop diagnostics are localization, not
acceptance. Preserve failures and owner profile fingerprints. Six journeys/four
loaded-return restores do not certify every interruption, traffic or complete set.
Evidence: character/veld-swim-carry-turn-matrix-coherent-v1/EXPEDITION_HANDOFF.md.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    if b'Expedition restoration and retained mesh ownership' not in p.read_bytes():
        with p.open('ab') as out:out.write(lesson.encode())
print('18,307 clean journey checks bound to6journeys/4restores/336candidate refs; milestone and lessons recorded.')
