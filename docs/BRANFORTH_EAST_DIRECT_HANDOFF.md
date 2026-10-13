# Project handoff

Updated: September 28, 2026 · BrineSpace · Branforth side walk

## Objective and acceptance
Owner asked to move on after Bill muted south/new east. Saved Bill selections in character/bill-muted-east-south-v1/selection.json, with loop cuts and installation explicitly unfinished. Continued the previously identified Branforth side-gait/head issue with one direct east take.

## Accepted decisions and constraints
Use the owner-preferred larger-head reference from crew-side-proportions-v2/branforth-east-source.png. Preserve grey hair, moustache, goggles, muted yellow engineering accents and attached wrench. Opposite equipment-bearing views are not mirrored. Higgsfield credits and saved free run remain untouched.

## Current state
character/branforth-east-direct-v1 contains the copied reference, exact prompt, task 446797517254987, original video and 141 matte frames. Default direct Fast 2.3 / 768P / 6s; estimated US$0.19 this turn, eight direct attempts estimated US$1.52 total (actual billing unverified).

Build retains fixed reference scale, 184-square canvas and (92,172) pivot. Existing Branforth source neutral gain (69/75,66/69,64/71) precedes the approved matte curve. A fixed post-matte body-only gain (0.90,0.93,0.98) matches the initially warmer/brighter generated fabric toward installed graphite; palette_match.py feathers below the head and excludes chromatic yellow accents and bright hardware. No per-frame histogram normalization or geometry edits.

compare.py renders new full take beside installed east, south and north at 148/82/54/27px reference heights. Candidate only: no chosen loop or game changes.

## Verification
Generation/download succeeded. Initial extraction: 141 frames at 24fps, first/last height 148/147px, full range 143-148px, no clipping. Sampled 24 poses inspected for identity/scale; full temporal gait acceptance is not claimed. Initial neutral medians (65,60,58)-(69,65,61) were warmer/brighter than installed east median (60,57,59), prompting the single fixed body correction; final values are recorded in validation.json. Source and head geometry are preserved.

## Next action
Review http://127.0.0.1:8791/character/branforth-east-direct-v1/ for gait and head/suit match. If selected, cut a complete alternating stride and inspect the seam before native installation. West remains separate. Bill selected east/south need full loop cuts and north loop review before their later install. No further generation retries submitted.

## Straight-profile retry

Owner rejected direct v1 because "His walk isnt straight". New direct v2 uses the same larger-head master and deterministic palette treatment, with a stricter prompt for right-facing profile throughout, aligned shoulders/hips/feet and no turning or sideways sway. One new generation: task 446798052852217, estimated US$0.19 (direct session total US$1.71, actual billing unverified). Previous take is preserved with owner-feedback.json. Preview compares previous/new east and installed south/north. No runtime edits or automatic additional retries.

V2 checks: 141 frames at 24fps, first/last height 148/144px, range 142-148px, no clipping. Neutral medians (60,57,56)-(64,61,60). Inspected sampled full-clip poses; stricter profile is the generation instruction, not a claim of verified gait/alignment. Owner motion review pending at character/branforth-east-direct-v2; runtime unchanged.


## Matched gloves and corrected reference (v4)
Owner liked v2 overall but reported a black far glove and slight rightward curvature. Edited the reference with built-in imagegen to stricter side profile and matching graphite gloves; reference prompt/provenance are in character/branforth-east-direct-v3. V3 task 446800362090826 produced idle-like stationary feet and is rejected in rejection.json. V4 task 446800685777278 uses the same corrected reference with a simpler continuous alternating-walk prompt.

V4 is a source candidate, not installed or loop-cut. 141 frames at 24fps; fixed scale/offset, first/last height 147/145px, range 142-148px, no clipping. Sampled poses show alternating steps and more consistent profile. Exposed far glove retains graphite detail but remains darker in shadow; motion acceptance is pending owner review. Neutral medians range (60,56,58)-(64,60,63). Preview compares v2 and v4 at 148/82/54/27px and installed south/north. hands-review.png records six hand crops.

Changed files: new v3/v4 candidate folders, v2 owner feedback, this handoff and CURRENT_STATUS. Two direct attempts for this correction estimated US$0.38; direct session total US$2.09, billing unverified. Built-in reference image edit cost is separate/unknown. Higgsfield untouched. Remaining: owner gait/alignment review, full-stride loop extraction and seam review, then isolated native installation checks; Bill selected candidates remain uninstalled.


## Accepted source and loop candidate
Owner approved v4: "Okay, looks good, lets keep going". Recorded selection.json. New character/branforth-east-loop-v1 copies frames 67-118 exactly with hashes, 52 poses / one alternating stride, 2167ms preserving source timing. Every pose inspected for alternating limb phases. Validation: zero clipping, height 142-148px; seam foreground MSE .003353 vs median internal .024894 and max .035857. Metrics do not certify temporal acceptance. Comparison includes installed directions at original timing and full approved source; loop playback review pending. Runtime unchanged, no generation spend. Next: accept loop seam/gait before installation and preserve asymmetric west equipment.


## Installed and verified
Owner continued after loop preview. Installed 52 hash-identical east frames under character/crew-runtime-matte-v1/branforth/frames/walk-east-direct-v4 and replaced only walk-east in the existing manifest (stride retained). Other states compared equal; original manifest and prior frame files preserved. Candidate installation.json records validation. tests/test_crew_walk_v2.gd now explicitly expects 2167ms for this accepted clip and checks half-stride phase relative to cycle duration; motion remains distance-driven. 2061 checks, zero failures. Native preview_crew_layout_studio verify passed with three moving actors and unchanged draft; rendered research-lab screenshot inspected and saved to candidate installed-studio.png. APPDATA isolated with copied owner layouts; before/after real-profile hashes equal. Logs in output/branforth-east-install-v1. No generation spend. Next: independent Branforth west consistency; Bill selected east/south and north cut remain pending installation.
