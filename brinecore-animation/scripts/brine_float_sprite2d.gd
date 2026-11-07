extends Sprite2D

@export var bob_amount: float = 3.0
@export var bob_speed: float = 1.2

var start_position: Vector2

func _ready() -> void:
    start_position = position

func _process(_delta: float) -> void:
    var bob := sin(Time.get_ticks_msec() / 1000.0 * bob_speed) * bob_amount
    position = start_position + Vector2(0, bob)
