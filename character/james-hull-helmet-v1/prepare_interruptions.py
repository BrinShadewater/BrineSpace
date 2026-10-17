from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
for family in ['return','reassign']:
    s=(R/f'character/james-hull-{family}-v1/validate.gd').read_text(encoding='utf-8')
    s=s.replace('res://character/james-hull-lifecycle-v1/validate.gd','res://character/james-hull-helmet-v1/north.gd')
    s=s.replace(f'res://character/james-hull-{family}-v1/',f'res://character/james-hull-helmet-v1/{family}/')
    s=s.replace('game.Architects.advance_core(game,10)','game.Architects.advance_core(game,10)\n\t\tcheck(game.branforth_npc.set_helmet_equipped(true),"Prescribed supported worn gear")')
    s=s.replace('player.frames','player.equipment_frames["diving-helmet"]')
    s=s.replace('game.grid_view.branforth_player.frames','game.grid_view.branforth_player.equipment_frames["diving-helmet"]')
    s=s.replace('"foot":[actor.foot.x,actor.foot.y]','"helmet":actor.helmet_equipped,"foot":[actor.foot.x,actor.foot.y],"footViewport":[(root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)).x,(root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)).y]')
    s=s.replace('RESULT+"validate.gd"',f'"res://character/james-hull-helmet-v1/{family}.gd"')
    s=s.replace('JAMES HULL '+family.upper()+':','JAMES HULL HELMET '+family.upper()+':')
    (P/f'{family}.gd').write_text(s,encoding='utf-8');(P/family).mkdir(exist_ok=True)
print('Actual helmeted North cancellation and reentry fixtures prepared')
