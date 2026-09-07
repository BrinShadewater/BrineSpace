# Older layered room export manifest

`export-manifest.json` records the six older layered room identities, their
selected raw sources, SHA256 hashes, current cards, views and canonical sockets.
It is consumed by the same combined export fixture as the production batches.
Keep source/card paths synchronized with the view and shared card catalog when
revising art. This inventory does not grant visual acceptance to older sources.

BRINE Core and corridor/corner are separate asset structures and are not covered
by this six-room manifest. The manifest extends the 25-room combined asset set
to 31 distinct identities, plus supporting Battery Arrays in the fixture.

The first 31-room controlled tour hit the harness's 60-second runtime timeout
after 34 arrival captures. It is retained under
`output/room-rollout/windows-31-current-controller-v1`. Asset hash/decodes passed,
but that run does not prove completed traversal. The export command now accepts
`-RuntimeTimeoutSeconds` (60–300; default 60) for explicitly bounded larger tours.

The v2 run with a 120-second allowance completed: 31 selected source hashes,
62 raw PNG decodes, 47 physical arrivals, 125 reciprocal transitions and 9,606
collision/speed samples. Evidence:
`output/room-rollout/windows-31-current-controller-v2/verification.json`.
It ran from a fresh external directory with no assertion errors. This is one
scheduled graph traversal, not arbitrary topology or close-up art acceptance.
