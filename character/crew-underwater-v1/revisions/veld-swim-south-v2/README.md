# Veld south camera correction — candidate

Six independently generated poses match the steep overhead south-swim camera
established by Bill's revision while preserving Veld's hair, blue shoulders and
left-hip scanner. Source and exact prompt are preserved under `generated/`.

Rebuild with `python character/crew-underwater-v1/build_south_revision.py --actor veld`.
The shared builder uses actor-specific source shoulder measurements and scale,
with canvas 104 x 112 and shoulder pivot (52,76). All six crops fit with margins.
Contact inspection shows the full torso and leg stroke; late recovery/reach
similarity still needs continuous loop review. This candidate has no helmet
fitting and is not loaded by the runtime. Branforth's matching correction remains
outstanding.

Current status: provisionally integrated. Native phase checks pass all six bare
and helmet phases through the normal loader. Southbound movement, turning and
continuous motion review remain outstanding; earlier candidate notes above
describe the packaging stage.
