# Medical Office — integrated, September 6

Tenth integrated room in this task's batch; live station/card consumers select v1.
Original source remains intact. med-office-card-v1.png is a native offline
candidate. The verified Medical Center supplies pale Medical floor and cladding;
the source's dark deck is not adopted. NS sockets remain engine-owned.

Four registered groups: records desk, storage cabinet, examination couch with
diagnostic console and consultation chairs/table. All stay south-facing. Couch/
console and consultation furniture use separate rendered polygons to avoid source
floor patches between pieces. Collision still reserves each group's footprint.

Only the visible examination console has operating readouts. The desk monitor
shows its rear, so it remains static; no readout is painted onto its back. Cabinets
and chairs also remain static. These are equipment-readiness cues, not patient
vitals or new survivor mechanics. Existing source material/indicator details still
need the broader fine-cleanup pass.

Evidence under output/:

- med-office-registration-v1 passes four-rotation full bounds, piece containment,
  static-host expectations and 4,320 source-surface effect samples.
- med-office-pilot-v1 passes per-host working/offline comparisons in all rotations
  with one active host and three static hosts. Direct renderer state, not economy.
- med-office-card-v1 rendered and visually inspected.
- med-office-depth-v1 captures 32 standable production-actor poses; q0's eight
  poses reviewed in med-office-depth-q0-v1.png. Integration reviewed the remaining
  24 in med-office-depth-q1..q3-v1.png, completing all 32 static pose reviews.

Live evidence: med-office-state-v1, med-office-state-1280-v1 and
med-office-state-2560-v1 pass four rotations, four actual economy states including
restoration, one animated/three static hosts, pause and 808 canonical socket
samples. med-office-station-v1 passes four rotated neighbor pairs with 404
production walker samples and mixed 40-room fit. med-office-four-rotations-v1.png
visually inspected; the complete seam capture set is not yet visually accepted.

med-office-test_synergy_manager-v1, test_discovery_progression, test_polish_gameplay,
test_run_balance and test_med_office_registration v1 pass. Latest successful
state/station/regression logs contain no ERROR/SCRIPT ERROR entries. Existing
raw-image warnings remain; these checks do not establish release export.

All ten rooms now have live integration with scoped native evidence. Remaining:
fine cleanup, broader cross-room/ingress tests, package/export and owner approval.
Neither this room nor the batch is declared fully accepted by the integration count.
