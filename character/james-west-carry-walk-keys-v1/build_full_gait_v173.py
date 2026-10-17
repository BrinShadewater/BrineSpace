from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1');s=(p/'prepare_full_gait_v172.py').read_text(encoding='utf-8').replace('full-gait-review-v172','full-gait-review-v173')
s=s.replace('rows[state.id][0].get_image().get_data(),"Full cycle wraps to first source"','rows[state.id][-1].get_image().get_data(),"Transition helper endpoint deliberately clamps"')
s=s.replace('''for cycle in [1,2]:
                    check(player.frame_at_elapsed(state.id,elapsed+hold*.5+player.cycle_seconds(state.id,gear)*cycle,gear).get_image().get_data()==source.get_data(),"Multiple-cycle midpoint exact")
                elapsed+=hold''','elapsed+=hold')
needle='    root.size=Vector2i(1200,320);root.content_scale_size=Vector2i.ZERO'
block='''    for mode in range(2):
        var gear: String="" if mode==0 else "diving-helmet"
        var key: String="carry-full-review-west"
        var state: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BODY)).states[0]
        var rows: Array=player.frames[key] if mode==0 else player.equipment_frames[gear][key]
        player.current_key="";player.motion.clear()
        player.frame("carry-full-review","west",0.0,Vector2.ZERO,gear)
        for cycle in range(3):
            var cursor:=0.0
            for i in range(state.frameCount):
                var hold:=float(state.frameDurationsMs[i])/1000.0
                var sample:=float(cycle)*player.cycle_seconds(key,gear)+cursor+hold*.5
                check(player.frame("carry-full-review","west",sample,Vector2.ZERO,gear).get_image().get_data()==rows[i].get_image().get_data(),"Production frame path time-based fixture loops exact")
                cursor+=hold
'''
assert needle in s;s=s.replace(needle,block+needle)
(p/'prepare_full_gait_v173.py').write_text(s,encoding='utf-8')
