# Eight-frame Veld side walks

Owner requested increased frame count. East/west expanded from4 to8 with newly
authored in-betweens, not duplicated holds. All eight original keyframe PNGs are
copied byte-for-byte into even zero-based frame slots; new frames occupy odd slots.
225ms key intervals split112/113ms, preserving900ms cycle duration per direction.
GIF timing uses110/110/110/120ms repeated to preserve900ms with10ms resolution.

Built-in image_gen used each direction's latest four-frame source as reference.
Exact prompts and raw results retained. No palette edits. Clip-wide new-source
scale; no per-frame scaling. Rebuild with build_review.py.

eight-frame-review.gif shows east left/west right at enlarged/gameplay scale.
contact-sheet.png labels retained keys and new frames. Manifest validator clean.
Inspected both sources and contact sheet. New arm/equipment silhouettes and
in-between staging still need motion review; increased count is not proof of
smoothness. No native stride calibration or runtime selection changed.
