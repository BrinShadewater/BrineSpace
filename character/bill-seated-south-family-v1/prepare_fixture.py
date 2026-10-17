from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
s=(ROOT/'tests/playtest_bill_seated_south_sofa.gd').read_text(encoding='utf-8').replace('bill-seated-south-sofa-v1','bill-seated-south-selected-sofa-v1')
start=s.index('\tplayer.load_manifest(');end=s.index('\tgame.selected_card_id=',start)
s=s[:start]+'''\tfor spec in [["res://character/bill-seated-south-family-v1/bare-manifest.json",""],["res://character/bill-seated-south-family-v1/helmet-manifest.json","diving-helmet"]]:
\t\tvar family: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(spec[0]));var clips: Dictionary=player.frames if spec[1].is_empty() else player.equipment_frames[spec[1]]
\t\tfor state in family.states:
\t\t\tfor i in 6:
\t\t\t\tcheck(clips[state.id][i].get_image().get_data()==Image.load_from_file(state.frameFiles[i]).get_data(),"Normal selected pixels")
\t\t\t\tcheck(clips[state.id][i].get_meta("crew_pivot")==Vector2(128,224) and clips[state.id][i].get_meta("crew_standing_height")==148.0,"Normal selected figure plane")
'''+s[end:]
start=s.index('\t\tcheck(npc.stage=="observation_read","Sit reaches');end=s.index('\t\tfor i in 7:\n\t\t\tawait capture(name+"-rise',start)
s=s[:start]+'''\t\tcheck(npc.stage=="observation_read_enter","Actual sit reaches tablet entry")
\t\tvar seated_offset: Vector2=npc.observation_visual_offset()
\t\tvar previous:=0.0
\t\tfor i in 6:
\t\t\tvar elapsed: float=[.03,.10,.19,.29,.38,.45][i];npc.update(game,elapsed-previous);previous=elapsed
\t\t\tcheck(npc.animation_state()=="read-seated-enter" and is_equal_approx(npc.action_elapsed(),elapsed),"Actual tablet entry chooser/clock")
\t\t\tcheck(npc.observation_visual_offset().distance_to(seated_offset)<.0001,"Entry keeps sofa contact")
\t\t\tcheck(npc.valid_bill_snapshot(npc.snapshot()),"Entry snapshot valid");await capture(name+"-enter-%02d"%i,npc)
\t\tnpc.update(game,.031);check(npc.stage=="observation_read" and is_equal_approx(npc.timer,11.04),"Actual entry reaches reading with retained budget")
\t\tfor i in 6:
\t\t\tgame.visual_time_seconds+=.16;await capture(name+"-read-%02d"%i,npc)
\t\tvar before: Texture2D=game.grid_view._get_human_frame_source(npc.animation_state(),npc.direction)
\t\tnpc.update(game,11.041);check(npc.stage=="observation_read_exit","Actual reading reaches tablet exit")
\t\tcheck(game.grid_view._get_human_frame_source(npc.animation_state(),npc.direction).get_image().get_data()==before.get_image().get_data(),"Actual exit preserves current whole reading pose")
\t\tcheck(is_equal_approx(.48+11.04+npc.timer,12.0),"Existing12-second reading budget")
\t\tprevious=0
\t\tfor i in 6:
\t\t\tvar elapsed: float=[.03,.10,.19,.29,.38,.45][i];npc.update(game,elapsed-previous);previous=elapsed
\t\t\tcheck(npc.animation_state()=="read-seated-exit" and is_equal_approx(npc.action_elapsed(),elapsed),"Actual tablet exit chooser/clock")
\t\t\tcheck(npc.observation_visual_offset().distance_to(seated_offset)<.0001,"Exit keeps sofa contact")
\t\t\tcheck(npc.valid_bill_snapshot(npc.snapshot()),"Exit snapshot valid");await capture(name+"-exit-%02d"%i,npc)
\t\tnpc.update(game,.031);check(npc.stage=="observation_rise","Put-away reaches actual rise")
'''+s[end:]
(ROOT/'tests/test_bill_seated_south_family_selected.gd').write_text(s,encoding='utf-8')
s=(ROOT/'tools/run_bill_seated_south_sofa_validation.py').read_text(encoding='utf-8').replace('bill-seated-south-sofa-v1','bill-seated-south-selected-sofa-v1').replace('playtest_bill_seated_south_sofa.gd','test_bill_seated_south_family_selected.gd')
(ROOT/'tools/run_bill_seated_south_family_selected_validation.py').write_text(s,encoding='utf-8')
