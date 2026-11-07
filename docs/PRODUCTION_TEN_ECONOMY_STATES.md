# Ten-room economy-driven visual states

`tests/playtest_production_ten_economy.gd` passes at 1600x900. It creates each
requested room in an isolated station fixture and drives supplied, depleted,
suspended and restored states through the real `_apply_room_economy()` function.
It does not assign working-cell overrides during these forty checks. Resource
reserves are fixture inputs (20 per resource supplied, zero depleted), and room
suspension is set explicitly. Production rules and failure settings are unchanged.

Each state checks the resulting working-cell membership and offline reason when
applicable, then compares two rendered frames. Animated hosts move only when
the economy marks the room working; passive rooms remain visually still. Rooms
without input requirements correctly remain functional with empty reserves.
Restoration resumes eligible visuals. All 40 state/frame pairs pass, process
exit is zero and stderr has no ERROR/SCRIPT ERROR entries.

Evidence: `output/production-ten/economy-1600.log`, `.err` and
`economy-native-1600/<room>-<state>-a/b.png`. Inherited raw-image warnings remain.
These batch states use each room's base orientation. The inherited fixture also
captures nursery rotations before the batch; its generic final banner must not
be read as four-rotation economy evidence for these ten rooms. Separate per-room
fixtures cover rotated active/inactive art with injected states.

This proves the economy-to-rendering connection under controlled reserve changes,
not organic multi-cycle balance, UI suspension clicks, actor crossings, pixel
seams or standalone export. Those remain separate verification scopes.
