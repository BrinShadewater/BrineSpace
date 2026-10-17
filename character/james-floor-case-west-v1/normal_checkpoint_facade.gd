extends RefCounted
const CODEC=preload("res://scripts/james_cargo_checkpoint.gd")
const SAVE=preload("res://scripts/run_save.gd")
const FIELD=CODEC.FIELD
static func capture(game)->Dictionary:return SAVE.capture(game)
static func valid_shape(data:Dictionary)->bool:return CODEC.valid_shape(data)
static func admits_loaded(data:Dictionary,player)->bool:return CODEC.admits_loaded(data,player)
static func base_packet(data:Dictionary)->Dictionary:return CODEC.base_packet(data)
static func write(game,path:String)->Error:return SAVE.write(game,path)
static func read(path:String)->Dictionary:return SAVE.read(path)
static func restore_staged(game,data:Dictionary)->bool:return await SAVE.restore_staged(game,data)
