"""Update the former staged contact study to actual admitted normal controller/art."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_south_step_world.gd').read_text()
s=s.replace('const Step=preload("res://character/marsh-south-step-v1/step_controller.gd")','const Step=preload("res://scripts/marsh_npc.gd")')
start=s.index('class StudyMain extends ');end=s.index('var game',start);s=s[:start]+s[end:]
s=s.replace('south-step-world-v1-2026-10-02','south-step-normal-world-v1-2026-10-03')
s=s.replace('const OUTPUT=', 'var OUTPUT=')
s=s.replace('func _init():call_deferred("run")','func _init():\n\tif OS.get_cmdline_user_args().has("--corrected"):\n\t\tOUTPUT="res://output/marsh-animation-audit/south-step-normal-world-v2-2026-10-03/"\n\tcall_deferred("run")')
s=s.replace('game=load("res://scenes/main.tscn").instantiate();game.set_script(StudyMain)','game=load("res://scenes/main.tscn").instantiate()')
s=s.replace('check(not Normal.valid_marsh_snapshot(saved),"normal actor cannot accept staged motion it does not restore")','check(Normal.valid_marsh_snapshot(saved),"actual normal actor accepts its current snapshot")')
s=s.replace('check(not player.frames.has("walk-step-south"),"normal catalog remains unselected")','check(player.frames.has("walk-step-south"),"actual normal catalogue selects South step")')
s=s.replace('\tplayer.load_manifest("res://character/marsh-south-step-v1/candidate-05/manifest.json",true)\n','')
s=s.replace('stagedActorRestores','normalActorRestores')
s=s.replace('Candidate05 staged actor/StudyMain contact offset, actual furnished-room navigation and normal grid; four prescribed5/5.734/6/7unit routes with20ms real actor updates and pause; six actor-only binary restores. Peers paused. No RunSave/Title Continue or normal admission.','Current normal actor/main/catalogue without source/controller injections, actual furnished-room navigation; four prescribed5/5.734/6/7unit routes with20ms actor updates/pause, source support-foot measurements and six actor-only binary restores. Peers paused. Fixture room/site, not natural task selection or paid building/fullRunSave/TitleContinue/continuous cadence acceptance.')
(ROOT/'tools/review_marsh_south_step_normal_world_v1.gd').write_text(s)
(ROOT/'tools/review_marsh_south_step_normal_world_v1.gd.uid').write_text('uid://dt9southworld2q7\n')
s=(ROOT/'tools/fingerprint_marsh_south_step_detail_v1.py').read_text()
s=s.replace("ROOT=Path(__file__).resolve().parents[1];paths={ROOT/'project.godot',ROOT/'scenes/main.tscn'}", "ROOT=Path(__file__).resolve().parents[1];paths={ROOT/'project.godot',ROOT/'scenes/main.tscn'}\npaths.update(ROOT/p for p in ['tools/install_marsh_south_step_contact_v1.py','character/marsh-v2/supplemental/south-step-contact-v1/admission.json','character/marsh-south-step-detail-v1/candidate-02-registered-frame.png'])")
s=s.replace('for name in [',"for name in ['review_marsh_south_step_normal_world_v1.gd','review_marsh_south_step_normal_world_v1.gd.uid','fingerprint_marsh_south_step_normal_world_v1.py',")
(ROOT/'tools/fingerprint_marsh_south_step_normal_world_v1.py').write_text(s)
print('Normal main/controller/catalogue contact probe prepared; strict supporting sole baseline retained')
