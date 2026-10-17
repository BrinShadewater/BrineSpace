from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'selected-join-audit-v9'
path=out/'audit.json';old=path.read_bytes();data=json.loads(old)
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in data['inputs'].items())
for gear,count in [('bare',1169),('helmet',1601)]:
    changes=data['gears'][gear]['transitions']
    assert changes[2]['upperRegionChangedRgbaPixels']==count
    assert all(x['upperRegionChangedRgbaPixels']==0 for i,x in enumerate(changes) if i!=2)
def atomic(path,old,new):
    assert path.read_bytes()==old
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(temp,path)
data.update(visualReviewPending=False,artworkChanged=False,
    finding='All fourteen registered source/reference presentations plus twelve enlarged collar crops inspected. Head/collar orientation switches abruptly between zero-based interiors2 and3; shoulder articulation also changes. Upper110 rectangle exact elsewhere,1169 bare/1601 helmet RGBA differences at join. Alpha32 crown148→149 bare,156→158 helmet relative fixed224 pivot; these are diagnostic crown distances, not anatomical body height or head-only counts. Preserve reference identity; next coherent paired intermediate upper-body articulation, not another narrow collar-only patch or whole-body rescale.')
atomic(path,old,(json.dumps(data,indent=2)+'\n').encode())
section='''### James selected West join isolated — October 2, 2026

Current normal V9 paired bridge audited at original256 canvas/p128224/H148,
beside selected registered idle reference. Fourteen full source/reference poses
and twelve enlarged neck/shoulder crops reviewed. Upper0..109 rectangle stays
byte-exact at every neighbor except zero-based frame2→3:1169bare/1601helmet RGBA
pixels change in that single80ms step. Crown distance at alpha32 changes148→149
bare,156→158helmet; lowest visible sole rows vary223..225. These are region/crown
diagnostics, not anatomical height measurements or head-only difference counts.
No pose normalization/translation/grade or selected artwork change. Visual source
review confirms abrupt head/collar orientation alongside shoulder change; a tiny
collar-only patch cannot distribute the missing upper-body articulation. Next
coherent paired intermediate head/collar/shoulder pose preserving master identity,
original endpoints, foot/root and source material. Do not globally resize bodies
to fix this source join. Not a full turn/cardinal/master/native-motion audit.
Evidence: character/james-cargo-return-bridges-v1/selected-join-audit-v9/audit.json.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        marker=b'## James normal West cargo integration'
        at=old.index(marker);new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,old,new)
path=r/'character/james-floor-case-west-v1/HANDOFF.md';old=path.read_bytes()
addition=b'\nSelected V9 join isolated at frame2-to3 (upper region1169bare/1601helmet pixels,\ncrown1/2px rise); full sources/collar crops reviewed, no source edits. Audit:\ncharacter/james-cargo-return-bridges-v1/selected-join-audit-v9/audit.json.\nNext paired coherent upper-body intermediate; tiny collar-only patches insufficient.\n'
if b'Selected V9 join isolated' not in old:atomic(path,old,old+addition)
print('Selected join evidence/visual finding recorded; source hashes unchanged; five guides and handoff updated.')
