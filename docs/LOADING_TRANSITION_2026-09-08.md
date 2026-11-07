# Title-to-station loading transition

The title now presents a root-owned, opaque BRINE loading screen before loading
the game scene. It survives scene replacement and waits for `startup_complete`,
including staged checkpoint restoration, then a covered rendered frame before
removing itself. Resource loading uses Godot's threaded loader; synchronous
gameplay initialization can still pause the indicator while the screen remains
visible. There is no artificial percentage. A scrolling deep-time transmission
now accompanies startup: a distant stellar signal wakes BRINE beneath an alien
ocean. It reveals at 35 characters per second with a two-second final reading
pause. Enter or a left click skips the narrative, but never skips scene readiness.
The gameplay subtree is disabled while the remaining transmission plays so the
station cannot spend resources behind it. Reduced motion presents the full text
immediately and adds no narrative delay.

The transmission shares the title's terminal typography and palette. Failed
resource preparation or scene replacement restores the title's
buttons and existing retry message. New Loop and Continue retain their existing
checkpoint handling.

Native Godot 4.6.1 verification: `--path . --script
res://tests/test_loading_transition.gd`. Optional `-- --capture-dir=<directory>`
writes loading-screen evidence. New Loop and Continue passed, including preserved
checkpoint reserves, loading coverage during restoration, cleanup after startup,
and reduced-motion presentation. The extended check covers Enter-to-skip, a frozen
gameplay subtree during the narrative, and the complete reduced-motion transcript.
Native screenshots were visually reviewed.
No script/runtime errors remained; existing raw-image export warnings were emitted.
No export build was produced.

The launch exposed an existing inferred-type parse error in
`rooms/full-wall-v1/full_wall_prop.gd`. Its local side-registration path now has an
explicit String type, allowing room renderers to compile.
