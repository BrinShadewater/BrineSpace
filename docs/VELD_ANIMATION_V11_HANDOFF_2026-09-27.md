# Veld targeted correction handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner requests B/E/G darker brown hair and slightly darker faces; C hair fuzz near
frame six; F more silver equipment. Keep the A-G review labels.

## Accepted decisions and constraints
Deterministic colour edits preserve poses/timing. A and D untouched this pass.
No production promotion. Owner visual acceptance pending.

## Current state
character/veld-animation-pilot-v11: east brown-hair luminance multiplied by .75,
east face target percentiles by .94; separate silver streak preserved. F receives
the existing independent bright-equipment exposure restoration. C hair-edge
magenta residues replaced with nearest opaque non-magenta head colours, retaining
every alpha pixel. No synthetic poses or silhouette edits. Native review tool
supports v11; its UID retained. Review-all GIF and head audit included.

## Verification
42 alpha masks unchanged. A/D twelve frames byte-identical. Manifest clean;
160 native checks pass; all 2670 real-profile hashes unchanged in isolated run.
Native playback capture and enlarged six-frame rear-head strip inspected.
C source strand/highlight variation remains; owner should confirm whether the
reported fuzz was the removed edge residue or a further temporal issue.

## Next action
Review updated A-G GIF. If C still flickers, isolate the specific strand/highlight
without replacing approved body motion. Front/rear walk drafts remain held.
