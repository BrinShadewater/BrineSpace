# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: North indexed sheets and six-source station

## Objective and acceptance

Reduce remaining measured drone upload bursts without changing selected frames, filtering, dimensions, roots, layers or gameplay. Full PC/Mac release/performance scope remains active.

## Accepted decisions and constraints

Private source/provider/physical fixture only; normal runtime/art unchanged. North startup and wheel sheets use exact RG8 indices/full original coordinates and PNG buffer loading. Six-source wrappers now carry source-specific width/height and fallback byte accounting, not assumptions from larger mining sheets. Original linear/unknown-material fallback retained; no lossy colors/frames/downscales/atlas moves.

## Current state

output/drone-north-indexed-2026-10-06/{start,wheels}/ contains source hashes, exact encodings, PNG sidecars, native probes/logs/results/fingerprints/captures. output/drone-six-indexed-2026-10-06/ holds source-keyed provider with per-source dimensions, physical station, provider/six reports, source-hashes and station-results/verified.json.

## Verification

Both North sheets2688x4480/60nonempty frames; startup22399colors/index+palette24174592bytes, wheels21398colors/24170496bytes versus48168960original each. Full sourceRGBA reconstruction exact. Native360pairs each(720total), all60cells/3scales/2mirrors, everycapture nonblank, zero failures/errors/cleanexit. Startupupload10.968→4.481+.047ms; wheels10.763→4.655+.048ms, isolated pairs/coldwarmuncontrolled/notgameplayacceptance. Source-clock timing/roots not changed. Selected startup frame30 capture inspected; both original/indexed captures retained.

Six-source native provider186checks/120complete South-drone pairs pass, including all six independent/stable identities, actual indexed bytes, dimensions matching actual textures, original fallback size/byte accounting and weak index-image release. Existing West/South complete-drone240pairs and all-cell bodies/effects evidence complementary. Complete North startup material/overlap/controller-join tests not yet established by standalone sheet comparisons.

Matched native40room/12multicell/3Moonbays, idle/pan1/2/4x,60frames/phase/180warmframes, VSyncoff/4070Ti/privatecompressedcrew/debug fixture:all6fullcrew/drone/door/light/power/zoom snapshots equal; no missingart/engineerrors/ordinaryselected duplicates. Allsix indexed paths execute in trace;148palette draws/0fallbacks, eightlogical uploads(total32.743ms including South reloads). Remaining selected cache132597760bytes is active Southbody/effects plusNorthwheels; inactive resources evicted.

p95reference→candidate:1xidle45.428→45.619,1xpan46.535→46.885,2xidle43.720→44.247,2xpan46.181→46.136,4xidle61.084→48.406,4xpan55.592→52.700ms. 4xp99/max idle79.648→54.333,pan71.762→61.618; >50ms frames idle6→2,pan8→9(total14→11). Onepair/no universalFPSgain; all full-frame targets still fail.

Texture endpoints unchanged firstfour phases;4xidle3035.615→2698.873MiB(−336.742), final3036.131→2776.236MiB(−259.895). Actual private scene endpoints, not normal release/peak/endurance or per-source constant claim. Largest captured upload bursts240844800bytes/22.435ms→96337924/8.237ms in different frames; respective overall71.762→59.942ms. Ready12.332/12.191s/no coldwarmacceptance. Every owner2936 non-log fingerprints unchanged; all native processes terminal.

## Next action

Freeze current six-source prototype; verify actual Main title/save/Continue lifecycle and complete surrounding dock/exterior/material composition plus sidecar/source hashes before normal admission. Repeat matched candidate only when it resolves remaining acceptance uncertainty. Shift major profiling attention to regular1x/2x steady frame cost (~44–47ms), which these transition-upload improvements leave unchanged; profile current CPU/render/backend separately with camera/state controls, preserve default quality. Remaining animation uploads/churn, normal texture/loading budget, original bug closure/endurance and actual Windows/Mac certification remain required.
