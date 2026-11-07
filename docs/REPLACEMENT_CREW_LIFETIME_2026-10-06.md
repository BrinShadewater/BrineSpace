# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: combined-cache scene ownership

## Objective and acceptance
Validate that the preferred compressed replacement-crew prototype releases old
scene resources, preserves save/Continue behavior and avoids accumulating textures
across ten transitions. This is an isolated native diagnostic lane, not packaged
gameplay, a two-hour soak or full release acceptance.

## Accepted decisions and constraints
Normal renderer and selected artwork remain unchanged; Bill remains on its existing
backend. All tests verify scratch user-data resolution before writes and fingerprint
the real owner profile. Fixture construction/resource reserves and suppression of
failures are limited to setup/rendering; both test flags are cleared before the
normal menu-save path. Save validation is preserved, never bypassed.

## Current state
Generators: `output/compressed-crew-2026-10-06/prepare-lifetime.py`,
`prepare-no-studio.py`, `prepare-studio-audit.py`.
Evidence and physical diagnostic scenes: `output/compressed-crew-2026-10-06/bounds-cache/`.
The fixture selects Veld, normally recovers the core, and supplies two completed
finite wards at actual unidentified recovery sites. CryoRecovery creates James
and Marsh's roster entries and emergence. A Crew Hab supplies capacity. Cameras
visit each actor; Studio opens/closes once, then ten normal save/title/Continue
cycles retain all three actors. Separate normal and candidate processes use the
same scene copies and fixture; only renderer selection differs.

Early fixture failures are preserved in named subfolders. The synthetic roster
first lacked corresponding recovered pods; the initial ward lookup then assumed
the retired seeded map rather than current unidentified sites. Save guards also
correctly rejected active fixture flags, and the roster validator rejected adding
architect wards without consuming unidentified sites. These were fixture errors,
not closed production bugs. The final fixture passes unmodified save validation.

## Verification
Candidate: 826 checks, ten transitions, zero behavioral failures.
Normal renderer: 296 checks, ten transitions, zero behavioral failures.
Nine Continue restores compare needs, decision RNG, foot position, active state,
goal and stage for all three actors. Old players release; candidate additionally
proves router, bank, presenter and sampled immutable source objects release via
weak references. Title has no obsolete scene/art leases or surviving library/source
lookups. The final native candidate screenshot was inspected: room, character and
compact needs display render correctly. It is one static view, not full animation
or original-nine-report certification.

Settled title texture memory is **identical between renderers in every cycle**:
182.795 MiB at title_0, 186.555 MiB at title_9 (+2.06%). Static memory:
candidate 222.647→229.937 MiB (+3.27%); normal 223.236→230.530 MiB (+3.27%).
Both stay below the 5% investigation threshold in this lane. Small later increments
are shared; diagnostic rows themselves retain snapshot data. This does not prove
an indefinite plateau or explain every allocation.

Equivalent gameplay rows retain the memory reduction: candidate game_9 1,766.377
MiB versus normal 3,130.109 MiB (1,363.732 MiB less). This four-room fixture does
not certify the 12-room memory gate. Candidate spill count is zero in these settled
rows; it does not exercise the earlier 40-room fixture's 26 simultaneous spills.
First-use and animation-dependent gameplay peaks remain distinct from title states.
All completed attempts preserve all 2,936 owner non-log fingerprints.

## Open warning and next action
The candidate exits with one anonymous `RefCounted`, reference-count-zero warning;
this ten-cycle normal control exits cleanly. Earlier Veld-only normal controls
also warned, but that historical result cannot waive the current candidate finding.
Admission remains blocked on its unexplained warning.

Candidate control with only Studio opening removed: two transitions pass and exit
without the warning. Candidate with Studio and an identity audit: one transition
passes but the warning returns. Studio's effects, stub game and stub grid all
release; their recorded IDs differ from the warned object (normalize signed IDs
before comparisons). Their direct retention is not an established cause.

Next isolate Studio interaction with the private router's registration of newly
added canvases and draw ownership, retaining actual Studio coverage. Do not fix by
removing Studio, hiding warnings or guessing an engine cause. Then repeat preferred
busy workload comparisons, exercise simultaneous spills during scene exit, and
continue startup/PNG-loading optimization. Sustained frame/loading gates, two-hour
soak, original issue closure, packaged Windows and actual Mac remain open.

Follow-up controls exclude Studio registration and its drawing as sufficient
causes. The trigger narrows to constructing the effects-preview StubGame within
the full scene; minimal constructors and minimal helper reloads are clean.
Explicit initialization/factory rewrites do not fix it. See
`STUDIO_CONTEXT_WARNING_ISOLATION_2026-10-06.md` for the control matrix and next
full-scene stage reduction. Normal source remains unchanged.
