# Project handoff

Updated: October 1, 2026 · Brine Space · Bill paired south rest

## Objective and acceptance
Full master-consistent Bill set, then cross-animation polish.

## Accepted decisions and constraints
Preserve selected masters, fixed source rulers, matte materials, owner saves and selected east bunk.

## Changed files and current state
New character/bill-rest-helmet-south-coherent-v1 sources, build/prepare scripts, manifest/frames, preview, verifier and evidence. New tests/test_bill_rest_helmet_south_candidates.gd with UID and tools/run_bill_rest_helmet_south_candidate_validation.py. No normal runtime selection changed.

## Checks and remaining work
Bill paired south generic rest candidate — October 1, 2026.
Three shared-helmet states, eight entry poses800ms, exact reversed wake800ms,
two sleep poses1200ms. Exact selected south equipped idle; interleaved body
registration follows each source record's frame index, preserving the approved
bare body/timeline. Existing authored axial front helmet projections reused from
bill-death-ground-helmet-south-coherent-v1 (exec-cad07484-a967-44cd-a49a-4533e1a6d26e),
fixed [.30,.31] component ruler, saved matte curve and face gain. Source/prompt
copied locally and authority/source hashes checked. Supine eyelids reuse authored
closed-eye donor exec-0b1ad8c7-6822-4afb-816d-f4980cb3c9fe in16 bounded RGB
pixels of the pitched component; hardware outside these regions and all alpha
remain exact. Identical sleep helmet component and position across both body
breathing poses.31 package checks and110 native player checks pass; native148/82
static board reviewed against selected equipped idle. Fine neckline, facial
identity, reclining perspective and live cadence still need full-set polish.
Runner 14.14s; native exit0; overall passed=False.
Strict full owner-profile guard changed ['last_session.json'], across
2,931 non-log files. Scratch APPDATA confirmed;
attribution unproven, guard failure retained, no clean-interval retry or owner
restoration. Candidate remains staged. Current habitation provides the selected
specialized east Bill bunk; no south furniture, route, interruption or Continue
proof. Next west paired rest, relevant family integration and full-set polish.
Full Bill goal remains active; no commit/export.
Lesson: interleave helmet fitting by explicit body frame index when source
atlases contribute noncontiguous timeline slots. Hash-bind reused authored
eyelids and validate exact wearable pixels outside the declared face region.

## Next action
West bare/shared-helmet rest, compatible integration and whole-set motion/master polish.
