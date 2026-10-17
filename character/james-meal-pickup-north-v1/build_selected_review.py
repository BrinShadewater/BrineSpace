from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'native-review.gd').read_text().split('\tgame.occupied.clear();')[0]
source+='''\tgame.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
\tfor offset in [Vector2i.ZERO,Vector2i.DOWN]:
\t\tvar room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
\t\troom.pos=cell+offset;room.rotation=0;room.water_level=0
\t\tgame.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
\tnpc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="life_eat";npc.goal="hunger";npc.path.clear();npc.timer=6;npc.helmet_equipped=false;npc.movement_medium="dry"
\tvar stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(not stations.is_empty(),"Real galley contact")
\tnpc.foot=center+Vector2(stations[0].point);npc.direction=stations[0].facing;npc.state="idle";npc.goal_cell=cell
\tcheck(npc.direction=="north","Installed source fits actual North contact")
\tgame.grid_view._get_branforth_frame_source(game)
\tvar selected:Array=player.frames["meal-acquire-north"]
\tvar times:Array=[.05,.175,.35,.55,.725,.85,.9001,1.05]
\tfor i in range(times.size()):
\t\tnpc.timer=6.0-float(times[i]);game.visual_time_seconds=100.0+float(times[i])
\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\tif i<6:check(texture==selected[i],"Production timeline selects exact pickup pose")
\t\tif i==6:check(texture==player.frames["eat-north"][0],"Production pickup joins exact held meal")
\t\tcheck(npc.can_stand(npc.foot),"Counter floor remains clear")
\t\tresults.append({"slot":i,"elapsed":times[i],"capture":await capture("selected-%02d"%i,npc),"textureHeight":texture.get_meta("crew_standing_height"),"pivot":str(texture.get_meta("crew_pivot")),"station":stations[0]})
\tvar file:=FileAccess.open(OUT+"native-selected-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Static production timeline samples at actual default North front counter, selected full-body poses and exact pickup-to-held join. No player manifest/frame overrides; actor timer sampled manually. Separate actual journey proves normal approach and Continue."},"  "));file.close()
\tprint("JAMES SELECTED PICKUP: ",checks," checks; ",failures," failures")
\tquit(1 if failures else 0)
'''
(P/'native-selected.gd').write_text(source)
print('Created production timeline contact samples; no renderer override')
