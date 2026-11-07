extends "res://rooms/underwater/observation-room-v1/observation_room_view.gd"
## Review uses the installed furnishings.
func _ready() -> void:
	super._ready()
	RoomFloor.profile_for(self)
	RoomFloor.floor_profiles[get_script().resource_path]=RoomFloor.floor_profiles.get("res://rooms/underwater/observation-room-v1/observation_room_view.gd",{}).duplicate(true)
