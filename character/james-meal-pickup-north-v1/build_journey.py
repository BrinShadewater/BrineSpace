from pathlib import Path
P=Path(__file__).resolve().parent
R=P.parents[1]
source=(R/'character/james-meal-journeys-v1/native-meal.gd').read_text()
source=source.replace('res://character/james-meal-journeys-v1/','res://character/james-meal-pickup-north-v1/')
source=source.replace('for q in range(4):','for q in [0]:').replace('for helmet in [false,true]:','for helmet in [false]:')
source=source.replace('check(npc.animation_state()==("inspect" if helmet else "eat" if npc.stage=="life_eat" else "drink"),"Sealed helmet uses inspection substitute")','check(npc.animation_state()==("meal-acquire" if npc.meal_acquire_active() else "eat" if npc.stage=="life_eat" else "drink"),"Pickup stays within original bare meal budget")')
source=source.replace('var sample:String=npc.stage+"-"+str(slot)','var sample:String=npc.animation_state()+"-"+str(slot)')
source=source.replace('[q,mode,npc.stage,slot]','[q,mode,npc.animation_state(),slot]')
source=source.replace('(not helmet and slot in [0,3,5])','(npc.meal_acquire_active() or (not helmet and slot in [0,3,5]))')
source=source.replace('npc.timer<=3.75','npc.timer<=5.62')
source=source.replace('native-meal-evidence.json','native-journey-evidence.json')
source=source.replace('Eight actual galley service journeys across four default room rotations and two gears. Normal seeded chooser, native main crew update, real station contact, bare eat/drink and equipped curiosity inspection substitute. Eight actual disk Continue restores into fresh scenes with exact actor/pixels and pause. Arrival facing and next normal walking join asserted; chooser can repeat a meal before departing. Pickup/deposit source choreography and interruptions remain separate.','One actual default North bare galley journey through installed900ms acquisition, eating/drinking and next walk; normal chooser/native crew update, all six acquisition slots, fixed contact/gear/facing, exact selected endpoints, one real mid-pickup disk Continue into a fresh scene and pause. Other room rotations/equipped stages, dish/cup transitions and interruptions remain separate.')
source=source.replace('JAMES GALLEY JOURNEYS: ','JAMES PICKUP JOURNEY: ')
marker='\t\t\tnpc.needs.curiosity=95;npc.timer=0;npc.decision_rng.seed=17'
assert marker in source
extra='''\t\t\tfor slot in range(6):check(slots.has("meal-acquire-"+str(slot)),"Real journey observes each acquisition source slot")
\t\t\tvar acquired:Array=player.frames["meal-acquire-north"]
\t\t\tvar idle_image:Image=player.frames["idle-north"][0].get_image()
\t\t\tvar padded:=Image.create(184,192,false,Image.FORMAT_RGBA8);padded.blit_rect(idle_image,Rect2i(Vector2i.ZERO,idle_image.get_size()),Vector2i.ZERO)
\t\t\tcheck(acquired[0].get_image().get_data()==padded.get_data(),"Native acquisition begins with exact accepted idle pixels")
\t\t\tcheck(acquired[-1].get_image().get_data()==player.frames["eat-north"][0].get_image().get_data(),"Native acquisition ends with exact accepted held meal pixels")
'''
source=source.replace(marker,extra+marker)
(P/'native-journey.gd').write_text(source)
print('Created one real North pickup meal journey and mid-pickup fresh-scene Continue')
