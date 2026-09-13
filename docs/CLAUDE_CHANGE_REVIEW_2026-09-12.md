# Project handoff

Updated: 2026-09-12 · Project: BrineSpace · Task: Review Claude changes

## Objective and acceptance
Inspect recent Claude changes for reusable lessons. Review only; no gameplay or art adoption requested.

## Accepted decisions and constraints
User corrected Astra to Claude. Concurrent uncommitted gameplay and art work is outside this review. Recommendations below are not new owner decisions.

## Current state
Reviewed merged side-wall and character mirroring, the Continue fixture fix, and character/pilot/workflow handoffs. Only this review note was added.

Useful practices: test one representative asset through its actual renderer and gameplay scale; record exact generation settings; derive opposite profiles deterministically with geometry/pivot/metadata handled together; preserve authored overrides; use asymmetric fixtures and source-immutability checks; wait for observable state with a deadline; explicitly withdraw disproven claims.

Limits to carry forward: pilot results support local defaults, not universal claims about models; avoid large formatting churn in test registries; distinguish test coverage of geometry from coverage of rendered behavior.

## Verification
Read committed diffs for a2bebbef, 7fafaa9e and 7cfa1dc5 and the associated current notes. No tests or new visual acceptance performed.

Static inspection found that mirror_registration() always sets mirrored=true. Applying it twice restores polygon coordinates but leaves source_uv() reflecting texture coordinates. The double-mirror test checks polygons only. Current loader uses a single mirror, so this does not establish a present gameplay regression.

The side-wall test also assumes both loaded sides are authored before reaching its opt-in checks; a future fixture with a genuinely missing opposite side will need to distinguish authored and derived registrations.

## Next action
Review complete. For future mirror work, add an isolated opt-in side-wall fixture and check complete geometry/UV behavior. No changes to the active implementations made.

## Expanded review: testing, gameplay fixes and release work
The initial review underweighted the September 10–11 engineering work. Follow-up inspected commit records for fe5a96ec, c7a4bb38, 30d8805d and 980529df; the icon-loader fix 8d701dba; the test runner; and bug-fix, performance, workflow and release notes. No fresh suite or benchmark run.

- Classify failures before editing: real regressions, superseded expectations, fixture contamination and unsupported headless rendering required different remedies. The recorded closeout was 112 headless passes, 1 skip, 54 native skips and 0 failures; the native layout lane separately had 7 passes. These are historical scoped results, not certification of today's changing checkout.
- Exercise transitions: oscillating flood thresholds starved personality actions; restore replayed alerts; a refuge became unsafe during travel; deferred UI work outlived its panel. Steady-state assertions miss these interactions.
- Isolate memory as well as save paths: redirecting MetaState had to reload/reset its in-memory profile. Real unlocks otherwise contaminated fixtures.
- Keep tests aligned with accepted behavior without weakening their purpose: required animation directions are more stable than exact clip counts; paid construction and thaw need real progression; navigation checks should follow actual path legs.
- Make optimization falsifiable: same-build opt-out flags, real pixel comparisons, mutation/invalidation cases and pre-change reproduction distinguished gains from regressions. Recorded 100-room fit time improved 74.81 to 61.40 ms; it still missed 60 fps.
- Consolidate duplicated rules at narrow seams: shared Studio/live placement envelopes and raw texture loading removed concrete sources of drift without a monolith refactor.
- Validate packaged consumers: pack reduction from about 5.8 to 1.2 GB exposed resource-icon loading assumptions. File presence and successful export do not establish correct UI or release behavior.
- Several practices are already in AGENTS.md and RELEASE_WORKFLOW.md. Apply those instructions consistently instead of adding another competing checklist.
