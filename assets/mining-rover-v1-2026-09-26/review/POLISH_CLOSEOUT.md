# Rover audit repairs

September 26, 2026. The owner authorized fixing the three audit findings before
starting the next drone. These changes supersede the open findings in ART_AUDIT.md.

- Selected `sources/diagonals-v5-polished.png`: restrained gray-cyan materials and
  smaller tyre studs on all four diagonals, preserving the registered wheel hubs,
  single front drill and independent headings. Original sources remain preserved.
  Native light/dark board reviewed after rebuilding; residual hand-painted view
  differences are not a claim of pixel-identical perspective reconstruction.
- Corrected the tyre projection so rolling frame zero exactly equals the source
  pose in all eight headings. The previous thousands of changed startup pixels
  are now zero (`art-audit-metrics.json`; previous metrics preserved separately).
- Exported 60 shared wheel-layer phases per heading in `headings.*.wheelAtlas`.
  The preview holds the braking phase across every work/power action and departure.
  Future consumers must composite this layer over stationary work bodies before
  effects/cargo; playing independent body atlases alone cannot preserve arbitrary
  incoming tread phase. Near-opaque tyre interiors are opaque in this overlay;
  the body silhouette and transparent perimeter remain outside it.

Validation passed: all 112 clips / 7,920 body/effect frame references; 32 rolling
clips / 1,920 frames; exact reverse, loop seams and connected steering; 480 wheel
layer phases; all work/power poses compatible with their frozen wheel overlay;
motion-controller joins. The browser completed the full work cycle without errors.
Revised northeast rolling inspected at quarter speed; native direction board and
updated loaded/state boards reviewed. No gameplay or owner save changes.

Rebuild remains pilot -> directions -> tyres -> completion -> review_pack.
Then run `build_completion_review.py`, `validate_tyres_v2.py`,
`validate_wheel_layers.py`, `node test_motion.mjs` and
`python review/audit_registration.py`. See `POLISH_PROMPTS.md` for exact generation
prompts. Scope moves to the Salvage pilot at http://127.0.0.1:8771/.
