# Menu audit — 2026-09-06

Scope: source and existing-test review of title, pause, Settings, Codex, progression,
doctrine, journal and run-summary menus. No gameplay behavior changed. This is not
a new exported-build or controller playtest. Recommendations below distinguish
observed implementation gaps from features that depend on product scope.

## Implementation follow-up

The core findings below have been addressed in the subsequent menu pass: timed
display recovery, checkpoint preview/errors, Settings/Back on all major overlays,
per-section defaults, controls reference and rebinding, explicit text-scale scope,
individual progression records, debug-only Admin View, and Credits/Build.
See `MENU_SETTINGS.md` for behavior and tests. Memories/upgrades remain IDs with
no authored effect catalog; the UI explicitly explains this prototype limitation.
New menu recovery, directional focus and non-16:9 layout checks supplement the
existing fixtures. Physical controller coverage, multi-monitor/hardware scaling
acceptance and optional save/audio/localization features remain separate work.

## Highest priority

1. **Display recovery.** Settings immediately applies and persists resolution and
   window mode (`scripts/settings_panel.gd`, `_select` and `_commit`). There is no
   Keep Changes countdown or automatic revert. Add a timed confirmation for display
   changes and retain the last usable configuration until accepted. Other settings
   can continue applying immediately. Validate timeout, Escape, focus loss and restart.

2. **Checkpoint visibility and failure communication.** Title initialization hides
   Continue whenever `RunSave.read()` returns empty, treating an absent checkpoint
   and an unreadable checkpoint alike. Backup recovery is implemented but silent.
   Continue has no cycle, doctrine pair or saved-time preview. Add a compact checkpoint
   summary and explicit damaged/unavailable/recovered-backup states. Preserve existing
   prototype save behavior; multiple slots or migration are separate decisions.
   Evidence: `scripts/title_screen.gd`, `_ready` and `_continue_loop`;
   `scripts/run_save.gd`, `read`.

3. **Persistent title errors.** `_continue_loop` and `_start_game` write errors to the
   decorative `status` label. `_layout` overwrites that text whenever not starting,
   and hides the label when logical width is below 1300. Give operational errors a
   dedicated, always-visible message area, independent of ambient title copy.

4. **Settings and Back from every major screen.** Doctrine selection exposes Begin
   and Return to Title, but no Settings; its input handler returns before Escape.
   Summary also lacks Settings; Escape attempts to open the pause menu, which is
   rejected because the summary blocks gameplay input. Define explicit Back behavior
   and allow access to Settings without losing the selected pair or completed summary.
   Evidence: `scripts/main.gd`, `_build_doctrine_overlay`, summary construction,
   `_unhandled_input`, `_open_menu`, `_gameplay_input_blocked`.

## Next usability pass

5. **Restore defaults.** Settings has no reset action. Add per-section defaults with
   clear scope; display resets should use the same recovery flow above.

6. **Complete Controls reference and remapping.** Settings lists a handful of keys;
   movement and several actions remain hard-coded in `main.gd`. Provide a complete
   reference first, then rebinding with conflict handling and reset. Do not advertise
   full controller support until placement, camera and menu flows are tested together.

7. **Consistent text-size scope.** Panel scaling now covers shared panels, pause,
   doctrines, journal and summary. Title controls and most station HUD text do not
   use `apply_menu_text`. Either broaden the setting or label its scope precisely.
   Avoid enlarging the HUD without checking playfield and card-space constraints.

8. **Progression details.** The progression page shows doctrine mastery and aggregate
   memory/upgrade counts. It has no list explaining individual recovered memories or
   core upgrades. Add descriptions for records that actually exist; do not invent
   an upgrade shop or change progression rules as part of menu polish.

9. **Player menu versus development tools.** Admin View appears alongside normal
   pause-menu actions. Consider a collapsed developer section or debug-only visibility
   for a player-facing build. Preserve the prototype tool for development.

10. **Credits and build identification.** The title has no Credits/About surface or
    visible version/build identifier. Add a small secondary entry for credits and
    build information so screenshots and bug reports identify the tested build.
    Use verified attribution records rather than guessing contributor credits.

## Coverage gaps, not confirmed runtime defects

- Focus containment explicitly handles Tab/Shift+Tab. Directional focus, gamepad
  navigation and open dropdown interactions need their own tests before claiming
  complete modal input isolation (`title_button_style.gd`, `contain_tab`).
- Current layout fixtures emphasize 16:9 at 1280, 1600 and 2560 widths. Add the
  permitted 960×540 window, 4:3/16:10, ultrawide, multi-monitor changes and OS scaling.
- Save tests cover corruption fallback and a failed write at the storage layer.
  Add UI-level checks for failure during Save & Quit / Save & Return and unavailable
  Continue; verify that the user remains in control and sees a persistent reason.
- Validate title artwork, fonts, popup positioning and display-mode recovery in an
  exported build. Existing native source-project tests do not establish export parity.

## Optional, depending on the intended release

Separate music/effects/ambience volume controls when those audio categories exist;
controller-specific prompts; localization; save slots; autosave with explicit policy;
new-discovery badges and mark-as-read. These are not required to complete the current
prototype menu, and some involve gameplay or persistence decisions.

## Suggested order

First address display recovery, checkpoint information/errors and Settings/Back
access. Then add defaults, controls reference and progression details. Finish with
the expanded navigation/layout matrix and an exported-build acceptance pass.
