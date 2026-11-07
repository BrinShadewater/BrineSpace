# Branforth south camera correction — candidate

Current source is candidate 03: second pose uses a compact bent-elbow catch.
The original wide sweep blocked the south doorway. Rebuilt body/helmet envelopes
now pass the furnished 19-node southbound route at unchanged body scale and
collision margins. Candidate 02 remains preserved for comparison.

Six poses use the same overhead projection as Bill and Veld, preserving orange
shoulders, grey hair and forehead goggles. Source and exact prompt are preserved.
Rebuild with `python character/crew-underwater-v1/build_south_revision.py --actor branforth`.

The source's second and third silhouettes overlap in horizontal projection but
remain disconnected. Connected-component extraction separates their actual pixels
instead of slicing at a guessed gutter. Six major components were extracted;
contact inspection shows intact reaching hands and feet. Canvas is 104 x 112,
shoulder pivot (52,76), with independently measured source anchors.

This is a candidate, not a runtime replacement. Helmet fitting, continuous loop
review and native north/south turning comparisons remain outstanding for all
three corrected south packs.

Current status: provisionally integrated. Native phase checks pass all six bare
and helmet phases through the normal loader. Southbound movement, turning and
continuous motion review remain outstanding; earlier candidate notes above
describe the packaging stage.
