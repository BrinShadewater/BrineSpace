from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
original=r/'character/james-carry-headcaps-v1/native_probe.gd';source=original.read_text(encoding='utf-8').replace('james-carry-headcaps-v1','james-carry-authored-helmet-v1').replace('candidate-manifest.json','bare-manifest.json')
source=source.replace('var checks := 0','const HELMET := "res://character/james-carry-authored-helmet-v1/helmet-manifest.json"\nvar checks := 0')
source=source.replace('player.load_manifest(PACK)','player.load_manifest(PACK)\n\tcheck(player.load_equipment_manifest("diving-helmet",HELMET),"Paired profile loaded")')
source=source.replace('\tfor state in pack.states:', '''\tvar cases: Array = []
\tfor equipment in ["", "diving-helmet"]:
\t\tvar selected_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(PACK if equipment.is_empty() else HELMET))
\t\tfor state in selected_pack.states: cases.append({"state":state,"equipment":equipment})
\tfor item in cases:
\t\tvar state: Dictionary = item.state
\t\tvar equipment: String = item.equipment
\t\tvar active_rows: Dictionary = player.frames if equipment.is_empty() else player.equipment_frames[equipment]
\t\tvar label: String = "bare" if equipment.is_empty() else "helmet"''')
source=source.replace('player.frames.has(state.id)','active_rows.has(state.id)').replace('player.frames[state.id]','active_rows[state.id]').replace('player.cycle_seconds(state.id)','player.cycle_seconds(state.id,equipment)')
source=source.replace('float(milliseconds)/1000.0+.000001)','float(milliseconds)/1000.0+.000001,equipment)').replace('player.frame_at_elapsed(state.id,3.0)','player.frame_at_elapsed(state.id,3.0,equipment)')
source=source.replace('"James bare candidate / "+state.id','"James paired candidate / "+label+" / "+state.id').replace('var file: String = state.id+', 'var file: String = label+"-"+state.id+')
source=source.replace('records.append({"state":state.id','records.append({"equipment":equipment,"state":state.id').replace('"clockSamples":84','"clockSamples":168').replace('Standalone candidate bare player','Standalone candidate paired bare/helmet player').replace('No normal loader, paired helmet,','No normal loader,').replace('JAMES AUTHORED CARRY BARE','JAMES AUTHORED CARRY PAIRED').replace('84clockSamples','168clockSamples')
(p/'native_probe.gd').write_text(source,encoding='utf-8')
manifestFiles=[p/'bare-manifest.json',p/'helmet-manifest.json'];frames=[]
for file in manifestFiles:
    for state in json.loads(file.read_bytes())['states']:
        for ref in state['frameFiles']:
            f=r/ref.removeprefix('res://')
            if f not in frames:frames.append(f)
files=frames+manifestFiles+[p/'native_probe.gd',Path(__file__),r/'scripts/crew_sprite_player.gd',r/'scripts/safe_image.gd',r/'character/james-side-motion-review-2026-10-02/run_validation.py']
(p/'native-inputs.json').write_text(json.dumps({'preLaunchSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'sourcePoseFiles':len(frames),'scope':'Frozen paired standalone source/player/manifest/probe before scratch native test, not normal loader or cargo room.'},indent=2)+'\n',encoding='utf-8')
print('Paired standalone native probe derived from checked bare fixture;10source bodies and helpers/manifests frozen before launch.')
