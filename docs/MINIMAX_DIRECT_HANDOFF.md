# Project handoff

Continuation: [adopted workflow and second trial](CREW_DIRECT_WORKFLOW_2026-09-28.md). The owner liked v1 and authorized the next iteration; evidence below describes the first connection trial.

Updated: September 28, 2026 · BrineSpace · Direct MiniMax video generation

## Objective and acceptance
Replace expensive routine Higgsfield Hailuo calls with the same model through MiniMax directly. Prove authentication and a single 6s/768p comparison; retain the existing extraction workflow. Generation success is not gait acceptance.

## Accepted decisions and constraints
Owner supplied MINIMAX_API_KEY through the Windows user environment after discussing a $0.19 comparison. Never put the key in scripts, logs or source control. Preserve Higgsfield balance and reserved Genjutsu run. No batch retries or runtime replacements in this trial.

## Current state
`tools/minimax_video.py` supports read-only `check`, single paid `submit`, and resumable one-shot `poll`/download. Uses the official api.minimax.io endpoint, Fast 2.3, 6s, 768P, optimizer off. Submission ledger is created exclusively before POST to prevent accidental duplicate billing; ambiguous failures require reconciliation, not retry. Key and base64 image are never saved in metadata; downloads do not receive the authorization header.

Trial: `character/bill-north-direct-v1`, task 446786521227807. Same approved larger-head master and prompt as Higgsfield north v6, so vendor route is the intentional change. Published estimated price US$0.19; actual billing not independently verified. Existing runtime remains unchanged.

## Verification
Read-only authenticated API check returned HTTP 200 / status 0. Live video submission returned task ID. Python syntax check passed. Repeat submission to the same output directory was refused with FileExistsError before a network call. Generation completed and downloaded. Existing builder extracted 141 frames at 24fps with no clipping. Contact sheet inspected: size drift persists (processed height 148px first frame, 128px last frame). No selected cycle or runtime installation; full motion acceptance remains pending.

## Next action
Review http://127.0.0.1:8791/character/bill-north-direct-v1/ for the direct clip beside Higgsfield v6 and the full processed clip. Connection is proven; gait/scale still need work. No automatic acceptance or further paid calls.

## References
- https://platform.minimax.io/docs/api-reference/video-generation-i2v
- https://platform.minimax.io/docs/api-reference/video-generation-query
- https://platform.minimax.io/docs/api-reference/video-generation-download
- https://platform.minimax.io/docs/guides/pricing-paygo
