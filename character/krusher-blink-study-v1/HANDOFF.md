# Project handoff

Updated: 2026-10-02 · Project: BrineSpace · Task: Krusher facial animation source

## Objective and acceptance
Add an authored facial source to the reusable-body Krusher trial while preserving his established head and body. Begin with a south/front blink reference rather than replacing the current runtime pack.

## Accepted decisions and constraints
Krusher Dom / System Administrator / matte muted cyan AI & Robotics suit. Preserve source identity, size, outline, alpha, hair, beard and body. New anatomy uses builtin image generation; deterministic composition is limited to generated eye-region pixels.

## Current state
Builtin generation 69911178-67b8-450c-9ac4-3b33086898de produced source-blink.png, true-alpha 1136x1384, from reference-head-16x.png. Exact prompt in prompt-blink.txt, provenance in provenance.json. registered-blink.png reduces the full source canvas to the original 23x28 head. build_study.py copies only two eye rectangles [8,14,13,17] and [16,14,21,17] into the original head, preserving original alpha. south-head-closed.png and south-idle-closed.png are study derivatives; blink-reference-sheet.png and blink-preview.png provide review.

## Verification
Only 30 native eye-region pixels change. Head alpha, head outside mask, and body outside mask are exact. APNG decoded to three exact source presentations at 1700/100/900 ms, preserving alpha. Reference sheet visually inspected after correcting clipped annotation text. At small display size the eye change is subtle; this is an unselected authored source study, not final natural-blink acceptance. Source generation changed hair/beard shading, so those areas were deliberately excluded from the derivative. No runtime pack or normal selection changes, no Godot run needed for this reference study.

## Next action
Review blink readability on the actual moving south idle before admitting it into a runtime revision. Half-close, profile sources and helmet fitting remain separate work; do not invent them through opacity fades or mirror the opposite profile.
