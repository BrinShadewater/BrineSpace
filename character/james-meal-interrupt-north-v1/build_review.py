from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'native-audit.gd').read_text().split('\tvar phases:Array=')[0]
source+='''\tgame.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
\tfor offset in [Vector2i.ZERO,Vector2i.DOWN]:
\t\tvar room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
\t\troom.pos=cell+offset;room.rotation=0;room.water_level=0
\t\tgame.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
\tnpc.rebuild(game);npc.active=true;npc.dead=false;npc.path.clear();npc.state="idle";npc.helmet_equipped=false;npc.movement_medium="dry";npc.direction="north";npc.goal_cell=cell
\tvar stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(not stations.is_empty(),"Actual counter contact")
\tnpc.foot=center+Vector2(stations[0].point)
\tvar samples:Array=[["meal-acquire","life_eat",5.45],["eat","life_eat",4.35],["meal-deposit","life_eat",.35],["cup-acquire","life_drink",2.45],["drink","life_drink",1.54],["cup-deposit","life_drink",.35]]
\tfor sample in samples:
\t\tnpc.meal_return.clear();npc.stage=sample[1];npc.timer=sample[2];npc.goal="hunger"
\t\tvar before:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\tcheck(npc.animation_state()==sample[0],"Exact reviewed source action")
\t\tvar source_index:int=player.frames[sample[0]+"-north"].find(before);check(source_index==3,"Same mid-action source index as actual interruption journey")
\t\tnpc.goal="";check(npc.begin_interrupted_meal(game),"Production interrupted return begins")
\t\tvar key:String=npc.animation_state()+"-north";var pictures:Array=[];var cursor:=0.0
\t\tfor i in range(player.frames[key].size()):
\t\t\tvar duration:float=player.timing[key].durations[i]/1000.0;npc.meal_return.elapsed=cursor+duration*.5;cursor+=duration
\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game);check(texture==player.frames[key][i],"Production return selects exact reviewed whole source frame")
\t\t\tpictures.append(await capture("review-"+sample[0]+"-%02d"%i,npc))
\t\tresults.append({"action":sample[0],"key":key,"captures":pictures,"durations":player.timing[key].durations})
\tvar file:=FileAccess.open(OUT+"native-review-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Production return source3 poses manually sampled at actual North counter; no renderer overrides. Actual service cancellation and disk Continue proven separately by six native-return journeys."},"  "));file.close()
\tprint("JAMES MEAL RETURN REVIEW: ",checks," checks; ",failures," failures")
\tquit(1 if failures else 0)
'''
(P/'native-review.gd').write_text(source)
print('Created six production return visual sequences')
