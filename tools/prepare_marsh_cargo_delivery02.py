"""Recheck complete routes with persisted arrival turn inside unchanged timer."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_cargo_delivery01_actor.gd').read_text().replace('cargo-delivery-01-2026-10-02','cargo-delivery-02-2026-10-02')
s=s.replace('var seen:Dictionary={};var pickup_seen:Dictionary={};var unload_seen:Dictionary={};','var seen:Dictionary={};var pickup_seen:Dictionary={};var unload_seen:Dictionary={};var arrival_seen:Dictionary={};')
s=s.replace('var key:String=actor.animation_state()+"-"+actor.direction if actor.action_elapsed()>=0 else str(player.motion.get("clip",""))','var presentation:Dictionary=actor.workshop_arrival_presentation(player)\n\t\t\tvar key:String=str(presentation.key) if not presentation.is_empty() else (actor.animation_state()+"-"+actor.direction if actor.action_elapsed()>=0 else str(player.motion.get("clip","")))')
old='''			if actor.stage=="workshop_unload":
				unload_seen[slot]=true
				if actor.action_elapsed()>=.52:check(slot==3,"actual delivery holds authored final North idle")'''
new='''			if actor.stage=="workshop_unload":
				if key=="carry-turn-west-north":
					arrival_seen[slot]=true
					check(actor.action_elapsed()<.400001,"arrival turn consumes first400ms of unchanged2second timer")
				else:
					check(key=="unload-north" and arrival_seen.size()==5,"all5arrival phases precede lowering")
					if unload_seen.is_empty():check(slot==0,"arrival finishes into exact North unload0")
					unload_seen[slot]=true
					if actor.action_elapsed()>=.92:check(slot==3,"remaining unload timer holds authored finalidle after400+520ms")'''
assert old in s;s=s.replace(old,new)
s=s.replace('if actor.stage=="workshop_unload":check(key=="unload-north" and slot==0,"actual arrival uses exact North unload0")','if actor.stage=="workshop_unload":check(key=="carry-turn-west-north" and slot==0,"actual arrival begins authored WestNorth turn0")')
s=s.replace('pickup_seen.size()==4 and unload_seen.size()==4,"complete normal','pickup_seen.size()==4 and unload_seen.size()==4 and arrival_seen.size()==5,"complete normal')
s=s.replace('"unloadSlots":unload_seen.keys(),','"unloadSlots":unload_seen.keys(),"arrivalSlots":arrival_seen.keys(),')
s=s.replace('No route/facing override after work begins.','No route/facing override after work begins. Marsh-only persisted arrival presentation turns WestNorth400ms then lowers520ms inside unchanged2second unload timer.')
s=s.replace('MARSH COMPLETE DELIVERY','MARSH DELIVERY02 ARRIVAL JOIN')
(ROOT/'tools/review_marsh_cargo_delivery02_actor.gd').write_text(s)
(ROOT/'tools/review_marsh_cargo_delivery02_actor.gd.uid').write_text('uid://ds6cargodel2v10\n')
finger=(ROOT/'tools/fingerprint_marsh_cargo_delivery01.py').read_text().replace('cargo_delivery01','cargo_delivery02');(ROOT/'tools/fingerprint_marsh_cargo_delivery02.py').write_text(finger)
pub=(ROOT/'tools/publish_marsh_cargo_delivery01.py').read_text().replace('cargo-delivery-01','cargo-delivery-02').replace('delivery-01-actor-review','delivery-02-actor-review')
pub=pub.replace("assert case['actorRestores']==case['captureCount']","assert case['actorRestores']==case['captureCount'] and case['arrivalSlots']==list(range(5))")
(ROOT/'tools/publish_marsh_cargo_delivery02.py').write_text(pub)
print('delivery02 fixture/publisher/fingerprint prepared; five arrival-turn phases required')
