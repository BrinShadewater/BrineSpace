"""Normal selected sofa paired admission and full world/disk future fixture."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/veld-sofa-fall-south-selected-v1';S.mkdir(exist_ok=True)
for gear in ['bare','helmet']:
    held=json.loads((P/f'{gear}-manifest.json').read_text());neutral=json.loads((P/f'{gear}-neutral-manifest.json').read_text())
    selected=dict(held);selected['name']='Veld South sofa fall paired selected '+gear;selected['status']='selected_pending_world_validation';selected['states']=held['states']+neutral['states']
    existing=S/f'{gear}-manifest.json'
    if existing.exists():
        current=json.loads(existing.read_text())
        if current.get('status')=='selected' and current['states']==selected['states']:selected['status']='selected'
    (S/f'{gear}-manifest.json').write_text(json.dumps(selected,indent=2)+'\n',encoding='utf-8')
script=R/'scripts/grid_canvas.gd';text=script.read_text(encoding='utf-8')
needle='\t\telif actor == "branforth":'
insertion='''\t\t\tplayer.load_manifest("res://character/veld-sofa-fall-south-selected-v1/bare-manifest.json", true)
\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/veld-sofa-fall-south-selected-v1/helmet-manifest.json"):
\t\t\t\tpush_error("Veld paired South sofa fall equipment mismatch")
'''
if 'veld-sofa-fall-south-selected-v1' not in text:
    assert text.count(needle)==1;script.write_text(text.replace(needle,insertion+needle),encoding='utf-8')
registry=R/'character/ACTIVE_ASSETS.json';original=registry.read_bytes();data=json.loads(original)
key='veld-south-sofa-reader-falls'
data['actionOverrides'][key]='character/veld-sofa-fall-south-selected-v1/bare-manifest.json'
data['equipmentActionOverrides'][key]='character/veld-sofa-fall-south-selected-v1/helmet-manifest.json'
for gear in ['bare','helmet']:
    binding={'script':'scripts/grid_canvas.gd','contains':f'res://character/veld-sofa-fall-south-selected-v1/{gear}-manifest.json'}
    if binding not in data['bindings']:data['bindings'].append(binding)
temp=registry.with_name('ACTIVE_ASSETS.sofa-admission.tmp');temp.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');assert registry.read_bytes()==original;temp.replace(registry)
source=(R/'tests/test_veld_bunk_selected_early.gd').read_text(encoding='utf-8')
helpers=source[:source.index('func run():')]
helpers=helpers.replace('test_veld_bunk_selected_early.gd.uid','test_veld_sofa_selected_continue.gd.uid').replace('veld-bunk-selected-early-v1','veld-sofa-selected-continue-v1').replace('veld-bunk-early-fall','veld-sofa-fall')
start=helpers.index('\t# Production selection only;');end=helpers.index('\treturn game',start)
helpers=helpers[:start]+'''\t# Real normal loader only: exact reader and both fall sources in fresh scenes.
\tfor equipped in [false,true]:
\t\tvar pool:Dictionary=game.grid_view.veld_player.equipment_frames["diving-helmet"] if equipped else game.grid_view.veld_player.frames
\t\tfor folder in ["veld-seated-south-selected-v1","veld-sofa-fall-south-selected-v1"]:
\t\t\tvar path:String="res://character/"+folder+"/"+("helmet" if equipped else "bare")+"-manifest.json"
\t\t\tvar manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
\t\t\tfor clip in manifest.states:
\t\t\t\tcheck(pool.has(clip.id) and pool[clip.id].size()==clip.frameFiles.size(),"Normal paired clip: "+clip.id)
\t\t\t\tif not pool.has(clip.id):continue
\t\t\t\tfor index in clip.frameFiles.size():
\t\t\t\t\tvar image=Image.load_from_file(clip.frameFiles[index]);image.convert(Image.FORMAT_RGBA8)
\t\t\t\t\tcheck(pool[clip.id][index].get_image().get_data()==image.get_data(),"Exact normal loaded source: "+clip.id+str(index))
'''+helpers[end:]
start=helpers.index('func prepare(');end=helpers.index('func recover_survivor(',start)
helpers=helpers[:start]+'''func prepare(actor,station:Dictionary,equipped:bool):
\tactor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="curiosity";actor.path.clear();actor.expedition.clear();actor.bunk_motion.clear();actor.water_death_motion.clear();actor.water_death_last_frame=null;actor.helmet_equipped=equipped;actor.movement_medium="dry";actor.goal_cell=CELL;actor.direction="south"
\tactor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
\tactor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":90.0,"maintenance":0.0}
\tcheck(actor.begin_room_activity(),"Actual timed South reader dispatch")
\tcheck(actor.valid_veld_snapshot(actor.snapshot()),"Prepared actor valid")
'''+helpers[end:]
old='''\t\tvar expected:Texture2D=clips[recipe.entry_key][recipe.entry_index] if elapsed<.18 else game.grid_view.veld_player.frame_at_elapsed(recipe.clip,elapsed,recipe.equipment)
\t\tcheck(sample.pixels==pixels_hash(expected),"Independent authored floor clock source: "+name)
\t\tcheck(sample.offset==Vector2.ZERO,"Unsupported early pose stays registered to floor")'''
new='''\t\tvar index:int=0 if elapsed<.18 else (1 if elapsed<.36 else (2 if elapsed<.56 else (3 if elapsed<.78 else (4 if elapsed<1.02 else 5))))
\t\tvar expected:Texture2D=clips[recipe.entry_key][recipe.entry_index] if index==0 else clips[recipe.clip][index]
\t\tcheck(sample.pixels==pixels_hash(expected),"Independent six-source sofa clock: "+name)
\t\tvar amount:float=1.0 if elapsed<.36 else clampf(1.0-(elapsed-.36)/.42,0,1)
\t\tcheck(sample.offset.distance_to(Vector2(recipe.entry_position_offset)*amount)<.00001,"Independent supported-to-floor offset")
\t\tvar at:Vector2=game.veld_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+sample.offset
\t\tcheck(is_equal_approx(sample.depth,maxf(at.y,float(recipe.entry_sort_depth)) if elapsed<.78 else at.y),"Independent seat/floor depth")
\t\tcheck(sample.foot==(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(recipe.sofa_motion.local_foot),"Physical navigation foot fixed")'''
assert old in helpers;helpers=helpers.replace(old,new)
run='''func run():
\tcheck(OS.get_user_data_dir().replace("\\\\","/").begins_with(OS.get_environment("APPDATA").replace("\\\\","/")+"/"),"Scratch APPDATA")
\tif failures:quit(2);return
\tDirAccess.make_dir_recursive_absolute(OUT)
\tvar game=await fresh()
\tgame.paused=false;game.Architects.advance_core(game,10);game.paused=true
\tcheck(game.veld_npc.active,"Normal Veld release")
\tgame.selected_rotation=0;game._place_room("observation_room",CELL,true);game.powered_room_cells[CELL]=true
\tawait recover_survivor(game);await game.veld_npc.rebuild(game)
\tvar station:Dictionary={}
\tfor candidate in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
\t\tif candidate.get("mode","")=="read" and candidate.facing=="south":station=candidate;break
\tcheck(not station.is_empty(),"Actual default South sofa station")
\tvar baseline:Dictionary=SAVE.capture(game);check(SAVE.problem(baseline).is_empty(),"Normal baseline checkpoint valid")
\tif failures:quit(1);return
\tvar records:Array=[]
\tvar cases:Array=[]
\tfor elapsed in [.05,.10,.25,.40,2.40,4.20,11.95]:cases.append([elapsed,"live"])
\tfor phase in [[.05,"power"],[.40,"power"],[2.40,"suspended"]]:cases.append(phase)
\tfor equipped in [false,true]:
\t\tfor case in cases:
\t\t\tcheck(await SAVE.restore_staged(game,baseline),"Normal baseline restore before world death")
\t\t\tgame.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
\t\t\tvar actor=game.veld_npc;prepare(actor,station,equipped)
\t\t\tgame.visual_time_seconds=400
\t\t\tvar player=game.grid_view.veld_player;player.current_key="";player.motion.clear();player.last_time=-1
\t\t\tfor tick in 1600:
\t\t\t\tgame.grid_view._get_veld_live_frame_source(game)
\t\t\t\tif actor.stage=="observation_read" and 12-actor.timer>=float(case[0]):break
\t\t\t\tactor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
\t\t\tcheck(actor.stage=="observation_read","Actual intended reader phase")
\t\t\tvar living:Texture2D=game.grid_view._get_veld_frame_source(game)
\t\t\tif case[1]!="live":
\t\t\t\tif case[1]=="power":game.powered_room_cells.erase(CELL)
\t\t\t\telse:game.occupied[CELL].suspended=true
\t\t\t\tcheck(not actor.service_available(game,CELL),"Actual reading service interrupted")
\t\t\t\tactor.update(game,.00001)
\t\t\t\tcheck(actor.stage=="observation_read_exit","Actual interrupted read exit")
\t\t\t\tcheck(game.grid_view._get_veld_frame_source(game).get_image().get_data()==living.get_image().get_data(),"Exact retained interruption entrance")
\t\t\t\tliving=game.grid_view._get_veld_frame_source(game)
\t\t\tvar expected_clip:String="death-sofa-neutral-south" if float(case[0]) in [.05,11.95] else "death-sofa-read-south"
\t\t\tvar name:String=("helmet" if equipped else "bare")+"-"+str(case[0])+"-"+str(case[1])
\t\t\tvar entry=await capture_bunk(game,CELL,name+"-living",living)
\t\t\tvar crew_before:int=game.crew_count
\t\t\tFLOOD.kill(game,actor,"veld","South sofa Continue fixture")
\t\t\tcheck(actor.dead and actor.water_death_motion.get("clip","")==expected_clip,"Actual world death selects prop-matched sofa family")
\t\t\tcheck(game.crew_count==crew_before-1 and not game.Architects.present(game,"veld") and game.Architects.present(game,"bill"),"Actual world roster mortality/survivor")
\t\t\tcheck(actor.valid_veld_snapshot(actor.snapshot()),"Strict saved sofa recipe")
\t\t\tif failures:quit(1);return
\t\t\tcheck(game.grid_view._get_veld_frame_source(game).get_image().get_data()==living.get_image().get_data(),"Exact full living pose on world death")
\t\t\tvar save_elapsed:float=[.10,.40,.60,.90,1.60][records.size()%5]
\t\t\tgame.visual_time_seconds=float(actor.water_death_motion.started)+save_elapsed
\t\t\tvar shown:Texture2D=game.grid_view._get_veld_frame_source(game)
\t\t\tvar pixels:PackedByteArray=shown.get_image().get_data();var snapshot:Dictionary=actor.snapshot()
\t\t\tvar foot:Vector2=actor.foot;var timer:float=actor.timer;var clock:float=game.visual_time_seconds
\t\t\tvar before=await capture_bunk(game,CELL,name+"-before",shown)
\t\t\tvar playback:Dictionary=game.grid_view.crew_playback_snapshot()
\t\t\tvar expected:Array=await future_trace(game,name+"-reference")
\t\t\tawait actor.restore_snapshot(game,snapshot,true);game.grid_view.restore_crew_playback(playback);game.visual_time_seconds=clock
\t\t\tcheck(actor.snapshot()==snapshot,"Exact reference rewind before disk save")
\t\t\tcheck(game.grid_view._get_veld_frame_source(game).get_image().get_data()==pixels,"Exact source rewind")
\t\t\tcheck(game.running and not game.testing_free_build and not game.testing_disable_failures,"Ordinary save eligibility")
\t\t\tvar written:int=SAVE.write(game,game.run_save_path);check(written==OK,"Ordinary disk write: "+SAVE.last_error)
\t\t\tif written!=OK:quit(1);return
\t\t\tvar disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Ordinary disk read: "+SAVE.last_error)
\t\t\tif disk.is_empty():quit(1);return
\t\t\tgame.queue_free();await process_frame;game=await fresh()
\t\t\tcheck(await SAVE.restore_staged(game,disk),"Fresh normal scene Continue: "+SAVE.last_error)
\t\t\tgame.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game.run_save_path="user://veld-sofa-fall.loop"
\t\t\tactor=game.veld_npc
\t\t\tcheck(actor.foot==foot and actor.timer==timer and actor.stage==snapshot.stage and actor.dead and actor.helmet_equipped==equipped,"Saved corpse pose/clock/equipment")
\t\t\tcheck(actor.water_death_motion==snapshot.veld_water_death,"Exact saved sofa selector/contact recipe")
\t\t\tcheck(game.paused and is_equal_approx(game.visual_time_seconds,clock),"Saved clock paused")
\t\t\tvar restored:Texture2D=game.grid_view._get_veld_frame_source(game)
\t\t\tcheck(restored!=null and restored.get_image().get_data()==pixels,"Exact whole source after fresh Continue")
\t\t\tvar after=await capture_bunk(game,CELL,name+"-after",restored)
\t\t\tcheck(after.position==before.position and is_equal_approx(after.depth,before.depth),"Actual native sofa/floor position and depth restored")
\t\t\tgame._process(.5);check(actor.timer==timer and game.grid_view._get_veld_frame_source(game).get_image().get_data()==pixels,"Paused Continue source fixed")
\t\t\tvar actual:Array=await future_trace(game,name+"-resumed")
\t\t\tcheck(actor.dead and actor.path.is_empty() and actor.geometry.is_empty(),"Corpse has no living navigation")
\t\t\tcheck(actual[-1].offset==Vector2.ZERO and actor.foot==foot,"Terminal floor contact and foot")
\t\t\tvar clips:Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
\t\t\tcheck(actual[-1].pixels==pixels_hash(clips[expected_clip][-1]),"Exact retained floor terminal")
\t\t\tcompare_future(expected,actual,name)
\t\t\trecords.append({"name":name,"saveElapsed":save_elapsed,"recipe":snapshot.veld_water_death,"living":entry,"clock":clock,"before":before,"after":after,"reference":expected,"resumed":actual})
\t\t\tprint("SOFA WORLD CONTINUE ",name," records=",records.size()," failures=",failures)
\tcheck(records.size()==20,"Both gears,14live and6actual interrupted world deaths")
\tvar f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\\t"));f.close()
\tprint("VELD SOFA WORLD CONTINUE: %d checks,%d failures;20 fresh disk restores"%[checks,failures]);quit(1 if failures else 0)
'''
# Do not retain the freed original player across a fresh scene.
run=run.replace('var clips:Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames','var clips:Dictionary=game.grid_view.veld_player.equipment_frames["diving-helmet"] if equipped else game.grid_view.veld_player.frames')
(R/'tests/test_veld_sofa_selected_continue.gd').write_text(helpers+run,encoding='utf-8')
(R/'tests/test_veld_sofa_selected_continue.gd.uid').write_text('uid://d0evssfcont1\n',encoding='utf-8')
runner=(R/'tools/run_veld_bunk_selected_continue.py').read_text(encoding='utf-8')
runner=runner.replace('veld-bunk-selected-continue-v1','veld-sofa-selected-continue-v1').replace('test_veld_bunk_selected_continue.gd','test_veld_sofa_selected_continue.gd').replace('timeout=750','timeout=1800').replace('helmet-death-after-room.png','helmet-2.4-suspended-after-room.png').replace('0 failures;8 fresh disk restores','0 failures;20 fresh disk restores').replace("['BUNK RESUME','VELD BUNK BODY RESUME'","['SOFA WORLD CONTINUE','VELD SOFA WORLD CONTINUE'")
start=runner.index('    inputs+=list(');end=runner.index('    bindings=',start)
runner=runner[:start]+'''    for folder in ['veld-sofa-fall-south-selected-v1','veld-seated-south-selected-v1']:
        for gear in ['bare','helmet']:
            manifest=ROOT/f'character/{folder}/{gear}-manifest.json';inputs.append(manifest)
            for state in json.loads(manifest.read_text(encoding='utf-8'))['states']:
                inputs.extend(ROOT/f.removeprefix('res://') for f in state['frameFiles'])
    inputs=sorted(set(inputs))
'''+runner[end:]
(R/'tools/run_veld_sofa_selected_continue.py').write_text(runner,encoding='utf-8')
print(json.dumps({'selectedStatesPerGear':2,'newWorldCases':20,'normalOnly':True,'worldValidation':'pending'}))
