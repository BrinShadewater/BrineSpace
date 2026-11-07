extends "res://character/bill-carry-turn-east-south-motion-v3/carry_motion_preview.gd"
## Hold only movement during the initial standing row; inherited needs remain live.
func move(delta:float)->void:
 if preview_player!=null and not preview_player.start_motion.is_empty() and preview_time-float(preview_player.start_motion.started)<.04:return
 super.move(delta)
