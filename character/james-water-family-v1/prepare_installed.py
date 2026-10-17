from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-paired.gd').read_text();start=s.index('\tvar player=');end=s.index('\tfor gear in',start)
s=s[:start]+'\tvar grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()\n\tvar player=grid.branforth_player\n'+s[end:]
s=s.replace('native-"+direction','native-installed-"+direction').replace('JAMES WATER PAIRED STAGED:', 'JAMES WATER INSTALLED:').replace('no live-route or installation claim','actual installed loader, all192 selected slots; route proof separate').replace('\tquit(1 if failures else 0)','\tgrid.free()\n\tquit(1 if failures else 0)')
(P/'native-installed.gd').write_text(s)
s=(P/'native-routes.gd').read_text()
start=s.index('\tvar clearance:');end=s.index('\tgame.selected_card_id=',start)
s=s[:start]+'''\tnpc.swim_clearance.clear();npc.tread_clearance.clear();npc.action_clearance.clear();npc.movement_medium="flooded"
\tnpc.swim_segment_clear(npc.foot,npc.foot,"east");npc.action_pose_clear("transition")
\tvar expected_clearance: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance.json"))
\tfor field in ["swim","tread","actions"]:
\t\tvar selected: Dictionary=npc.swim_clearance if field=="swim" else (npc.tread_clearance if field=="tread" else npc.action_clearance)
\t\tcheck(selected==expected_clearance[field],"Actual NPC lazy selected "+field+" clearance")
\tvar player=game.grid_view.branforth_player
'''+s[end:]
s=s.replace('route-evidence.json','installed-route-evidence.json').replace('route-captures/','installed-route-captures/').replace('OUT+"route-captures"','OUT+"installed-route-captures"').replace('JAMES WATER ROUTES:', 'JAMES WATER INSTALLED ROUTES:').replace('staged real routes','installed real routes').replace('Staged candidates on real James','Installed candidates on real James')
(P/'native-installed-routes.gd').write_text(s)
print('Prepared actual installed loader and actual NPC lazy-clearance route fixtures')
