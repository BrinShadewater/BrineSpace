# Salvage facing handoff

## Objective
Continue the full room-facing rollout, including previously custom art families.

## Decisions
Keep live north bench and move it back to overlap riser slightly. Install overhead
southwest tote; retain original carried tote. New south bench remains a library
variant because a continuous bank conflicts with this host's south doorway.
Source omissions: two hammers and one small bin after unsuccessful facing edits.

## Changed files
assets/salvage-directional-v1 contains sources, rejected revisions, exact prompts,
registrations, prior defaults and new card. Two registrations in full-wall-v1.
workshop_view.gd supports library rendering and installs overhead tote. Default
q0 positions and both card bindings updated. Coverage, current status, rollout,
bible and maintained/installed full-wall lessons updated.

## Verification
Native q0 before/after and card reviewed. South bench isolated diagnostic renders
correctly; diagnostic does not establish wall fit. Tests pass: 176 routes, 20 side
variants, 188 layout keys, 47 card identities. Source/card LFS attributes confirmed.
No export, no personal save changes, no claim of owner acceptance.

## Remaining
East/west workshop companions; valid south bench host fit. Many other catalog
directions remain pending in assets/room-facing-rollout/coverage.json. Full goal
remains active. Continue the next missing family from current evidence.
