# Project handoff

Updated: 2026-10-02 | Project: BrineSpace | Task: reusable body family fitting

## Objective and acceptance
Continue Krusher's body reuse trial with a reviewable comparison of Bill, Veld, James and Marsh. Establish static head fit before considering alternate animation reuse.

## Accepted decisions and constraints
Krusher Dom, System Administrator, AI & Robotics, matte muted cyan. Existing Bill candidate retained. Other family suits keep source colours in this comparison; no owner base choice inferred. Existing extracted cardinal heads reused at their original native dimensions. No new anatomy generated.

## Current state
build_study.py creates 16 static PNGs and family-fit-comparison.png. verification.json records source/output hashes and placement offsets. Bill row uses the existing runtime candidate. Alternate rows use preliminary collar cutoffs Veld 51, James 50, Marsh 51; every source body pixel from that row down remains exact. All normal selections remain unchanged.

## Verification
24 head/body byte-fidelity checks pass. Initial full RGBA comparison exposed alpha-compositing changes in transparent head pixels; copying the head directly onto the cleared region preserves the native source exactly. Both initial and corrected sheets visually inspected. Corrected sheet shows distinct builds and per-family collar placements. No Godot run required for static source comparison; this does not establish animated neck joins, helmets or recolouring compatibility.

## Next action
Optional owner priority question remains pending: finish Bill-based Krusher, explore another Krusher base, or build all four reusable templates. Bill is the current recommendation. For alternate template production, refine source-aware collar masks, author family-specific marking masks, then check representative idle/walk and helmets. Current comparison is a preliminary fit study, not approval or runtime adoption.
