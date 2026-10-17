"""Publish bounded native final-sweep evidence without changing character art."""
from pathlib import Path
import html,json,shutil
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'output/marsh-final-sweep-2026-10-15'
OUT=ROOT/'character/marsh-final-sweep-2026-10-15/review'

def main():
    report=json.loads((EVIDENCE/'report.json').read_text())
    assert report['failures']==0 and len(report['journeys'])==2
    assert len(report['cases'])==30
    assert 'water-salvage-north' in report['journeys'][0]['water_holds']
    log=(EVIDENCE/'native-fixed.log').read_text()
    assert 'SCRIPT ERROR:' not in log and '\nERROR:' not in log
    rest=json.loads((EVIDENCE/'rest-shutdown.json').read_text())
    assert rest['failures']==0 and len(rest['cases'])==1
    rest_log=(EVIDENCE/'rest-shutdown-native.log').read_text()
    assert 'SCRIPT ERROR:' not in rest_log and '\nERROR:' not in rest_log
    OUT.mkdir(parents=True,exist_ok=True)
    groups={}
    for row in report['captures']+rest['captures']:
        label=row['label']
        group=next((room for room in ['galley','crew_hab','observation_room','salvage_workshop'] if label.startswith(room)),None)
        group=group or ('Rest shutdown restore' if row['file'].startswith('rest-shutdown-') else 'Water interruption branches' if label.startswith(('lift','work','settle')) else 'Dry injury and shutdown')
        name=Path(row['file']).stem+'.webp'
        Image.open(EVIDENCE/row['file']).save(OUT/name,lossless=True)
        groups.setdefault(group,[]).append((row,name))
    sections=''
    for title,rows in groups.items():
        sections+=f'<details><summary>{html.escape(title)} · {len(rows)} sampled poses</summary><section>'
        for row,name in rows:
            label=html.escape(row['label'])
            sections+=f'<article><a href="{name}"><img loading="lazy" src="{name}" alt="{label}"></a><p>{label}</p></article>'
        sections+='</section></details>'
    # Preserve a compact cross-family contact board for the handoff.
    picks=[]
    for title,rows in groups.items():
        chosen=rows[len(rows)//2]
        if title=='crew_hab':chosen=next((r for r in rows if 'life_sleep' in r[0]['label']),chosen)
        if title=='observation_room':chosen=next((r for r in rows if 'observation_read' in r[0]['label']),chosen)
        picks.append((title,chosen))
    board=Image.new('RGB',(1500,440*((len(picks)+2)//3)),'#26333c');draw=ImageDraw.Draw(board)
    for i,(title,(row,name)) in enumerate(picks):
        x=i%3*500;y=i//3*440
        board.paste(Image.open(OUT/name),(x,y+40));draw.text((x+8,y+8),title,fill='white')
    board.save(OUT/'native-overview.png')
    north=next(c for c in report['journeys'][0]['captures'] if c['key']=='water-salvage-north' and c['slot']==3)
    shutil.copyfile(EVIDENCE/'north-route'/north['file'],OUT/'north-salvage.png')
    text=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Marsh · final in-game sweep</title><style>body{{background:#142129;color:#dbe4e6;font:16px system-ui;margin:32px auto;max-width:1500px;padding:0 20px}}p{{line-height:1.6;max-width:1050px}}section{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}}article{{background:#26333c;padding:10px;border-radius:8px}}img{{width:500px;max-width:100%;image-rendering:pixelated}}summary{{font-size:22px;margin:25px 0;cursor:pointer}}a{{color:#a7d6cc}}.overview{{width:1500px}}</style><h1>Marsh · final in-game sweep</h1><p>{report['checks']:,} native checks, zero failures. Two actual north-route expeditions, 16 room activity runs, six water interruption branches and four directional dry injury/shutdown runs. Four default corner-lounge configurations remain deliberately excluded.</p><p>Current artwork retained. This controlled sweep uses real dispatch, sea routing, actor updates, default furniture and renderer selection. Activity approaches and damage/death entry points are prescribed. Still images sample pose changes; they are not continuous gameplay video or real-time performance evidence. Other actors and world cycle timers are held. Normal economy/failure flags stay enabled.</p><h2>North-facing salvage reached by actual pathfinding</h2><p>A fixture corridor blocks the eastern approach, so the production route arrives north-facing. All braking and salvage holds, pickup, return, drainage, unloading and delivery complete. No production route or facing rule was changed.</p><img src="north-salvage.png" alt="Native north-facing salvage"><h2>Native pose overview</h2><a href="native-overview.png"><img class="overview" src="native-overview.png" alt="Native room and interruption samples"></a><p>Open each family below to inspect the captured poses at full crop size.</p>{sections}<p>The older shutdown rebuilder test now compares against its declared master-repair stage. Historical provenance checks remain; current runtime shutdown is checked here. No animation source or game behavior change was required.</p><p><a href="../../../docs/MARSH_FINAL_SWEEP_2026-10-15.md">Evidence and handoff</a> · <a href="../../marsh-water-actions-v1/review/index.html">Accepted water source chains</a></p></html>'''
    text=text.replace('Current artwork retained.','Fixed exterior shutdown visibility: clearing the expedition no longer hides Marsh’s body outside the station. Current artwork retained.')
    text=text.replace(f"{report['checks']:,} native checks",f"{report['checks']+rest['checks']:,} native checks")
    text=text.replace('No animation source or game behavior change was required.','Exterior shutdown visibility and rest-contact cleanup now pass regression checks. A mid-climb bunk shutdown writes and restores through the actual save reader. Existing animation sources and gameplay rules are preserved.')
    # Validate every exported native still and every local review asset link.
    import re
    for link in re.findall(r'(?:src|href)="([^"]+)"',text):
        if link.endswith(('.png','.webp')):
            path=OUT/link;assert path.is_file(),path
            with Image.open(path) as image:image.load()
    (OUT/'index.html').write_text(text,encoding='utf-8')
    (OUT/'publication.json').write_text(json.dumps({'nativeChecks':report['checks']+rest['checks'],'failures':0,'journeys':2,'cases':len(report['cases'])+len(rest['cases']),'nativeCrops':len(report['captures'])+len(rest['captures']),'artworkChanged':False,'runtimeFixes':['has_marsh admits dead exterior actor after expedition cleanup','die clears bunk and berth live-stage contact']},indent=2)+'\n')
    print(f"Published {len(report['captures'])+len(rest['captures'])} native pose crops and north-route evidence")

if __name__=='__main__':main()
