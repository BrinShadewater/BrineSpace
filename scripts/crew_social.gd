extends RefCounted
## Nearby off-duty crew share a short exchange; no teleporting or reserved routes.
const Architects=preload("res://scripts/architects.gd")
const SECONDS=6.0
static func safe(game,actor) -> bool:
	return actor.active and not actor.dead and actor.movement_medium=="dry" and actor.expedition.is_empty() and not actor.helmet_equipped and actor.locker_request.is_empty() and not actor.helmet_action_active() and actor.stage.is_empty() and actor.path.is_empty() and actor.service_available(game,actor.cell_at(actor.foot)) and (not actor.needs_air() or (actor.needs.hunger<65 and actor.needs.fatigue<65))
static func nearby(a,b) -> bool:
	var distance: float=a.foot.distance_to(b.foot)
	return a.cell_at(a.foot)==b.cell_at(b.foot) and distance>=40 and distance<=150 and a.segment_clear(a.foot,b.foot)
static func release(actor,completed: bool=false) -> void:
	actor.social_partner=""
	if actor.goal!="social":return
	actor.goal="";actor.timer=0;actor.state="idle";actor.activity="conversation finished" if completed else "conversation interrupted"
	if completed:actor.needs.curiosity=maxf(0,actor.needs.curiosity-15)
static func face(actor,peer) -> void:
	var offset: Vector2=peer.foot-actor.foot
	actor.direction=("east" if offset.x>0 else "west") if absf(offset.x)>absf(offset.y) else ("south" if offset.y>0 else "north")
static func advance(game,delta: float) -> void:
	if delta<=0 or not game.running or game.paused:return
	var present: Dictionary={}
	for id in Architects.IDS:
		if Architects.present(game,id):present[id]=Architects.actor_for(game,id)
	for id in present:
		var actor=present[id]
		actor.social_cooldown=maxf(0,actor.social_cooldown-delta)
		if actor.social_partner.is_empty():continue
		var peer=present.get(actor.social_partner)
		if actor.goal!="social" or peer==null or peer.social_partner!=id or peer.goal!="social" or not safe(game,actor) or not safe(game,peer) or not nearby(actor,peer):
			release(actor)
			if peer!=null and peer.social_partner==id:release(peer)
	var handled: Dictionary={}
	for id in present:
		var actor=present[id]
		if actor.goal!="social" or handled.has(id):continue
		var peer=present[actor.social_partner]
		handled[id]=true;handled[actor.social_partner]=true
		var remaining: float=maxf(0,minf(actor.timer,peer.timer)-delta)
		actor.timer=remaining;peer.timer=remaining
		if remaining<=0:release(actor,true);release(peer,true);continue
		var speaker=actor if remaining>SECONDS/2 else peer
		for member in [actor,peer]:
			member.state="interact" if member==speaker else "idle"
			member.activity=("talking with " if member==speaker else "listening to ")+Architects.NAMES[member.social_partner]
	for id in present:
		var actor=present[id]
		if actor.social_cooldown>0 or actor.goal not in ["","primary-work","curiosity"] or not safe(game,actor):continue
		for other in present:
			var peer=present[other]
			if other==id or peer.social_cooldown>0 or peer.goal not in ["","primary-work","curiosity"] or not safe(game,peer) or not nearby(actor,peer):continue
			for member in [actor,peer]:
				member.social_partner=other if member==actor else id
				member.social_cooldown=90;member.goal="social";member.goal_cell=member.cell_at(member.foot);member.timer=SECONDS;member.state="idle"
				member.activity="chatting with "+Architects.NAMES[member.social_partner]
			face(actor,peer);face(peer,actor)
			break
