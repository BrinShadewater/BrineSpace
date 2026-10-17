from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-staged.gd').read_text();a=s.index('\tvar player=');b=s.index('\tfor gear in',a);s=s[:a]+'\tvar grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()\n\tvar player=grid.branforth_player\n'+s[b:]
s=s.replace('native-bare-contact.png','native-installed-bare-contact.png').replace('native-helmet-contact.png','native-installed-helmet-contact.png').replace('JAMES AIR STAGED:','JAMES AIR INSTALLED:').replace('source player and native render only','actual installed normal loader and player/render').replace('\tquit(1 if failures else 0)','\tgrid.free()\n\tquit(1 if failures else 0)')
(P/'native-installed.gd').write_text(s)
s=(P/'native-behaviour.gd').read_text();a=s.index('\tpreload("res://scripts/crew_life.gd").clearance["branforth"]');b=s.index('\tgame.selected_card_id=',a)
s=s[:a]+'''\tpreload("res://scripts/crew_life.gd").clearance.clear()
\tpreload("res://scripts/crew_life.gd").clear(npc,"swim-distress")
\tcheck(preload("res://scripts/crew_life.gd").clearance["branforth"]==clearance.life,"Actual lazy selected life clearance")
\tvar player=game.grid_view.branforth_player
'''+s[b:]
s=s.replace('route-captures/','installed-behaviour-captures/').replace('OUT+"route-captures"','OUT+"installed-behaviour-captures"').replace('behaviour-evidence.json','installed-behaviour-evidence.json').replace('normal grid candidate overrides','normal grid actual installed manifests and lazy life clearance').replace('JAMES AIR BEHAVIOUR:','JAMES AIR INSTALLED BEHAVIOUR:')
(P/'native-installed-behaviour.gd').write_text(s)
print('Prepared actual installed loader and life-state progression fixtures')
