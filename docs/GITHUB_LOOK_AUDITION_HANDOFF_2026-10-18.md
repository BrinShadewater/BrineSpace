# Project handoff

Updated: 2026-10-18 · Project: BrineSpace · Task: GitHub look-audition update

## Objective and acceptance
Publish the new source audition on GitHub, preserving existing Windows/Mac/iPad integration and the owner's working state.

## Accepted decisions and constraints
F10 is a session-only comparison, starts off, and writes no visual preference. Shift+F10 enables the optional 2 px / 60% pixel grid. Selected preview is 0.5 px tilt shift, focus at 25%, original colours. No export or permanent style acceptance.

## Current state
Branch `codex/look-audition-20261018` is based on integration `585111ca38`. Adds the audition script and native fixture with paired UIDs; attaches it with two lines in screen_atmosphere; adds controls and publication notes, and prepends this milestone to current status. Prepared through a separate Git index so the original main checkout/index and unrelated local work remain untouched. No binary art changes. All broader Windows work was already preserved on `codex/windows-preservation-20261017`; integration baseline retains its existing Mac/iPad reconciliation. Newer Mac/iPad branches have not been merged here.

## Verification
Fresh `python tools/run_tests.py --only test_look_audition --native` and `python tools/run_tests.py --only test_atmosphere_mask_invalidation` pass. All 2,958 real player-profile file hashes remain unchanged. Screen-atmosphere source matches the integration baseline after removing exactly the two audition lines and normalizing newlines. Prior actual-game visual review remains scoped to the October 18 audition, as recorded in its notes. Publication evidence and full logs are retained locally in `output/github-look-audition-20261018/`.

## Next action
Review the source branch and compare with F10. Integrate newer Mac/iPad work separately and perform platform checks before any cross-platform export or release. No platform or performance acceptance is added by this publication.
