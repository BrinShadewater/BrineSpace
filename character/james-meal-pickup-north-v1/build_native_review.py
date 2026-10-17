from pathlib import Path
import json
P=Path(__file__).resolve().parent
R=P.parents[1]
paths=['res://character/crew-runtime-matte-v1/branforth/'+json.loads((R/'character/crew-runtime-matte-v1/branforth/manifest.json').read_bytes())['states'][0]['frameFiles'][0]]
m=json.loads((R/'character/crew-runtime-matte-v1/branforth/manifest.json').read_bytes())
idle=next(s for s in m['states'] if s['id']=='idle-north')
paths=['res://character/crew-runtime-matte-v1/branforth/'+idle['frameFiles'][0]]+[f'res://character/james-meal-pickup-north-v1/frames/{i:03d}.png' for i in range(6)]+['res://character/james-meal-north-v1/frames/eat/000.png']
manifest=dict(name='Static staged pickup contact only',frameWidth=184,frameHeight=192,pivot=[92,172],standingHeight=148,textureFilter='linear',states=[dict(id='eat-north',frameCount=8,frameFiles=paths,frameDurationsMs=[200]*8,loop=False)])
(P/'review-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
source=(R/'character/james-meal-journeys-v1/native-meal.gd').read_text().split('\tfor q in range(4):',1)[0]
source=source.replace('res://character/james-meal-journeys-v1/','res://character/james-meal-pickup-north-v1/')
source+='''\tgame.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
\tfor offset in [Vector2i.ZERO,Vector2i.DOWN]:
\t\tvar room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
\t\troom.pos=cell+offset;room.rotation=0;room.water_level=0
\t\tgame.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
\tnpc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="life_eat";npc.goal="";npc.path.clear();npc.timer=6;npc.helmet_equipped=false;npc.movement_medium="dry"
\tvar stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(not stations.is_empty(),"Real galley contact")
\tnpc.foot=center+Vector2(stations[0].point);npc.direction=stations[0].facing;npc.state="idle";npc.goal_cell=cell
\tcheck(npc.direction=="north","Staged source fits actual North contact")
\tgame.grid_view._get_branforth_frame_source(game)
\tplayer.load_manifest("res://character/james-meal-pickup-north-v1/review-manifest.json",true)
\tvar authored:Array=player.frames["eat-north"].duplicate()
\tfor i in range(authored.size()):
\t\tplayer.frames["eat-north"]=[authored[i]];player.timing["eat-north"]={"durations":[1000],"loop":true,"seconds":1.0};player.current_key="";player.last_time=-1;player.motion.clear()
\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\tcheck(texture==authored[i],"Actual renderer selects exact staged pose")
\t\tcheck(npc.can_stand(npc.foot),"Counter floor remains clear")
\t\tresults.append({"slot":i,"capture":await capture("pickup-%02d"%i,npc),"textureHeight":texture.get_meta("crew_standing_height"),"pivot":str(texture.get_meta("crew_pivot")),"station":stations[0]})
\tvar file:=FileAccess.open(OUT+"native-review-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Static staged pickup poses rendered at actual default front galley contact. Test-only manifest override; no production transition installation, gameplay, hand-anchor assertion or Continue proof."},"  "));file.close()
\tprint("JAMES PICKUP CONTACT: ",checks," checks; ",failures," failures")
\tquit(1 if failures else 0)
'''
(P/'native-review.gd').write_text(source)
print('Created eight static native contact samples; production unchanged')
