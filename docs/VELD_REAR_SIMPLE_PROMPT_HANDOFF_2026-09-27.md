# Veld simple rear prompt test

## Objective and acceptance
Owner requested simplifying the rear-walk prompt after hopping failures.

## Accepted decisions and constraints
One 4-credit Hailuo 2.3 Fast test using same rear reference, short natural treadmill-walk description and identity preservation. No new reference or model. Accepted side walks unchanged.

## Current state
character/veld-video-north-v4 contains exact prompt/job, original input, raw source.mp4, full-clip.gif, contact sheet and diagnostic extraction outputs. 141 frames at 24fps/768px. Marked held_gait_still_suspect, not installed.

## Verification
Source decoded and sampled poses reviewed. Both feet still appear to move together with pronounced vertical bobbing; short prompt alone has not established credible northward walking. Generated diagnostic loop is not acceptance. Do not use its seam score to override visual findings.

## Next action
Show original test for owner comparison. If rejected, use a verified rear-walk motion reference or controlled rig instead of further blind text-only Hailuo retries. No further generation submitted.
