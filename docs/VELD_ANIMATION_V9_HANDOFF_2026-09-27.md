# Veld east exposure handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner reports east animation too bright. Attached image is held rear-walk draft;
east clips corrected as requested, while rear draft remains rejected for equipment.

## Accepted decisions and constraints
Deterministic exposure only, preserve poses, selected design and separate skin/blue
targets. No runtime installation or claim of owner visual acceptance.

## Current state
character/veld-animation-pilot-v9 revises east idle/walk/inspection. The old cloth
measurement excluded luminance above 0.43, biasing bright-source measurements;
minimum exposure gain 0.72 also limited correction. East now measures neutral thigh
fabric in source y 0.51..0.60 without an upper luminance exclusion, target 0.272
from front idle. Global suit exposure changes, with skin/blue overrides retained.
tools/review_veld_pilot.gd supports v9. Earlier source/version files remain intact.

## Verification
42 frame alpha masks identical; 24 non-east frames byte-identical. Manifest clean.
160 native checks pass; 2670 real-profile hashes unchanged using scratch APPDATA.
Native 148px/45px capture reviewed against previous version and locked turnaround.
Before/after image and exposure audit stored with candidate. No pose/timing change.

## Next action
Review east exposure with owner; assess west against same fabric measurement next.
Front/rear walks still need corrected phases/equipment; inspect magenta fringes
against light backgrounds before production promotion.
