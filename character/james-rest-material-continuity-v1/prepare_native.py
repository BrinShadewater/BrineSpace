from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];old=R/'character/james-sleep-cadence-v1'
s=(old/'validate.gd').read_text(encoding='utf-8').replace('james-sleep-cadence-v1','james-rest-material-continuity-v1').replace('JAMES SLEEP','JAMES REST MATERIAL')
needle='\t\tfor state in pack.states:\n\t\t\tcheck(selected[state.id].size()==6'
extra='''		for source_state in pack.states:
			var elapsed:=0.0
			for i in range(source_state.frameFiles.size()):
				var expected_image:=Image.load_from_file(ProjectSettings.globalize_path((OUT+mode+"-manifest.json").get_base_dir().path_join(source_state.frameFiles[i])))
				var frame:Texture2D=selected[source_state.id][i]
				check(frame.get_image().get_data()==expected_image.get_data(),"All installed rest source pixels "+source_state.id+str(i))
				check(frame.get_meta("crew_pivot")==Vector2(128,224) and frame.get_meta("crew_standing_height")==148.0,"All rest authored density/pivot")
				check(player.frame_at_elapsed(source_state.id,elapsed+.0001,gear).get_image().get_data()==expected_image.get_data(),"All rest source action clocks")
				elapsed+=float(source_state.frameDurationsMs[i])/1000.0
			check(absf(player.cycle_seconds(source_state.id,gear)-elapsed)<.0001,"All rest complete source clocks")
		for state in pack.states:
			if not String(state.id).begins_with("sleep-"):continue
			check(selected[state.id].size()==6'''
assert needle in s;s=s.replace(needle,extra)
s=s.replace('var disk:=Image.load_from_file(ProjectSettings.globalize_path(state.frameFiles[i]))','var disk:=Image.load_from_file(ProjectSettings.globalize_path((OUT+mode+"-manifest.json").get_base_dir().path_join(state.frameFiles[i])))')
s=s.replace('All eight normal loaded sleep states, three visual cycles each;','All144 ordinary rest source references/metadata/clocks through normal loader; all eight sleep states, three visual cycles each;')
(P/'validate.gd').write_text(s,encoding='utf-8');shutil.copy2(old/'no-layout-overrides.json',P/'no-layout-overrides.json')
grid=R/'scripts/grid_canvas.gd';data=grid.read_bytes();needle=b'\t\t\tplayer.load_manifest("res://character/james-water-north-polish-v1/bare-manifest.json", true)'
addition=b'\t\t\tplayer.load_manifest("res://character/james-rest-material-continuity-v1/bare-manifest.json", true)\r\n\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-rest-material-continuity-v1/helmet-manifest.json"):\r\n\t\t\t\tpush_error("James ordinary rest material helmet mismatch")\r\n'
if b'res://character/james-rest-material-continuity-v1/bare-manifest.json' not in data:
    assert data.count(needle)==1;grid.write_bytes(data.replace(needle,addition+needle))
file=R/'character/ACTIVE_ASSETS.json';m=json.loads(file.read_text());m['actionOverrides']['branforth-rest-material']='character/james-rest-material-continuity-v1/bare-manifest.json';m['actionOverrides']['branforth-rest-material-helmet']='character/james-rest-material-continuity-v1/helmet-manifest.json';file.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(P/'selection.json').write_text(json.dumps({'status':'installed_native_validation_pending','runtimeInstalled':True,'fullSetComplete':False,'sourceReferences':144,'materialChangesOnly':True},indent=2)+'\n',encoding='utf-8')
print('Full ordinary rest material pair installed after cadence; all-reference/native berth/Continue fixture prepared.')
