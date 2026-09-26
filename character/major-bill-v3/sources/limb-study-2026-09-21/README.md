# Independent limb sources — integrated September21

These independently generated east/west sources drive the selected Bill side-walk surface repair through tools/rebuild_bill_art.py and tools/repair_bill_walk.py. No mirroring or Higgsfield. Raw source, exact prompt and source hash/registration are retained per direction.

Production: python tools/rebuild_bill_art.py
Review-only export: python tools/build_bill_limb_candidate.py --output output/bill-limb-rebuild

The historical candidate filename remains; its repair function is now used by the canonical build. The CLI only writes under output/. The build uses authored body/helmet inputs, existing gait trajectory, original upper motion and complete original foot rectangles. It never reads temporary output images as source.

Exactly24walk frames changed in integration; other generated assets and metadata matched the snapshot. Agent reviewed pose transitions and native phase captures. Full owner motion acceptance and live expedition review remain open; this does not claim all gait issues are solved. See docs/BILL_LIMB_INTEGRATION_2026-09-21.md.
