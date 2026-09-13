# Animation acceptance ledger

`clips.csv` inventories all 480 body clips and 328 human equipment variants.
Regenerate with `python tools/crew_animation_ledger.py`. The script preserves
manual status/evidence fields and flags clips whose selected pixels, pivot or
timing changed. It does not infer visual approval from manifests or test counts.

Current body categories: 12 instrument, 12 repair, 36 daily-life, 24 death,
148 water-related, and 248 other motion/transition clips. Equipment variants are
tracked separately so they do not inflate body-action counts.

The instrument batch has sampled native clip review and selected-source checks;
continuous live-context review remains. Repair, daily-life and death form the
72-body-clip review/rework queue discussed with the owner. The remaining rows
need prior evidence reconciled: several cargo, gait and rest batches already have
recorded review. An unresolved row does **not** mean its art needs regenerating.

Use specific evidence for each accepted row. Do not declare a completion
percentage until prior review is reconciled and the remaining visual scope is
known. Water includes swimming, treading, recovery and salvage; death-water is
counted under death, not twice. Marsh's legacy equipment-named body states remain
inventory entries, not authorization to add a helmet.
