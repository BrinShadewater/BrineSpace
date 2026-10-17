from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'character/james-construction-motion-v1/safety.gd').read_text(encoding='utf-8')
s=s.replace('res://character/james-construction-motion-v1/','res://character/james-construction-helmet-v1/')
s=s.replace('actor.helmet_equipped=false','check(actor.set_helmet_equipped(true),"Prescribed worn helmet")')
s=s.replace('game.grid_view.branforth_player.frames','game.grid_view.branforth_player.equipment_frames["diving-helmet"]')
s=s.replace('"foot":[actor.foot.x,actor.foot.y]','"helmet":actor.helmet_equipped,"foot":[actor.foot.x,actor.foot.y],"footViewport":[(root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)).x,(root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)).y]')
s=s.replace('JAMES CONSTRUCTION SAFETY:','JAMES HELMET CONSTRUCTION SAFETY:')
(P/'safety.gd').write_text(s,encoding='utf-8')
