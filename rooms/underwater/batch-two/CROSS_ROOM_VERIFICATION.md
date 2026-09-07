# Combined room-batch connection sweep

The batch-two connection manifest identifies its ten registered views without
duplicating source provenance or asserting art acceptance. It can be supplied as
`--additional-manifest=res://rooms/underwater/batch-two/connection-manifest.json`
to the existing production-ten connection and walker-path tests. Their original
ten-room default remains unchanged.

This tests both sessions' twenty rooms together, including same-room pairs,
ordered pairs, all sixteen rotation combinations and all four boundary sides.
Expected sockets come independently from RoomDatabase. The connection test also
rejects duplicate manifest identities.

`output/twenty-room-connections-v1.log`: 25,600 pair configurations, 10,404
compatible boundaries, 1,050,804 centerline standability samples, zero failures.
Incompatible boundaries remain non-traversable. The banner was renamed afterward
from TEN ROOM CONNECTIONS to REGISTERED ROOM CONNECTIONS for expanded-batch clarity.

The separate production-walker sweep includes each supported previous entrance
and the rendered foot offset. The initial v1 sweep found 110 Holographic Core
projector contacts. The focused v1 sweep reproduced all 110; moving its authoring
x from -168 to -172 cleared them without resizing the prop or changing paths.
The focused v2 sweep passes 706,192 samples with zero failures.

`output/twenty-room-walker-v2.log`: 25,600 pair configurations, 10,404
compatible boundaries, 4,162,008 production-route samples, zero failures.
The successful full rerun contains no ERROR or SCRIPT ERROR entries. Failed v1
logs are preserved as diagnostic evidence. Neighbor-dependent ingress coverage
matters: a single reference-room pairing did not expose this marginal clearance.
Neither sweep proves pixel-perfect seams, sprite occlusion or autonomous runtime
state transitions. Native review, fine art cleanup and packaging remain separate.
