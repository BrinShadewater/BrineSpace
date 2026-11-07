extends RefCounted
## Additive room definitions; existing room rates/unlocks are unchanged.
const PATH="res://rooms/new-room-expansion/definitions.json"
static var cached:Dictionary={}
static func rooms() -> Dictionary:
 if not cached.is_empty():return cached.duplicate(true)
 var result={}
 var rows=JSON.parse_string(FileAccess.get_file_as_string(PATH))
 for row in rows:
  row.size=Vector2i.ONE
  result[row.id]=row
 cached=result
 return result.duplicate(true)

