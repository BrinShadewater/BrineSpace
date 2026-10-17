# Project handoff

Updated: 2026-10-02 | Project: BrineSpace | Task: James body muted cyan trial

## Objective and acceptance
Extend representative alternate-body reuse by testing department recolouring on the James south idle/walk head-fit candidate. Preserve source identity, body, tools, clock and registration.

## Accepted decisions and constraints
Krusher Dom, System Administrator, AI & Robotics, muted matte cyan RGB 82/124/128. James tools keep their original colours. Current Bill-based candidate retained. Alternate static families remain proposals, not selected characters.

## Current state
148 candidate PNGs, two-state manifest, per-frame marking masks, provenance and validation scripts. build_study.py changes only yellow preserved upper-suit pixels outside the preceding head-fit edit mask, stopping above the utility/tool region. Source luminance supplies shading, capped at 1.15 times the base cyan to keep highlights subdued. Alpha untouched. Mask changes 381-494 pixels per frame. review/bill-james-comparison.png compares both cyan bodies. Before/after APNGs and 7.5-second source-derived MP4 retained; no continuous native capture claim.

## Verification
444 composition checks and 756 independent source/output/metadata/alpha/protected-pixel checks pass. Existing sprite-player native probe: 446 checks, zero errors, Godot exit 0/5.00 seconds. All 2,930 owner files unchanged under scratch APPDATA. Comparison and walk before/after sheet visually reviewed. Normal selections unchanged. These checks prove scoped source recolouring and frame compatibility, not temporal polish or complete alternate-family readiness.

## Next action
Review the supplied moving before/after and Bill/James comparison. James east/north/west and helmets remain unchecked; Veld/Marsh need their own representative motion and palette masks if reusable-family production is prioritized. Keep original sources and earlier yellow fit candidate. No owner approval or base choice inferred.
