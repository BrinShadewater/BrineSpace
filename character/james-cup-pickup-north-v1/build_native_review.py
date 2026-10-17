from pathlib import Path
P=Path(__file__).resolve().parent
base=P.parent/'james-meal-pickup-north-v1/native-selected.gd'
source=base.read_text().split('\tgame.occupied.clear();')[0].replace('res://character/james-meal-pickup-north-v1/','res://character/james-cup-pickup-north-v1/')
source+='''\tgame.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
\tfor offset in [Vector2i.ZERO,Vector2i.DOWN]:
\t\tvar room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
\t\troom.pos=cell+offset;room.rotation=0;room.water_level=0
\t\tgame.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
\tnpc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="life_inspect";npc.goal="curiosity";npc.path.clear();npc.timer=6;npc.helmet_equipped=false;npc.movement_medium="dry"
\tvar stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(not stations.is_empty(),"Real galley contact")
\tnpc.foot=center+Vector2(stations[0].point);npc.direction=stations[0].facing;npc.state="idle";npc.goal_cell=cell
\tcheck(npc.direction=="north","Staged cup source fits actual North contact")
\tgame.grid_view._get_branforth_frame_source(game)
\tplayer.load_manifest("res://character/james-cup-pickup-north-v1/manifest.json",true)
\tvar selected:Array=player.frames["cup-acquire-north"]
\tfor i in range(selected.size()):
\t\tplayer.frames["inspect-north"]=[selected[i]];player.timing["inspect-north"]={"durations":[1000],"loop":true,"seconds":1.0};player.current_key="";player.last_time=-1
\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\tcheck(texture==selected[i],"Test-only source review shows exact cup pose")
\t\tcheck(npc.can_stand(npc.foot),"Counter floor remains clear")
\t\tresults.append({"slot":i,"capture":await capture("source-%02d"%i,npc),"textureHeight":texture.get_meta("crew_standing_height"),"pivot":str(texture.get_meta("crew_pivot")),"station":stations[0]})
\tvar file:=FileAccess.open(OUT+"native-review-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Static staged selected cup poses at actual default North counter. Test-only inspect-frame overrides for source contact review; no production choreography or Continue proof."},"  "));file.close()
\tprint("JAMES CUP SOURCE CONTACT: ",checks," checks; ",failures," failures")
\tquit(1 if failures else 0)
'''
(P/'native-review.gd').write_text(source)
print('Created staged six-pose cup counter review')
