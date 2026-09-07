extends SceneTree
## Parent room dressing must not leak into a child with replacement hosts.
func _init() -> void: call_deferred("run")
func run() -> void:
	var failures:=0
	for identity in ["biodome","bio_lab"]:
		var view=load("res://rooms/underwater/batch-two/"+identity+"_view.gd").new()
		view.embedded=true
		root.add_child(view)
		for q in range(4):
			view.configure_embedded(q,[],false,0.0)
			if identity=="biodome":
				if view.dressing==null: failures+=1
				else:
					for route in view.dressing.profile.get("routes",[]):
						for endpoint in [route.from,route.to]:
							if view.dressing.find_prop(endpoint.host).is_empty(): failures+=1
			else:
				# A child-owned profile is valid; only leaked parent hosts are wrong.
				if view.dressing!=null:
					for route in view.dressing.profile.get("routes",[]):
						for endpoint in [route.from,route.to]:
							if view.dressing.find_prop(endpoint.host).is_empty() or str(endpoint.host).begins_with("biodome_"): failures+=1
				for prop in view.props:
					if str(prop.id).begins_with("biodome_"): failures+=1
		view.free()
	print("BIO DRESSING ISOLATION: parent routes retained; child replacement hosts; four quarters; ",failures," failures")
	quit(1 if failures else 0)
