# Veld west stutter repair

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner says east looks okay; west stutters. Preserve east and repair west sequence.

## Accepted decisions and constraints
New side masters and idles approved; east side-walk-v1 accepted for visual motion.
No runtime promotion or mirrored equipment. No procedural invented poses.

## Current state
character/veld-side-walk-v2 contains west repair: first half uses v1 frames2/0/1,
second half three newly authored opposite-step poses from approved master only.
150ms equal west durations; original east frames/timing retained exactly.
Sources, exact prompt, local build script, manifest and before/after GIF retained.

## Verification
Inspected new source and six-frame contact sheet. Opposing arm swing now present.
Extraction and manifest validator pass; all six east files byte-identical.
No native runtime/foot-contact validation. New half shows increased far-side
canister exposure/detail variation; owner loop acceptance pending. Do not claim
technical validation proves stutter fully resolved.

## Next action
Review west-before-after.gif. Tighten gear/body joins after assessing gait;
retain accepted east unchanged. Inspection and other-character work pending.
