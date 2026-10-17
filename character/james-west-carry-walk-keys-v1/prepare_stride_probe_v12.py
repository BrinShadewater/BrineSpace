from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'paired-v12'
template=p/'paired-v11/native_probe.gd'
source=template.read_text().replace('paired-v11','paired-v12')
needle='\t# Continuous render clock: three full loops, no source-change waits or extra holds.'
tests='''
	# Exercise the actual movement-driven player, at three speeds, both gears.
	var stride: float=pack.strideDistanceCells["carry-west"]
	var distance_samples := 0
	var pause_checks := 0
	for equipment in ["", "diving-helmet"]:
		for speed in [0.045,0.09,0.18]:
			player.load_manifest(PACK)
			check(player.load_equipment_manifest("diving-helmet",HELMET),"Distance profile loaded")
			var selected: Array=player.frames["carry-west"] if equipment.is_empty() else player.equipment_frames[equipment]["carry-west"]
			var initial: Texture2D=player.frame("carry","west",0.0,Vector2.ZERO,equipment)
			check(initial==selected[0],"Movement starts phase0")
			check(player.frame("carry","west",2.0,Vector2.ZERO,equipment)==initial,"Stationary start holds, no time-driven gait")
			pause_checks+=1
			var milliseconds := 0.0
			var paused_time := 0.0
			for slot in range(49):
				var midpoint: float=(milliseconds+float(durations[slot])/2.0)/1000.0
				var distance := stride*midpoint/1.68
				var time: float=100.0+distance/speed+paused_time
				var position := Vector2(-distance,0)
				var actual: Texture2D=player.frame("carry","west",time,position,equipment)
				check(actual==selected[slot],"Distance phase independent of elapsed speed")
				check(actual.get_meta("crew_pivot")==Vector2(128,224),"Distance pivot retained")
				distance_samples+=1
				if slot==24:
					paused_time+=2.0
					check(player.frame("carry","west",time+2.0,position,equipment)==actual,"Midstride stationary pause holds exact pose")
					pause_checks+=1
				milliseconds+=float(durations[slot])
			var wrap_distance := stride*1.000001
			check(player.frame("carry","west",110.0+wrap_distance/speed,Vector2(-wrap_distance,0),equipment)==selected[0],"Distance cycle wraps to source0")
	var natural_players: Array=[]
	for equipment in ["", "diving-helmet"]:
		var np=load("res://scripts/crew_sprite_player.gd").new()
		np.load_manifest(PACK)
		np.load_equipment_manifest("diving-helmet",HELMET)
		np.frame("carry","west",0.0,Vector2.ZERO,equipment)
		natural_players.append(np)
'''
assert needle in source
source=source.replace(needle,tests+'\n'+needle)
source=source.replace('board.textures=[player.frame_at_elapsed("carry-west",phase),player.frame_at_elapsed("carry-west",phase,"diving-helmet")]',
                      'var position := Vector2(-seconds*stride/1.68,0)\n\t\tboard.textures=[natural_players[0].frame("carry","west",seconds,position),natural_players[1].frame("carry","west",seconds,position,"diving-helmet")]')
source=source.replace('"sourceSamples":98,','"sourceSamples":98,"distanceSamples":distance_samples,"stationaryChecks":pause_checks,"strideDistanceCells":stride,')
source=source.replace('three continuous wall-clock render loops','three continuous distance-driven render loops')
source=source.replace('No actual cargo scheduler, walking-distance stride, room,','Three speeds and stationary holds verified. No actual cargo scheduler, room,')
source=source.replace('JAMES PAIRED49:', 'JAMES DISTANCE49:')
(out/'native_probe.gd').write_text(source,encoding='utf-8')
files=[template,Path(__file__),out/'native_probe.gd',out/'bare-manifest.json',out/'helmet-manifest.json',r/'scripts/crew_sprite_player.gd',r/'character/james-side-motion-review-2026-10-02/run_validation.py']
for kind in ('bare','helmet'):
 m=json.loads((out/(kind+'-manifest.json')).read_bytes())
 files.extend(r/f[6:] for f in m['states'][0]['frameFiles'])
(out/'native-inputs.json').write_text(json.dumps({'preLaunchSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Distance probe and input inventory prepared.')
