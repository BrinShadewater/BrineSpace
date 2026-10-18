extends SceneTree
const Preferences=preload("res://scripts/title_settings.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var game=load("res://scripts/main.gd").new()
 game.set_meta("tablet_controls",true)
 var previous:bool=Preferences.pixel_frames
 Preferences.pixel_frames=false
 game._load_ui_textures()
 check(game.ui_textures.is_empty(),"Tablet vector panels retain no unused raster skins")
 var panel:=PanelContainer.new();panel.name="ControlsPanel"
 game._apply_panel_style(panel)
 check(panel.get_theme_stylebox("panel").get_script()==preload("res://scripts/terminal_frame_style.gd"),"Default vector panel style preserved")
 check(game.ui_textures.is_empty(),"Vector styling performs no raster load")
 Preferences.pixel_frames=true
 game._apply_panel_style(panel)
 var style=panel.get_theme_stylebox("panel")
 check(style is StyleBoxTexture and style.texture!=null,"Pixel-frame setting still loads its authored skin")
 check(game.ui_textures.size()==1 and game.ui_textures.has(game.UI_TERMINAL_PANEL),"Only requested panel skin remains resident")
 var original=preload("res://scripts/safe_image.gd").raw_image(game.UI_TERMINAL_PANEL)
 if style is StyleBoxTexture:check(style.texture.get_image().get_data()==original.get_data(),"Requested skin pixels are unchanged")
 var first=style.texture if style is StyleBoxTexture else null
 game._apply_panel_style(panel)
 check(panel.get_theme_stylebox("panel").texture==first,"Repeated pixel styling shares the existing texture")
 game.set_meta("tablet_controls",false);game._load_ui_textures()
 check(game.ui_textures.size()==18,"Desktop eager skin policy unchanged")
 Preferences.pixel_frames=previous;panel.free();game.free()
 print("TABLET UI TEXTURE STORAGE failures=",failures)
 quit(1 if failures else 0)
