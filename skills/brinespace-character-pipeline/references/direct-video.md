# Direct Hailuo crew video workflow

## Current choice and scope

As of September 28, 2026, use MiniMax's direct API for authorized routine Hailuo
crew generations. The owner switched from Higgsfield after a successful live trial.
Keep Higgsfield for separately selected capabilities such as motion transfer;
the saved free Genjutsu run remains reserved until explicitly released by the owner.
Existing authorization covers continuing the requested crew work. A provider
switch does not authorize unrelated animation batches or spending down a balance.

MiniMax-Hailuo-2.3-Fast, 768P, 6 seconds costs an estimated US$0.19 per attempt
under the official pay-as-you-go pricing checked September 28. Previous Higgsfield
settings consumed 4 credits; the owner reported approximately US$1 per credit.
The roughly 95% saving is conditional on those prices. Recheck official rates
before a new budget or settings change; never compare providers' credit counts.
Count failed visual candidates in the attempt budget. Record estimated cost
separately from verified billing. Do not promise a usable animation per generation.

Direct access uses the same model family; it does not fix gait, proportions,
lighting or scale drift by itself. The first direct trial used the same prompt
and approved master as Higgsfield v6 and still shrank. Owner liked the preview
and authorized continuation; it was not installed as a finished replacement.

## Key, submission and recovery

Use `tools/minimax_video.py` from the repository root. The key is read only from
`MINIMAX_API_KEY`; never ask for it in chat or put it in an argument, source file,
preview, screenshot or metadata. A newly set Windows user variable needs a fresh
Codex process. A read-only check proves authentication, not prepaid balance.

```powershell
python tools/minimax_video.py check
python tools/minimax_video.py submit --image character/<new-version>/master-input.png --prompt-file character/<new-version>/prompt.txt --output character/<new-version>
python tools/minimax_video.py poll --output character/<new-version>
```

The submit command currently fixes Fast 2.3 / 6s / 768P / prompt_optimizer=false
and submits exactly one job. Save the exact master and concise prompt first.
It sends the local image as a data URL to api.minimax.io. Ledger creation is
exclusive before POST: repeating the command in that folder fails before billing.
Do not delete a ledger or pick another folder to blindly retry an ambiguous
timeout. Reconcile the task in the provider console first. Poll uses the saved
task ID, makes no new generation, and downloads source.mp4 on success. Keep
polling intervals reasonable (roughly 20-40 seconds while doing independent work).
Never log authorization headers or persist signed download links; CDN downloads
receive no API key. Preserve source, task ID, settings, source hash and cost estimate.

## Review and extraction

Use the selected reference for that direction, not a regenerated identity.
Keep a simple action prompt and change one demonstrated failure at a time.
Bill north trials show the tradeoffs: treadmill wording can produce running,
overly slow/short-step wording can produce shuffling, and ordinary walk wording
can still shrink. No phrase is a guaranteed fix. After repeated similar failures,
compare the accepted source motion or a deliberately chosen motion-transfer path;
do not keep issuing uncontrolled retries just because direct calls are cheaper.

Inspect the whole raw clip before selecting a loop. Compare early/middle/late
head, shoulders, torso and suit tone with the approved reference. Body bounding
box alone changes naturally with steps; use head/torso landmarks to corroborate
scale drift. Inspect alternating contacts, full left/right stride, arm swing,
body sway and seam motion. A still contact sheet cannot certify a natural walk.

Reuse the existing matte extraction builder in a new candidate directory. Current
human bare locomotion profile is 184x184, pivot (92,172), standing reference 148px,
linear sampling. Freeze registration from the reference for the clip. Do not
resize every frame to equal bounding boxes, generate duplicate/interpolated
poses to inflate frame count, or cut away half the stride to hide stutter.
Preserve raw motion and record source indices, full gait cycles and timing.
The initial full-clip review with cycles=0 is not a finished looping manifest.

Apply approved matte treatment exactly once. Existing processed exports may
already contain it. Fixed masked palette/material corrections must preserve
skin, brown hair and department accents; avoid frame-by-frame normalization
that creates brightness flicker. Opposite views with asymmetric gear require
their own references and cannot be blindly mirrored.

Review at approximately 82px, 54px and 27px character heights, plus enlarged
diagnostics. Gameplay scales are more important than detail visible only in a
master. Separate raw-source acceptance, loop acceptance and native installation.
Do not overwrite approved runtime frames until the selected candidate is reviewed.

## Current sources and integration

`character/ACTIVE_ASSETS.json` declares the three bare locomotion overrides:

- `character/crew-runtime-matte-v1/bill/manifest.json`
- `character/crew-runtime-matte-v1/veld/manifest.json`
- `character/crew-runtime-matte-v1/branforth/manifest.json`

These coexist with older action/helmet libraries; counts in historical complete
packs do not prove those states match the revised masters. Marsh is separate.
Historical trials below are provenance, not current selection. At September 29
closeout the accepted bare idle/walk revisions are installed for all three actors;
shared helmet idle/walk is installed for each, and Veld action overrides cover four
directions. Bill east action/matte packs remain staged. Read the current registry,
loader and actor continuation handoff for exact selections; do not resume the older
Bill north trial or Branforth side-gait TODO merely from this reference.

Preserve approved graphite/matte materials, silvers, warm skin and character
head proportions across all views. Bill: brown hair/beard and burgundy accents;
Veld: brown bun, warm light skin and blue accents; Branforth: muted engineering
yellow accents, with his distinct hair/goggles/moustache. Helmet lights are white.
Reference sheets must include palette swatches and helmet-off directional views
as well as helmet-on views. Broader coverage remains an explicit audit task.

When installing, use explicit whole res:// manifest paths, frozen selected frame
hashes and the existing crew validation/native fixtures. Isolate Godot APPDATA
and fingerprint the owner's save before/after. Documentation/source trials do
not require a runtime test, and never imply release-package acceptance.

## Official references

- https://platform.minimax.io/docs/guides/pricing-paygo
- https://platform.minimax.io/docs/api-reference/video-generation-i2v
- https://platform.minimax.io/docs/api-reference/video-generation-query
- https://platform.minimax.io/docs/api-reference/video-generation-download

Live connection evidence: docs/MINIMAX_DIRECT_HANDOFF.md. Workflow updates should
reach both this maintained skill and the installed character-skill copy.

## Explicit first/last endpoint mode — October 2, 2026

For a demonstrated endpoint-join failure, optional `--last-image` uses the official
first/last API with MiniMax-Hailuo-02,6s768P at estimatedUSD0.28; ordinary one-image
submissions retain Fast2.3 and USD0.19. It is an explicit scoped source attempt,
not a blanket model migration. Both images must have identical dimensions and
supported formats; freeze actual runtime source hashes and equal registration.
`python tools/minimax_video.py submit --image <first.png> --last-image <last.png> --prompt-file <prompt.txt> --output <new-candidate>`
Records include both path/hash inputs, never their base64 payload or credentials.
Existing exclusive ledger/no automatic paid retry/poll/download rules remain.
Six offline mocked payload/ledger/error/redaction tests pass in
character/james-west-endpoint-video-v1/test_submission.py. Exact endpoints still
do not prove unchanged anatomy, proportions, material or natural motion between
them; inspect every raw frame before extraction and normal admission.
Official API:https://platform.minimax.io/docs/api-reference/video-generation-fl2v
Pricing:https://platform.minimax.io/docs/guides/pricing-paygo

First/last source conditioning is not motion-path control: James exact-endpoint
job448164031005009 reaches the requested finish yet spins through all cardinals,
lifts feet and invents case marks. All142raw frames inspected; rejected before
extraction/native admission. Keep exact input conditioning and all-frame review
as separate gates. A localized upper-body source trial must retain collar/shoulder
articulation and be reviewed in full-body context, not merely as an isolated head.

James upper first/last job448164885340650 avoids whole-body spin but final crop
still undershoots supplied terminal face angle; inspect actual final pixels, not
only configured input hashes. Picking later frames cannot create missing angular
progression. Grade/alpha edits can remove magenta and white halos yet leave pose
discontinuity or alter identity/patch detail. Preserve transparent generated alpha,
review exact full-body joins and source geometry separately from colour success.
Outgoing-target late edit can repeat final angle and merely move the jump earlier;
do not infer a solved bridge from one endpoint-side pose. Raw/grade/alpha/late trials
and verdicts:character/james-west-upper-video-v1. No normal admission.

James master-family quarter-turn448180480450899 uses new canonical selected-head
South/West carried endpoints, not old endpoint face drift. South59802outside pixels
exact; West60726outside exact; complete source pose reviews closed BEFORE video
hash freeze. Review records themselves can be generation inputs: close them first
or record a fixed snapshot, not a silently mutable pending verdict. Preserve all
original source/geometry hashes and review actual whole-body chronology/terminal
frame; matched input families do not prove a correct generated quarter-turn.
Evidence:character/james-master-cargo-turn-south-west-v2.


James matched endpoint video448180480450899 terminal review:142frames/all six
chronology boards and actual endpoint samples inspected; rejected full spin,
foot lifting and purple backpack. Identity-aligned inputs do not ensure shortest
quarter path. Do not repeat uncontrolled whole-turn jobs after equivalent route
failures; move to explicitly authored intermediate whole-body poses. Final128..141
segment is not accepted without stance/material and exact cardinal join evidence.
Evidence:character/james-master-cargo-turn-south-west-v2/raw-review/review.json.
