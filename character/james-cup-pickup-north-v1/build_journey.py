from pathlib import Path
P=Path(__file__).resolve().parent
source=(P.parent/'james-meal-pickup-north-v1/native-journey.gd').read_text().replace('res://character/james-meal-pickup-north-v1/','res://character/james-cup-pickup-north-v1/')
source=source.replace('func run()->void:', '''func checkpoint(npc)->String:
\tvar pose:String=npc.animation_state()
\tif pose=="meal-acquire" and npc.timer<=5.62:return "bowl-acquire"
\tif pose=="meal-deposit" and npc.timer<=.5:return "bowl-deposit"
\tif pose=="cup-acquire" and npc.timer<=2.62:return "cup-acquire"
\tif pose=="cup-deposit" and npc.timer<=.5:return "cup-deposit"
\treturn ""
func run()->void:''')
source=source.replace('var ticks:=0;','var restorations:Dictionary={};var ticks:=0;')
source=source.replace('check(npc.animation_state()==("meal-acquire" if npc.meal_acquire_active() else "eat" if npc.stage=="life_eat" else "drink"),"Pickup stays within original bare meal budget")','check(npc.animation_state() in ["meal-acquire","eat","meal-deposit"] if npc.stage=="life_eat" else npc.animation_state() in ["cup-acquire","drink","cup-deposit"],"All handoffs stay within original meal stage budgets")')
source=source.replace('if (npc.meal_acquire_active() or (not helmet and slot in [0,3,5])) or (helmet and npc.timer<=3 and not captures.any(func(path):return "held" in path)):','if not helmet:')
source=source.replace('[q,mode,npc.stage,slot]','[q,mode,npc.animation_state(),slot]')
source=source.replace('if not restored and npc.stage=="life_eat" and npc.timer<=5.62:', 'if not checkpoint(npc).is_empty() and not restorations.has(checkpoint(npc)):\n\t\t\t\t\t\tvar restore_label:String=checkpoint(npc)')
source=source.replace('game.set_process(false);game.paused=false;restored=true','game.set_process(false);game.paused=false;restored=true;restorations[restore_label]=restore_exact')
marker='\t\t\tnpc.needs.curiosity=95;npc.timer=0;npc.decision_rng.seed=17'
extra='''\t\t\tcheck(restorations.size()==4 and restorations.values().all(func(value):return value),"Four actual handoff disk Continues hold exact pixels")
\t\t\tfor action in ["meal-acquire","eat","meal-deposit","cup-acquire","drink","cup-deposit"]:
\t\t\t\tfor slot in range(6):check(slots.has(action+"-"+str(slot)),"Actual journey observes each choreography source pose")
\t\t\tfor pair in [["meal-acquire","eat"],["eat","meal-deposit"],["meal-deposit","cup-acquire"],["cup-acquire","drink"],["drink","cup-deposit"]]:
\t\t\t\tcheck(player.frames[pair[0]+"-north"][-1].get_image().get_data()==player.frames[pair[1]+"-north"][0].get_image().get_data(),"Exact whole source handoff pixels")
\t\t\tcheck(player.frames["cup-deposit-north"][-1].get_image().get_data()==padded.get_data(),"Cup return ends at exact accepted empty idle")
\t\t\tvar held_stage:String=npc.stage;var held_timer:float=npc.timer;var held_player:Dictionary=player.snapshot()
\t\t\tfor boundary in [["life_eat",5.1000001,"life_eat",5.0999999],["life_eat",.9000001,"life_eat",.8999999],["life_eat",.0000001,"life_drink",2.9999999],["life_drink",2.1000001,"life_drink",2.0999999],["life_drink",.9000001,"life_drink",.8999999]]:
\t\t\t\tnpc.stage=boundary[0];npc.timer=boundary[1];var before_join:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
\t\t\t\tnpc.stage=boundary[2];npc.timer=boundary[3];check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==before_join,"Actual timer boundary retains exact pixels")
\t\t\tnpc.stage=held_stage;npc.timer=held_timer;player.restore_snapshot(held_player)
'''
source=source.replace(marker,extra+marker)
source=source.replace('"restorePixelsExact":restore_exact,','"restorePixelsExact":restore_exact,"restorations":restorations,')
source=source.replace('One actual default North bare galley journey through installed900ms acquisition, eating/drinking and next walk; normal chooser/native crew update, all six acquisition slots, fixed contact/gear/facing, exact selected endpoints, one real mid-pickup disk Continue into a fresh scene and pause. Other room rotations/equipped stages, dish/cup transitions and interruptions remain separate.','One actual default North bare9s galley journey:900ms bowl pickup, eating,900ms bowl return,900ms cup pickup, complete sip retimed into1.2s,900ms cup return and next normal walk. Six poses from each of six clips, exact joined endpoints and four real mid-handoff disk Continues into fresh scenes with exact actor/clock/pixels/pause. Other contacts, interruptions and credit audit remain separate.')
source=source.replace('JAMES PICKUP JOURNEY: ','JAMES MEAL HANDOFF JOURNEY: ')
assert 'restorations.size()==4' in source and 'var restore_label' in source
(P/'native-journey.gd').write_text(source)
print('Created complete North meal choreography journey and four fresh-scene handoff Continues')
