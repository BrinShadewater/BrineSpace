from pathlib import Path
P=Path(__file__).resolve().parent;cargo=P.parent/'james-water-cargo-family-v1'
s=(P/'native-staged.gd').read_text();a=s.index('\tvar player=');b=s.index('\tfor gear in',a)
s=s[:a]+'\tvar grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()\n\tvar player=grid.branforth_player\n'+s[b:]
s=s.replace('native-"+mode','native-installed-"+mode').replace('JAMES WATER CARGO TURNS STAGED:','JAMES WATER CARGO TURNS INSTALLED:').replace('source player and native render only, no installed route claim','actual normal grid loader and cargo turn playback; routes separate').replace('\tquit(1 if failures else 0)','\tgrid.free()\n\tquit(1 if failures else 0)')
(P/'native-installed.gd').write_text(s)
s=(P/'native-routes.gd').read_text();a=s.index('\tvar clearance:');b=s.index('\tgame.selected_card_id=',a)
s=s[:a]+'''\tnpc.swim_clearance.clear();npc.tread_clearance.clear();npc.action_clearance.clear();npc.movement_medium="flooded"
\tnpc.swim_segment_clear(npc.foot,npc.foot,"east");npc.action_pose_clear("transition")
\tpreload("res://scripts/crew_life.gd").clearance.clear();preload("res://scripts/crew_life.gd").clear(npc,"cargo-turn")
\tvar clearance:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance.json"))
\tfor field in ["swim","tread","actions"]:
\t\tvar selected:Dictionary=npc.swim_clearance if field=="swim" else (npc.tread_clearance if field=="tread" else npc.action_clearance)
\t\tcheck(selected==clearance[field],"Actual lazy "+field+" clearance")
\tcheck(preload("res://scripts/crew_life.gd").clearance["branforth"]==clearance.life,"Actual lazy cargo-turn life clearance")
\tvar player=game.grid_view.branforth_player
'''+s[b:]
s=s.replace('route-evidence.json','installed-route-evidence.json').replace('route-captures/','installed-route-captures/').replace('OUT+"route-captures"','OUT+"installed-route-captures"').replace('JAMES WATER CARGO TURN ROUTES:','JAMES WATER CARGO TURN INSTALLED ROUTES:').replace('staged manifest override','actual installed cargo and turn manifests and lazy life clearance')
(P/'native-installed-routes.gd').write_text(s)
s=(cargo/'native-phases.gd').read_text()
a=s.index('\tplayer.load_manifest(');b=s.index('\tgame.selected_card_id=',a)
s=s[:a]+s[b:]
s=s.replace('phase-evidence.json','installed-phase-evidence.json').replace('route-captures/','installed-phase-captures/').replace('v1/route-captures"','v1/installed-phase-captures"').replace('candidate manifest injected','actual installed manifest').replace('or installed selection proof','proof of dispatch or a full airlock return journey').replace('JAMES WATER CARGO PHASES:','JAMES WATER CARGO INSTALLED PHASES:')
(cargo/'native-installed-phases.gd').write_text(s)
s=(cargo/'native-staged.gd').read_text();a=s.index('\tvar player=');b=s.index('\tfor gear in',a)
s=s[:a]+'\tvar grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()\n\tvar player=grid.branforth_player\n'+s[b:]
s=s.replace('native-"+mode','native-installed-"+mode').replace('JAMES WATER CARGO STAGED:','JAMES WATER CARGO INSTALLED:').replace('\tquit(1 if failures else 0)','\tgrid.free()\n\tquit(1 if failures else 0)')
(cargo/'native-installed.gd').write_text(s)
print('Prepared installed loader, actual cargo movement and installed expedition phase fixtures')
