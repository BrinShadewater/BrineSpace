# Northbound clearance correction

Native moving northbound fixture passes and records 78 frames with source-file
hashes in `north-cross-room-route-evidence.json`. Twenty-one sampled frames show
attached helmets and no obvious doorway collision; the initial contact crop cut
the trailing feet in early samples and has been widened without changing source
captures. Full-sequence playback review remains outstanding. The comparison page
now accepts `?direction=north`, explicitly labels Veld's retained runtime cycle,
and passes five controller tests including the mixed pack selection.

Native phase check now passes (`native-north-test.log`) for all six body and
helmet phases across all three crew. Expected files come from the actual selected
source pack: Bill/Branforth revisions and Veld's retained pilot. Dimensions and
pivots are compared per actor rather than forcing one canvas onto all three.
The revision checker covers eleven packs, including exact north helmet foreground
composition and source hashes, with zero failures. Moving northbound visual
capture and full loop inspection remain pending.

Current result: PASS for all three crew (`north-revised-route-test.log`), each
completing the 19-node reverse doorway route. Bill and Branforth now provisionally
load their tighter north revisions and fitted rear helmets; Veld retains her
passing original north cycle. Runtime, main review and clearance export agree.
Native phase selection and moving visual review are still required. The failure
description below is historical evidence from before integration.

The reverse vertical doorway fixture now supports `--cross-room --north`.
Current runtime results: Veld passes a 19-node route; Bill and Branforth fail.
Bill's north-facing destination envelope also fails clearance. Diagnostics use
the actual north-facing sweep, not the east-facing debug probe.

`generated/bill-swim-north-candidate-02.png` introduces a compact bent-elbow
second-pose catch while retaining the original source's body proportions and
other stroke stages. The exact prompt is preserved. This source is not packaged
or integrated yet. Recheck anatomical registration against the current north
source before choosing canvas dimensions: old registration belongs to a
different source hash and must not be reused blindly.

Branforth still needs the corresponding correction. Keep the failed north
fixture active while fitting and integrating revisions; a passing south route
does not prove the opposite-facing silhouette fits.
