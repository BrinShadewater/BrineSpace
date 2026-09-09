# Animated title screen

## Current September 9 revision

The installed artwork is in `consistency-v1/`: BRINE V13 likeness/rendering, matte slate/ivory laboratory, a native silhouette-clipped character and separate background. Float, monitors and Reduced Motion remain. See that directory's README and `docs/ART_FIXES_2026-09-09.md`. The original-layer workflow below remains for the preserved older cover.

Settings, Codex and Meta Progression are shared with the in-game pause menu.
See `docs/MENU_SETTINGS.md` for options, persistence and navigation behavior.

The active title screen now renders lossless layers directly in Godot through
`scripts/title_cover.gd`. `cover-stage.png` holds the fixed lab, logo and waterline;
`cover-character.png` contains the extracted foreground with transparent margins
and bottom padding for its three-pixel float. The still stage uses nearest texture
filtering; the moving character uses linear filtering for subpixel travel.
Thirty-eight rear bubbles and nine faint foreground bubbles have different speeds
and fade near the water surface. Seven monitor panels animate independently.
No video decoder runs on the starting screen.

Regenerate the layers with `python tools/title/render_cover_loop.py --layers-only`.
Settings now persists Reduced Motion alongside display/audio preferences. It
freezes ambient animation at its current position and disables menu fades.
The footer groups share a vertical center; panel transitions and button feedback
use short tweens without shifting control hitboxes. Opening panels blocks the
underlying actions until the close transition finishes and returns focus.

`brinespace-title-clean.ogv` is the preserved polished eight-second video: steady water
level, a subtle three-pixel character float, smaller rising bubbles and seven
animated monitors. It is 1584 × 672 at 48 fps, silent, encoded directly from
rendered frames as high-quality Ogg Theora for Godot's native VideoStreamPlayer.
The original `brinespace-title.ogv` remains available for comparison.
Tracked through Git LFS; rights follow `NOTICE.md`.

`cover-clean.png` and `cover-background.png` are generated cleanup plates based
on the owner's original cover. The background plate supplies only pixels revealed
behind the moving character. `tools/title/render_cover_loop.py` reproduces the
animation using Pillow, NumPy, OpenCV and imageio-ffmpeg. Subpixel sprite
translation removes integer-step bobbing; the rendered period is checked for
exact equality and the title and waterline are protected by assertions.

The source export is `Art/cover-loop/brinespace-loop-v4.mp4` in the original
`project-margot` art workspace. Conversion: `ffmpeg -i input.mp4 -an -c:v
libtheora -q:v 9 -pix_fmt yuv420p brinespace-title.ogv`.

The project starts at `scenes/title_screen.tscn`. New Loop opens the
existing `scenes/main.tscn` and its doctrine selection. The gameplay scene can
still be launched directly by fixtures. The full cover retains its aspect
ratio, with menu controls beneath it; no gameplay state runs behind the menu.

The right-hand Codex and Meta Progression badges use bespoke SVG emblems.
Codex has Rooms and Synergies tabs with search, discovery counts and
All / Discovered / Hidden filters. Recovered room cards show current artwork,
build costs, output and upkeep; recovered synergy cards pair their room images
with effects, stabilization status and rewards. Hidden slots conceal names and
artwork while offering individual discovery clues. This owner-requested preview
of undiscovered entries preserves hidden recipes and existing unlock conditions;
search cannot reveal concealed names. Progression shows
research, victories, stabilized patterns, doctrine ranks and their starting
bonuses. Both are read-only overlays; Escape or Close returns keyboard focus
to the badge. Room thumbnail paths are shared with gameplay through
`scripts/room_card_art.gd` so both interfaces use the same art.

Native smoke test: run Godot with `--path . --script
res://tests/test_title_screen.gd`. It checks independent floating motion,
continued animation, layout at three resolutions, keyboard activation,
discovery filtering, concealed-name search, synergy clues, modal focus,
progression, persisted settings, reduced-motion pause/resume and arrival at doctrine
selection. A preview is written to the ignored
`output/title-screen.png`. Release export remains unverified; the project
currently has no release export preset.
