# Project handoff

Updated: 2026-09-30 · Project: BrineSpace · Task: Marsh master comparison

## Objective and acceptance

Owner requested comparison of all animations to masters. Completed read-only visual audit of 204 selected states / 1,058 slots against four standing identity sources and selected idle export anchors. This establishes remaining visual differences, not owner acceptance or new motion certification.

## Accepted decisions and constraints

Original directional masters in character/marsh-motion-polish-v1/sources/*-standing-identity-01.png are identity/design authority; installed idle is runtime scale/material anchor. Preserve asymmetric hardware, white android injury fluid, authored scale/pivot/timing, pose-specific perspective and coherent anatomy.

## Current state and changed files

Added character/marsh-master-comparison-v1/index.html, seventeen complete frame boards, hashed comparison.json and findings.json; tools/compare_marsh_masters.py reproduces the review. All selected frames appear beside the matching idle. Interactive comparison shows high-resolution original masters, registered selected idle and current timed animation; turns show both master directions. Source/station scale, pause and frame stepping are available. Production artwork/catalog unchanged.

## Findings / remaining work

1. Cargo, pickup/unload, cargo turns/drain and swimming pickup: simplified panel construction, straps/pouches and more stylized side faces; idle endpoints expose the detail change. Highest source-detail repair priority.
2. Swimming turns and loaded swimming: brighter cream interior poses, rounder panels and simplified cargo detail. Unloaded turn ivory-mask range reaches approximately 30 sRGB mean units; masks differ with pose and this is a review flag, not an exposure prescription.
3. Diagnostics: canonical head/boots match; working torso/arms still smoother and less detailed than master. Refine coherent source body without arm stencils.
4. Run, seated/rest/fallen and recovery: some face/panel drift; posture and foreshortening explain reduced bounds. Preserve white injury effects and furniture registration.
5. Idle, conversation, walk and welding are closest anchors. Eating/drinking and ordinary swimming retain identity but have some simpler working detail.

Full per-group findings and per-state grouping are in comparison.json. Colour grading alone cannot restore missing authored construction detail. Runtime selections remain unchanged pending subsequent repair work.

## Verification

Inspected four original masters and all seventeen all-frame boards. Verified 204 states / 1,058 slots, all source paths, four source hashes, and maximum nine authored slots fitting boards. Viewer JavaScript syntax passes. Static all-frame review does not certify complete animation motion; interactive controls supplied but not exercised in browser. No Godot test/probe required or run for this read-only comparison; no player profile access.

## Next action

Review character/marsh-master-comparison-v1/index.html; repair cargo and swimming interior pose detail/materials first, then diagnostic working body and remaining face/panel drift, preserving shared joins and validating changed motion.
