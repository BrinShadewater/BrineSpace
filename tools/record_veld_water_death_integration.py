"""Record current normal-loader evidence without relabelling dated source proofs."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent.parent
O=R/'character/veld-water-death-entry-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    entry=R/'output/veld-water-death-entry-v1';cont=R/'output/veld-water-death-continue-v1'
    reports=[json.loads((p/'validation.json').read_text()) for p in [entry,cont]]
    assert all(x['passed'] and not x['realProfileChanges'] for x in reports)
    summary=[]
    for folder,marker in [(entry,'VELD LIVE WATER DEATH ENTRY:'),(cont,'VELD WATER DEATH CONTINUE:')]:
        lines=(folder/'native.log').read_text(encoding='utf-8').splitlines()
        summary.append(next(s for s in lines if s.startswith(marker)))
    O.mkdir(exist_ok=True)
    bound={}
    def bind(p):bound[p.relative_to(R).as_posix()]=sha(p)
    for path in ['scripts/veld_death_motion.gd','scripts/veld_death_motion.gd.uid','scripts/veld_npc.gd','scripts/grid_canvas.gd','scripts/room_flooding.gd','character/ACTIVE_ASSETS.json','tests/index.json','tests/test_veld_water_death_entry.gd','tests/test_veld_water_death_entry.gd.uid','tests/test_veld_water_death_continue.gd','tests/test_veld_water_death_continue.gd.uid','tools/run_veld_water_death_entry.py','tools/run_veld_water_death_continue.py','character/veld-consistency-audit-v2/build_coverage.py','character/veld-consistency-audit-v2/coverage.json','character/veld-consistency-audit-v2/dry-death-recheck.json']:
        bind(R/path)
    for family in ['veld-death-water-prone-family-v1','veld-death-water-tread-family-v1']:
        for gear in ['bare','helmet']:
            p=R/'character'/family/(gear+'-manifest.json');bind(p)
            for state in json.loads(p.read_text())['states']:
                for f in state['frameFiles']:bind((p.parent/f).resolve())
    for folder in [entry,cont]:
        for f in ['validation.json','native.log','profile-before.json','profile-after.json']:bind(folder/f)
    bind(entry/'native-contact.png')
    (O/'evidence.json').write_text(json.dumps({'date':'2026-10-01','normalLoader':True,'summaries':summary,'reports':reports,'sha256':bound,'remaining':['wet cargo/gesture/turn entrance coverage','furnished corpse render and collision/occlusion review','death pitch/body-center/material/detail polish','dry death/rest/life and full animation set/polish']},indent=2)+'\n',encoding='utf-8')
    result='; '.join(summary)
    handoff=f'''# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Veld normal water death and disk Continue

## Objective and acceptance
Complete the matching Veld animation set, then cross-family consistency and motion polish. This milestone installs sixteen cardinal wet-death states and proves live entrance/restore behavior; the full goal remains active.

## Accepted decisions and constraints
Retain matte directional masters, original independently authored cameras, equipment handedness, 256 canvas/pivot128/standingHeight148 and finite corpse endpoints. Preserve existing dry behavior, room furniture and resource failure rules. Second Chance executes before Veld captures death entry.

## Current state
grid_canvas.gd and ACTIVE_ASSETS.json select prone/tread family pairs. New veld_death_motion.gd captures the last actually drawn whole frame, saves selectors/source gear/target gear/start clock/partial pitch index, holds it180ms and then uses authored finite interiors. veld_npc.gd persists validated metadata; room_flooding.gd invokes its hook. Both native tests/UIDs/runners are indexed. Source-stage reports retain their original staged scope; current selected integration evidence is evidence.json.

## Verification
{result}. Native incoming/interior/terminal station-scale board reviewed. The Continue fixture writes and reads a real scratch disk checkpoint, discards the scene and uses staged Continue with newly loaded players for4directions×2gears×3phases. Exact pixels, selectors, world anchor, clock, paused hold and terminal after normal draining pass. Both passing intervals preserve all2,920 real non-log profile files. Prior failed entry intervals include last_session.json deltas during concurrent interactive gameplay; failed Continue setup intervals preserved all owner files. Logs retained, no retroactive clean-profile claim.

## Next action
Test actual cargo/gesture/turn incoming poses and furnished corpse draw/occlusion. Polish pitch continuity/body center/head/materials, especially north/south changing camera views. East dry-collapse raw source begun in character/veld-death-ground-east-coherent-v1 (exec-341162b9-d481-49a5-bb1f-c39735c3245c):6poses, prompt/reference/source hashes retained; fitting/grade/paired helmet/native proof pending. Continue dry death/rest/life coverage and full-set matching. No owner visual acceptance, title-button automation, separate process launch or release certification claimed. No commit/push/export.
'''
    (O/'HANDOFF.md').write_text(handoff,encoding='utf-8')
    url='../../output/veld-water-death-entry-v1/native-contact.png?v='+sha(entry/'native-contact.png')[:12]
    (O/'index.html').write_text(f'''<!doctype html><meta charset="utf-8"><title>Veld water death — installed entry and Continue</title><style>body{{background:#202a30;color:#e2e8ec;font:16px sans-serif;max-width:1000px;margin:28px auto}}a{{color:#9ad2ed}}img{{max-width:100%}}</style><h1>Veld — installed water death</h1><p>Exact live incoming pose → authored collapse → finite corpse. Four directions, bare and canonical helmet. This board shows the incoming, first authored and terminal frames at82px standing scale.</p><p>{result}</p><p>Fresh-scene disk staged Continue retains exact entrance, interior and terminal pixels and clocks. Full animation set and visual polish remain in progress.</p><p><a href="../veld-death-water-tread-family-v1/?v=assembled-v1">Finite directional playback and masters</a> · <a href="HANDOFF.md">Scope and remaining work</a> · <a href="evidence.json">Bound checks</a></p><img src="{url}" alt="Eight directional gear rows; incoming, first authored and corpse pose"></html>''',encoding='utf-8')
    heading='## Veld live water-death selection and disk Continue — October 1, 2026'
    lesson=f'''\n\n{heading}

Sixteen cardinal prone/upright wet-death states now selected by the normal loader.
{result}. Passing intervals each preserve all2,920 owner non-log files under scratch APPDATA. Live incoming texture, independent source/target gear, death clock and partially completed pitch are saved as validated selectors; first180ms holds the actual last drawn whole pose, then finite authored interiors/corpse. Fresh-scene disk staged Continue reloads exact pixels/clock/anchor at entry, interior and terminal for both gears/all4directions. Normal draining skips the dead actor and retains the corpse. Old empty metadata remains readable.

Lessons: oxygen exhaustion sets distress flags before kill, so re-querying semantic live state can capture a frame never drawn. Cache the last actual renderer result; serialize row/index/gear/clock, never Texture objects. Rebuild navigation before testing partial transitions after actor restoration. Wake recovery requires an unpaused station; exercise normal Flood.advance for corpse draining, since direct step_crew is a live-actor primitive. Source/candidate tests and fresh-scene disk Continue are distinct evidence. Preserve failed logs/profile deltas; a later clean interval does not erase earlier concurrent last_session.json changes.

Selected inventory refreshed:177bare/171helmet states,2,972frame refs,zero RGBA/path failures. res:// frame references resolve from the project root; relative references resolve from their manifest. Current dry-death page visibly retains orange/larger helmet and blue-grey suit drift; all8dry-death paths match the retained audit, while historical pixel equality is unproven because that old report did not bind hashes. Recover an existing site pod for the Continue survivor; anonymous counts cannot override the normal all-characters-lost rule.

Native station-scale entrance/first-interior/corpse board reviewed; pitch/body-center/head/material/detail polish and broader cargo/gesture/turn entrances plus furnished corpse occlusion remain. East dry-collapse raw candidate source saved:exec-341162b9-d481-49a5-bb1f-c39735c3245c,6poses, exact prompt/source/master hashes; not selected, fitting/grade/paired helmet/native proof pending. Source RGB haze may be alpha0; composite before diagnosing glow from raw RGB. Dry death/rest/life/full-set coverage and final cross-animation matching remain. Full goal active; no full visual acceptance/commit/export. Handoff: character/veld-water-death-entry-v1/HANDOFF.md.
'''
    art_lesson=f'''\n\n{heading}

Veld wet death now uses the matched cardinal source families in normal play. Preserve the actual last drawn whole pose at entry: replacing it with an idle or newly queried distress frame creates an identity/posture jump. Continue must retain the same palette, canonical helmet and camera pose after loading a fresh scene. Native82px incoming/interior/corpse board reviewed; pitch/body-center/head/detail polish remains, especially north/south view changes.

The refreshed selected inventory still shows older dry-death orange/larger helmets and cooler suit material beside the corrected cargo family. Coverage is not identity acceptance. New east dry-collapse source preserves grounded lowering and head support; raw source is not yet fitted/graded/selected. Allow crown-to-floor height to decrease physically, while keeping one anatomical ruler. RGB haze in alpha0pixels is invisible: inspect composited edges before treating raw RGB as glow. Remaining dry rest/life/death and cross-family motion/material polish remain open. Evidence: character/veld-water-death-entry-v1/HANDOFF.md.
'''
    skill_lesson=f'''\n\n{heading}

At an irreversible animation transition, capture the last actually drawn whole texture, not a semantic re-query after gameplay flags change. Oxygen exhaustion sets low-air before death, which can otherwise capture an unseen distress frame. Keep cached textures ephemeral; serialize validated row/index, source and target gear, start clock and completed pitch. Preserve the base actor state and finite terminal pose. Run Second Chance before the hook.

Test in-memory actor/player restore and fresh-scene disk staged Continue separately. The latter must actually write/read a checkpoint, discard the scene and load new players; stop on write failure to avoid testing an older save. Restore live navigation before partial-transition fixtures. Wake core recovery unpaused; use an existing recovered site pod as survivor because an anonymous count cannot override all-characters-lost. Drain corpses through normal Flood.advance; step_crew is a live-actor primitive. Resolve res:// frame paths from project root and relative paths from their manifests. Keep failed logs/profile deltas; a clean later interval does not erase them. {result}. Full-set identity and furnished world evidence remain separate.
'''
    docs={'docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md':lesson,'docs/ASSET_PIPELINE_AND_WORKFLOW.md':lesson,'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md':art_lesson,'skills/brinespace-character-pipeline/references/crew-consistency.md':skill_lesson}
    for path,content in docs.items():
        p=R/path
        if heading.encode() not in p.read_bytes():
            with p.open('ab') as f:f.write(content.encode())
    installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
    if heading.encode() not in installed.read_bytes():
        with installed.open('ab') as f:f.write(skill_lesson.encode())
    p=R/'docs/CURRENT_STATUS.md'
    status=f'''{heading}

Sixteen cardinal wet-death states selected locally. {result}. Both passing intervals preserve all2,920 real non-log files. Exact last drawn entrance180ms, source/target gear, partial pitch and finite corpse persist; fresh-scene disk staged Continue proves exact pixels/clock/anchor at3phases×4directions×2gears. Source-stage reports retain their original scope. Native station-scale board reviewed; broader wet roles/turns and furnished corpse occlusion plus pitch/material/detail polish remain.

Selected inventory177bare/171helmet states/2,972refs,zero path/RGBA failures; current dry-death frames still show old helmet/material drift. New east dry-collapse raw6pose source saved with exact prompt/master binding, fitting/grade/paired helmet/native proof pending. Skills/pipeline/bible updated. Remaining rest/life/drydeath/full-set matching and final polish remain; full goal active. [Handoff](../character/veld-water-death-entry-v1/HANDOFF.md).

'''
    if heading.encode() not in p.read_bytes():p.write_bytes(status.encode()+p.read_bytes())
    print(json.dumps({'boundFiles':len(bound),'summaries':summary,'handoff':str(O/'HANDOFF.md')}))
if __name__=='__main__':main()
