from pathlib import Path
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1';o=p/'release-death-review-v349';o.mkdir(exist_ok=True)
s=(p/'water-install-review-v347/installed_native_probe.gd').read_text();s=s[:s.index('\tvar union:=Rect2()')]
s=s.replace('water-install-review-v347','release-death-review-v349').replace('water347','death349')
s+='''\tvar foot:=Vector2.INF
\tfor node in npc.room_nodes.get(ORIGIN,[]):
\t\tvar at:Vector2=npc.graph.get_point_position(node)
\t\tif npc.can_stand(at) and npc.swim_segment_clear(at,at,"north","north",true):foot=at;break
\tcheck(foot.is_finite(),"Actual workshop supports native terminal pose fixture")
\tif not foot.is_finite():quit(2);return
\tvar cases:=0
\tfor gear in ["","diving-helmet"]:
\t\tvar bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
\t\tvar clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
\t\tfor direction in ["west","east","north","south"]:
\t\t\tfor medium in ["dry","flooded"]:
\t\t\t\tfor room in game.placed_rooms:room.water_level=0.0 if medium=="dry" else .95
\t\t\t\tnpc.foot=foot;npc.active=true;npc.dead=false;npc.direction=direction;npc.movement_medium=medium;npc.state="idle";npc.stage="";npc.goal="";npc.expedition.clear();npc.path=PackedVector2Array([foot+Vector2(12,0)])
\t\t\t\tplayer.current_key="";player.motion.clear();player.current_equipment=gear;player.last_time=-1;player.phase=0.0;game.visual_time_seconds=100.0;npc.helmet_equipped=not gear.is_empty()
\t\t\t\tnpc.die()
\t\t\t\tvar state:String="death-ground" if medium=="dry" else "death-water"
\t\t\t\tcheck(npc.dead and npc.animation_state()==state and npc.path.is_empty() and npc.goal.is_empty(),"Actual death dispatcher clears route/work and selects correct medium")
\t\t\t\tvar key:String=state+"-"+direction;var elapsed:=0.0
\t\t\t\tgame.grid_view._get_branforth_frame_source(game)
\t\t\t\tfor slot in range(bank[key].size()):
\t\t\t\t\tgame.visual_time_seconds=100.0+elapsed+float(clocks[key].durations[slot])/2000.0
\t\t\t\t\tvar tex:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\t\t\t\tcheck(same(tex,bank[key][slot]),"Actual selected death source/clock sampled")
\t\t\t\t\tawait capture(("bare" if gear.is_empty() else "helmet")+"-"+key+"-"+str(slot),npc)
\t\t\t\t\tcheck(npc.foot==foot and npc.dead and npc.path.is_empty(),"Native death remains stationary and terminal")
\t\t\t\t\telapsed+=float(clocks[key].durations[slot])/1000.0
\t\t\t\tgame.visual_time_seconds=100.0+elapsed+2.0
\t\t\t\tcheck(same(game.grid_view._get_branforth_frame_source(game),bank[key][-1]),"Terminal death source remains held")
\t\t\t\tcases+=1
\tif not FileAccess.file_exists(OUT+"native_probe.gd.uid"):FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")
\tFileAccess.open(OUT+"native-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"scope":"Actual James die() dispatch and normal selected renderer for all four directions, both gears and dry/flooded media; every six-pose death clock sampled and terminal held. Prescribed renderer times, not autonomous oxygen/starvation dispatch or continuous motion observation."},"\\t"))
\tprint("JAMES NATIVE DEATH checks=",checks," failures=",failures," cases=",cases," captures=",captures.size());game.queue_free();await process_frame;quit(0 if failures==0 else 1)
'''
(o/'native_probe.gd').write_text(s)
print('Prepared actual James terminal death dispatch and rendering review')
