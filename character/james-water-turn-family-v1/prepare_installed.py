from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-staged.gd').read_text();a=s.index('\tvar player=');b=s.index('\tfor gear in',a)
s=s[:a]+'\tvar grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()\n\tvar player=grid.branforth_player\n'+s[b:]
s=s.replace('native-"+mode','native-installed-"+mode').replace('JAMES WATER TURNS STAGED:','JAMES WATER TURNS INSTALLED:').replace('source player and native render only, no installed route claim','actual normal grid loader and turn playback, route proof separate').replace('\tquit(1 if failures else 0)','\tgrid.free()\n\tquit(1 if failures else 0)')
(P/'native-installed.gd').write_text(s)
s=(P/'native-routes.gd').read_text();a=s.index('\tvar clearance:');b=s.index('\tgame.selected_card_id=',a)
s=s[:a]+'''\tnpc.swim_clearance.clear();npc.tread_clearance.clear();npc.action_clearance.clear();npc.movement_medium="flooded"
\tnpc.swim_segment_clear(npc.foot,npc.foot,"east");npc.action_pose_clear("transition")
\tvar expected_clearance:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance.json"))
\tfor field in ["swim","tread","actions"]:
\t\tvar selected:Dictionary=npc.swim_clearance if field=="swim" else (npc.tread_clearance if field=="tread" else npc.action_clearance)
\t\tcheck(selected==expected_clearance[field],"Actual NPC lazy selected "+field+" clearance")
\tvar player=game.grid_view.branforth_player
'''+s[b:]
s=s.replace('route-evidence.json','installed-route-evidence.json').replace('route-captures/','installed-route-captures/').replace('OUT+"route-captures"','OUT+"installed-route-captures"').replace('JAMES WATER TURN ROUTES:', 'JAMES WATER TURN INSTALLED ROUTES:').replace('staged two-leg paths','installed two-leg paths').replace('staged manifest override','actual installed manifests and NPC lazy clearance')
(P/'native-installed-routes.gd').write_text(s)
print('Prepared normal installed loader and NPC lazy-clearance turn route fixtures')
