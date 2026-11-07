# Darker suits and Bill re-review

## Objective and acceptance
Owner reopened Bill north/south quality: front head slightly small, odd body proportions, funny motion and pale hair reported in south wording; all suits a little too light. Asked asynchronous clarification whether repeated south wording meant north for motion/hair. No answer yet. Earlier acceptance does not override this feedback.

## Accepted decisions and constraints
Darken suits while preserving pose and timing. Bill north/south remain on hold for repair. No new Higgsfield video trial until reference/motion issue is resolved; last verified balance76.

## Current state
`character/crew-darker-suits-v1/` includes 24 staged idle/walk states across Bill, Veld and Branforth, separate from originals/runtime. Fixed 14% maximum darkening in feathered low-chroma body mask; head protected by top27px exclusion, bright metal and chromatic accents protected by mask. `bill-front-proportion-v4/master-input.png` is a built-in image edit candidate requesting a modest head enlargement, slightly reduced upper-arm/thigh bulk, dark brown hair and darker graphite. Not animated or accepted.

## Verification
Three manifests pass, zero errors/warnings. Per-frame assertions confirm unchanged alpha and head pixels and no brightened RGB values. Source hashes unchanged. Inspected before/after colours and six front hair/face samples. Mask is a material approximation, not semantic segmentation; shadowed silver may also darken. Existing motion/proportion defects are deliberately still visible in palette-only preview. New reference is illustrative generated artwork, not an exact pixel-preserving edit.

## Next action
Resolve the north/south motion-and-hair clarification, review Bill reference v4 and dark suit target, then repair Bill's weak motion from selected reference. Do not install held Bill walks or call palette work a gait repair. No Higgsfield credits spent here.
