# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: packaged loading repeatability and large-station lifetime

## Objective and acceptance

Continue the full PC/Mac performance and release plan. Loading targets remain ≤10 seconds cold / ≤6 seconds warm, responsive progress, with equivalent workload and hardware certification. Large-scene texture budget remains ≤3 GiB; ten transitions do not substitute for the two-hour native soak.

## Accepted decisions and constraints

The cold-hint/drone candidate is experimental, not admitted into normal source. Preserve selected pixels, clocks, filters, metadata, save bindings and gameplay. All probes use verified scratch profiles and fingerprint the owner's files. No release upload authorized.

## Current state

Candidate `81365a7987632800`, retained under `output/drone-compiled-2026-10-07/cold-hints-release/`. Three fixed-site packaged comparisons are consolidated in `cold-hints-three-pairs-summary.json`. Large fixture uses normal placement/save/Continue with fixture-only resources/free-building/failure controls; external adapter and identity retained in `qa-cold-hints/`. Small adapter is preserved as `small-loading-before-large.gd`.

## Verification

- Six debug=false processes: 142 checks each, zero failures/engine errors/exit warnings. Median first New Game improves 12.446→6.960 seconds (~44.1%); Continue 4.984→5.119 seconds, mixed. All 18 retained library source-list endpoints match; texture differences zero or four bytes. OS cache uncontrolled; this is local repeatability, not full cold/warm certification.
- Large two-cycle fixture: 182 checks, clean. First 40-room Continue 7.661 seconds; restore stage 2.913 seconds, target fails.
- Large ten-cycle fixture: 824 checks, clean. First Continue 7.739 seconds; later Continues 4.837–5.054 seconds. All restores preserve tested crew/fleet state and exactly 40 rooms. Owner's 2,936 non-log fingerprints unchanged.
- Title texture counter rises 271.361→310.170 MiB at first restore return, then reaches 310.951 MiB at cycle nine. After cycle two it increases ~36 KiB per transition. Causes unassigned; memory-growth acceptance remains open despite clean exit warnings. Title session owners/library images/live shared source storage all zero.
- Gameplay texture counter ~3.79–4.38 GiB, above budget; activity varies, so endpoints are not an equivalent-state slope. Release static-memory monitor returns zero and is unavailable, not proof of zero RAM.
- First large restore ~2.911 seconds versus later ~0.616 seconds within the restore stage. First three observations justify targeted attribution; no root-cause claim yet. Large station capture inspected.

## Next action

Attribute checkpoint application, crew navigation restoration and final refresh before fixing the first-restore delay. Investigate title retention independently. Restore small QA adapter after large fixtures. Continue compressed-provider admission, matched gameplay pacing, original packaged bug/UI review, memory/soak, target hardware and native Mac certification. No release gate is closed by these local checks.
