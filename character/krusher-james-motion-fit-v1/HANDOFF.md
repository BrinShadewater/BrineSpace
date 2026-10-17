# Project handoff

Updated: 2026-10-02 | Project: BrineSpace | Task: James body moving neck-fit trial

## Objective and acceptance
Exercise representative moving head/body reuse on an alternate family before expanding reusable templates. Source south idle and walk, consistent density, clocks and registration; no NPC integration implied.

## Accepted decisions and constraints
Existing Krusher south head reused without resizing. Current ACTIVE_ASSETS James/Branforth locomotion source resolved at build time. Original yellow suit colours, tools and body retained for fit diagnosis. Current Bill-based Krusher selection remains unchanged; optional owner priority unanswered.

## Current state
148 PNGs, two-state manifest, protected edit masks and source hashes. build_study.py tracks the source head top/axis, translates family-specific collar boundaries, layers original collar pixels over the new head, and preserves lower-body pixels. Observed head shifts x 0..1, y -3..0. South walk source cycle 4,500 ms; idle 3,000 ms. review/motion-preview.mp4 is a 7.5-second, 604,523-byte source-derived side-by-side 60fps preview, not native continuous capture. APNGs, enlarged neck samples and two native samples retained.

## Verification
296 composition checks and 460 independent source/output/metadata/protected-pixel checks pass. Godot existing consumer: 446 checks, zero errors, exit 0 in 5.02 seconds. Every frame midpoint resolves to exact candidate pixels; pivot and standing ruler unchanged. Scratch APPDATA; all 2,930 owner non-log files unchanged. Idle/walk neck sample boards and native walk image visually reviewed. PNG LFS attribute confirmed. No obvious join break in sampled poses; full temporal artistic acceptance remains unproven.

## Next action
Review the supplied continuous preview for head/collar movement quality. Then test remaining directions or another family's representative motion according to owner priority. James recolouring and helmets still need family-specific work. This does not prove complete cross-family compatibility or station/controller behavior.
