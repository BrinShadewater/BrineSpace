# Medical Bay and Reactor repair package check

Standalone Windows validation v13 includes Medical Bay card v5 and Reactor card
v3 through `rooms/whole-room/export-manifest.json`. Both current sources retain
their recorded hashes; all six manifest entries pass source hash, 512-square card
and central card-catalog checks. The five applicable grid fallbacks match too;
Nursery has no duplicated card path in that grid table.

Evidence: `output/batch-two/windows-validation-v13/verification.json`.
PCK SHA256: `DDEA52EE4914B01899F31DFE53500DB00D76EB17E9C14225BA77DE807DD25F5F`.

- Export and external-working-directory runtime checks pass with zero exit and
  no ERROR/SCRIPT ERROR entries. Existing raw-image loading warnings remain.
- Six whole-room subjects plus ten production subjects: 16 source hashes and
  32 raw PNG decodes pass, with eight supporting trunk rooms.
- Controlled production movement reaches all 24 rooms: 24 arrivals, 62 reciprocal
  transitions and 4,734 collision/speed samples. Destinations are scheduled, not
  chosen autonomously by the NPC.
- Full-frame state-sidecar PNGs independently measure 1600x900.
- Reviewed `controlled-tour-start.png` and `tour-arrival-22-med_bay.png`: Medical
  Bay and Reactor interiors are present in the lower station row. At roughly
  22% zoom these are loading/layout evidence, not fine contour acceptance. The
  objective overlay obscures some other rooms at lower left.

The native individual-room contour/state tests remain separate evidence. V13
does not run those individual Medical Bay/Reactor fixtures through its selector,
and does not establish three-size packaged state coverage, every doorway seam,
autonomous behavior or release approval. Existing source/card versions survive.
