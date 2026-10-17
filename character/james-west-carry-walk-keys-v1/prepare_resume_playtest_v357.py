from pathlib import Path

bank = Path.cwd() / 'character/james-west-carry-walk-keys-v1'
review = bank / 'release-resume-playtest-v357'
review.mkdir(exist_ok=True)
source = (bank / 'release-expedition-playtest-v355/expedition_playtest.gd').read_text()
source = source.replace('expedition355', 'resume357').replace('JAMES PACKAGED EXPEDITION', 'JAMES PACKAGED RESUME')
source = source.replace('var home:Vector2i', 'var resume_records:Array=[]\nvar home:Vector2i')
source = source.replace('var phases:Array=[];var keys:Array=[];', 'var resumed:Array=[];var phases:Array=[];var keys:Array=[];')
source = source.replace('            check(game.resources.metal==5', '''            if phase in ["return","drain"] and not resumed.has(phase):
                resumed.append(phase)
                await capture(npc,label,frames);frames+=1
                var before:Dictionary={"phase":phase,"foot":npc.foot,"trip":npc.expedition.duplicate(true),"tank":npc.tank_oxygen,"helmet":npc.helmet_equipped,"units":game.drone_fleet.sites[target].units,"metal":game.resources.metal,"data":game.resources.data}
                var Save=load("res://scripts/run_save.gd")
                var save_path:String="user://resume357-"+str(rotation)+"-"+phase+".loop"
                check(Save.write(game,save_path)==OK,"Loaded expedition checkpoint writes: "+Save.last_error)
                var checkpoint:Dictionary=Save.read(save_path)
                check(not checkpoint.is_empty(),"Disk checkpoint reads: "+Save.last_error)
                if checkpoint.is_empty():get_tree().quit(2);return
                game.set_process(false);game.tick_timer.stop();game.queue_free();get_tree().current_scene=null
                await get_tree().process_frame
                Save.pending=checkpoint
                game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
                game.meta.save_path="user://resume357.meta";game.run_save_path=save_path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
                get_tree().root.add_child(game);get_tree().current_scene=game
                while not game.startup_complete:await get_tree().process_frame
                game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
                check(game.paused,"Normal staged Continue starts paused")
                check(game.run_save_path==save_path,"Continue keeps checkpoint in scratch folder")
                npc=game.branforth_npc;player=game.grid_view.branforth_player
                check(npc.expedition==before.trip,"Loaded expedition payload and route survive fresh scene")
                check(npc.foot.distance_to(before.foot)<.001,"Exact exterior floor contact restored")
                check(is_equal_approx(npc.tank_oxygen,before.tank) and npc.helmet_equipped==before.helmet,"Tank and helmet survive Continue")
                check(game.drone_fleet.sites[target].units==before.units and game.resources.metal==before.metal and game.resources.data==before.data,"Checkpoint does not duplicate or prematurely deliver salvage")
                check(player.get_script().resource_path=="res://scripts/james_water_player.gd","Continue retains selected normal James player")
                game.run_save_path=save_path;game.paused=false;game.hand_panel.hide();game.card_drag.hide()
                await capture(npc,label,frames);frames+=1
                resume_records.append({"case":label,"phase":phase,"beforeFrame":frames-2,"afterFrame":frames-1,"footError":npc.foot.distance_to(before.foot),"tank":npc.tank_oxygen,"cargo":npc.expedition.get("cargo",{}).duplicate(true)})
            check(game.resources.metal==5''')
source = source.replace('        cases.append({', '        check(resumed.size()==2,"Both loaded return and airlock drain resume tested")\n        cases.append({"resumed":resumed,')
source = source.replace('"captures":records,"scope":', '"captures":records,"resumes":resume_records,"scope":')
source = source.replace('Not random expedition ecology, real-time pacing, long-session traffic or loaded checkpoint interruption.', 'Two disk checkpoints per journey restored into fresh scenes via normal staged Continue: loaded return and airlock drain. Not title-button interaction, process restart, random expedition ecology, real-time pacing or long-session traffic.')
(review / 'resume_playtest.gd').write_text(source)
runner = (bank / 'run_expedition_playtest_v355.py').read_text().replace('release-expedition-playtest-v355', 'release-resume-playtest-v357').replace('james-expedition-playtest-v355', 'james-resume-playtest-v357').replace('JamesExpeditionPlaytest', 'JamesResumePlaytest').replace('expedition_playtest.gd', 'resume_playtest.gd').replace('expedition355', 'resume357')
(bank / 'run_resume_playtest_v357.py').write_text(runner)
print('Prepared loaded return and airlock Continue test in exact Windows package')
