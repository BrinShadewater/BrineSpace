# Shared menus and preferences

For room explanations, unread discovery navigation, run-summary hierarchy and the
contextual first-loop guide, see [Station learning UI](LEARNING_UI.md).

For station health, reserve forecasts, placement feedback, blueprint decisions
and searchable checkpoint history, see [Station decision UI](DECISION_UI.md).

The starting screen and in-game pause menu open the same Settings, Codex and
Meta Progression panels (`scripts/title_archive.gd`). A shared navigation row
switches between these sections. Close returns to the title-screen opener;
Back returns to the pause menu without resuming the station. Resume restores
the pause state that existed before the menu was opened.

The pause menu retains Save Game, Save & Return to Title, Save & Quit,
Recenter Station, Admin View, restart and expedition conclusion. The former
in-game display controls have been removed; all preferences use one store and
one settings panel (`scripts/settings_panel.gd`). Fonts, pressure-panel buttons,
hover feedback, menu tooltips and text scaling are shared.

## Options

| Section | Options and effect |
| --- | --- |
| Display | Window resolution; Windowed, Borderless Fullscreen or Exclusive Fullscreen mode; V-sync; and frame cap (unlimited, 30, 60, 120, 144, 240). V-sync can impose a lower limit. Borderless fills the current display and preserves the previous windowed resolution. |
| Audio | Master volume, master mute, mute while unfocused. Muting preserves volume and focus return clears only temporary background muting. |
| Controls & Pause | Shift-wheel zoom sensitivity (50–200%), inverted wheel zoom, and pause on focus loss. Automatic pausing requires an explicit resume afterward. |
| Accessibility | Reduced motion, panel text size (100–130%), and menu tooltip delay (100–1500 ms). Reduced motion freezes the title cover and removes menu fades; gameplay timing stays unchanged. |

Resolution and window-mode changes preview for 15 seconds. Keep Changes records
them; Revert, timeout, losing focus, or leaving the panel restores the previous
configuration. Display defaults use the same preview. Other changes apply
immediately and persist to `user://brine_settings.cfg`, separately
from progression and loop checkpoints. Defaults preserve normal gameplay:
unlimited FPS, unmuted audio, no focus-loss pause, standard zoom direction/speed,
standard text size and a 500 ms tooltip delay. The menu tooltip delay applies to
the shared menu buttons; existing station HUD tooltips retain the engine default.

The native `tests/test_shared_menu.gd` fixture uses isolated preference, meta and
checkpoint files. It checks cross-menu navigation, save/return, live frame caps,
audio focus behavior, actual wheel input, pause preservation, larger text,
preference reload, directional focus and tooltip timing. `tests/test_title_screen.gd` and
`tests/test_run_save.gd` cover title navigation and checkpoint continuation.
Run the shared-menu fixture with `-- --window-modes` to also switch through
borderless, exclusive and windowed modes and verify saved-mode restoration.
That pass omits pointer-tooltip timing, which is checked in the normal pass.

## Menu polish

Shared panels use matching search fields, tabs, sliders, scrollbars and progress
bars. The selected section stays highlighted, and Settings keeps its save feedback
above the scrolling options. Codex preserves its search, filter, tab and scroll
position when visiting another section. Progression cards use two columns on wide
windows and one on smaller windows.

The pause menu groups navigation, checkpoint actions and station tools. Doctrine,
journal and run-summary overlays share the menu typography and button treatment;
keyboard focus enters the active overlay and returns to the journal opener when
closed. HUD buttons have clearer text and focus outlines. Reduced motion also
removes blueprint-card hover translation and scaling while retaining highlighting.

Tab and Shift+Tab stay inside the active overlay, skipping hidden and disabled
controls. Journal and archive reading areas can receive keyboard focus for
scrolling, and Ctrl+F (Command+F) focuses Codex search.

Codex lists recovered entries first while preserving catalog order within each
group and hidden signal numbering. Empty results offer a Clear Search & Filter
action. Settings slider values sit separately from their labels, and the settings
column breakpoint accounts for the selected panel text size.

Panel text scaling also applies to doctrine choices, journal rich text and the
run summary. `tests/test_overlay_text.gd` checks repeat-refresh font stability,
summary focus and panel bounds at 1280×720 with 130% text, using isolated saves.

Pause-menu save results appear beside the checkpoint action, preserving the
station summary. Returning to an already-paused station is labeled explicitly.
Doctrine confirmation reports the remaining selections and explains how to change
a completed pair. Save and restart actions include tooltips describing their effect.

## Audit additions

- Settings is also accessible from doctrine selection, journal and run summary;
  Back restores the originating screen, its choices and keyboard focus. Escape
  returns doctrine selection and run summary to the title; journal Escape returns
  to the station with its prior pause state.
- Each Settings category has a Restore Defaults action. Controls includes single-key
  rebinding for camera movement, pause, fit, journal, rotation and debug Admin View.
  Duplicate bindings are rejected; Escape cancels capture. Tab, Enter and Escape
  remain reserved for menus. Hints update with bindings. Full controller gameplay
  support is not claimed.
- Continue displays cycle, doctrine pair and UTC save time for new checkpoints.
  Older checkpoints remain readable without a timestamp. Backup recovery and
  unreadable saves have persistent title messages; resizing does not erase errors.
- Progression lists recovered memory/upgrade IDs. The current prototype has no
  authored descriptions or effects for these records, so the panel states that
  limitation instead of inventing benefits.
- Credits / Build is available from the title and shared navigation. It shows the
  project build identifier, copyright information, Godot version and engine license.
- Admin View remains available in debug builds and is omitted from release menus.
- `tests/test_menu_recovery.gd` exercises display preview/keep/revert, actual key
  capture and conflicts, defaults, overlay return state, save-failure UI, damaged
  checkpoint messages, and title bounds at 960×540, 1024×768, 1440×900 and 2560×1080.

The `Windows Menu Validation` export preset builds the title/main scenes and menu
recovery fixture using the locally configured Windows templates. It is a local
debug validation build, not a release or publication workflow.

Run `tools/build_menu_export_fixture.ps1` before exporting that preset. It adapts
the same recovery suite into a scene because Windows export templates do not run
editor `--script` fixtures. The `menu_validation` feature selects this scene only
for the validation preset; normal launches still open the title screen.

Validation on 2026-09-06: title, shared-menu (normal and window modes), enlarged
overlay text, save/restore and menu-recovery suites pass. The exported Windows
debug executable also prints `MENU RECOVERY: PASS` from an empty external working
directory, with no ERROR or SCRIPT ERROR log entries. Raw-image export warnings
remain; this preset explicitly includes PNG bytes and the tested art loads.
Evidence is in `output/menu-audit-*.log`, `output/menu-recovery.log`,
`output/menu-export.log` and `output/menu-export-runtime.log`. Physical controller,
multi-monitor transitions and OS display scaling remain unverified hardware cases.

Validation: native title-menu and shared-menu fixtures pass, including Codex state
retention; the save/restore fixture passes. The broader `playtest_polish.gd` run
reports three economy/discovery assertions (solar-array affordability, second
discovery chain, and retained blueprints). The save fixture also logs missing
sub-biome image files. These require separate gameplay/asset investigation.
