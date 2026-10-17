"""Preserve prior probes while deriving normal-loader integration evidence."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
specs=[
 ('approach','test_veld_bunk_body_approach','veld-bunk-body-approach-v1','2 natural chooser/route/activity cases',600),
 ('partial','test_veld_bunk_body_settle','veld-bunk-body-settle-v1','80 partial actor deaths,320 actor-file restores',600),
 ('settle','test_veld_bunk_body_settle_resume','veld-bunk-body-settle-resume-v1','4 fresh disk restores',750),
 ('early','test_veld_bunk_early_fall_native','veld-bunk-early-fall-native-v1','8 fresh disk restores',750),
 ('fire','test_veld_bunk_body_fire_resume','veld-bunk-body-fire-resume-v1','6 fresh disk restores',750),
]
uids=['uid://d0evbknsela1','uid://d0evbknsela2','uid://d0evbknsela3','uid://d0evbknsela4','uid://d0evbknsela5']
rows=[]
for (label,old_name,old_out,success,timeout),uid in zip(specs,uids):
 new_name='test_veld_bunk_selected_'+label;out='veld-bunk-selected-'+label+'-v1'
 s=(R/'tests'/(old_name+'.gd')).read_text(encoding='utf-8').replace(old_name,new_name).replace(old_out,out)
 a=s.index('\tgame.grid_view.veld_player.load_manifest',s.index('func fresh'))
 b=s.index('\treturn game',a)
 assert 'load_manifest' in s[a:b]
 # Read expected source data, but never inject it into the player.
 normal='''	# Production selection only; no fixture manifests may override the player.
	for equipped in [false,true]:
		var pool:Dictionary=game.grid_view.veld_player.equipment_frames["diving-helmet"] if equipped else game.grid_view.veld_player.frames
		for manifest_path in (["res://character/veld-bunk-body-master-v1/helmet-manifest.json","res://character/veld-bunk-early-fall-v1/helmet-manifest.json"] if equipped else ["res://character/veld-bunk-body-master-v1/bare-manifest.json","res://character/veld-bunk-early-fall-v1/bare-manifest.json"]):
			var expected:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
			for clip in expected.states:
				check(pool.has(clip.id) and pool[clip.id].size()==clip.frameFiles.size(),"Normal loader admits complete bunk clip: "+clip.id)
				if not pool.has(clip.id):continue
				for index in clip.frameFiles.size():
					var source=Image.load_from_file(clip.frameFiles[index]);source.convert(Image.FORMAT_RGBA8)
					check(pool[clip.id][index].get_image().get_data()==source.get_data(),"Normally submitted exact bunk source: "+clip.id+" "+str(index))
'''
 s=s[:a]+normal+s[b:]
 assert 'load_manifest(' not in s and 'load_equipment_manifest(' not in s
 (R/'tests'/(new_name+'.gd')).write_text(s,encoding='utf-8')
 (R/'tests'/(new_name+'.gd.uid')).write_text(uid+'\n',encoding='utf-8')
 rows.append({'label':label,'test':new_name,'output':out,'success':'0 failures;'+success,'timeout':timeout,'derivedFrom':old_name})
(P/'native-suites.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Five normal-loader suites prepared; prior staged probes unchanged')
