# Locker pickup and deposit animation

Candidate 04 was rejected after visual inspection: although helmet bulk increased,
it introduced bare hands and an excessive overhead lift. The enlarged runtime
endpoint is too low-detail to constrain those features reliably. Use the original
donning source `generated/bill-equip-helmet-east-candidate-05.png` for the next
attempt, with the runtime endpoint retained as the registration target. Preserve
gloves and keep pickup below the head; donning is the separate overhead action.

Bill candidate 02 removes the face-like warm detail from all four held helmets.
It returned RGB with an opaque black background despite the alpha request, so
do not pass it through an alpha-only cropper. Obtain a keyed/transparent source
before packaging; dark exterior keying could eat the character's outline. Source
and cleanup prompt are preserved, and no runtime assets have been replaced.

Production airlock service approaches the west fitting shelf facing east. Current
donning starts with the helmet already held; removal ends holding it. Pickup and
deposit must bridge these endpoints without changing gear before action completion.

Bill pickup candidate 01 supplies six stages: empty-hand idle, reach, grasp, lift,
draw inward and hold. Source and exact prompt are preserved. It is not packaged
or integrated. Inspect registration against the actual donning first frame;
generated endpoint similarity is not an exact match. The source helmet visor has
warm internal detail that needs review so an empty held helmet does not appear
to contain another face. Final pickup should connect to the existing endpoint.

Veld and Branforth need their own identity-specific transitions. Deposit needs
separate timing and a confirmed hand-release endpoint; reversing pickup alone
does not prove correct interaction timing. Update locker action/save interruption
tests when integrating the additional stages.

Latest pickup candidate 05 is packaged in `bill-pickup-helmet-east-v2`. Referencing the original high-resolution donning source restored gloves and the open helmet silhouette. Static contact review still finds a helmet-height jump into the exact reused endpoint. Candidate only; no runtime integration. Source, prompt, registration and endpoint hashes are retained.

A shared adjacent-action playback page is now available at `revisions/locker-review.html`, rebuilt from `build_locker_review.py`. Its 42 source frames are dimension-checked and hashed; Bill's pickup final frame is byte-identical to the first donning frame. Browser loading and terminal playback were verified for all three actors. This is not continuous visual acceptance. The page exposes missing actions, separate clip timings, half/quarter speed, join seeks and terminal holds without an artificial return loop.

Candidate 06 targeted the remaining pickup boundary using both candidate 05 and the original donning source. The generated strip changes the last gloves/helmet placement but retains the candidate body's proportions. Saved as further source evidence; not packaged or selected in the runtime. The source-only appearance is insufficient to prove the exact runtime join corrected.

Pickup coverage now includes six-frame candidates for all three actors. Veld and Branforth are generated from their own existing donning sources; `build_pickup_revision.py --actor veld|branforth` reproduces the new packs. The shared review now checks 54 frames and verifies all three exact pickup/donning boundary images. Veld static registration is close; Branforth still drops the held helmet visibly into the boundary. Bill candidate 06 was packaged as v3 but retains a prop-scale discontinuity, so the review keeps v2. All pickup packs remain provisional; deposit, in-game shelf contact and sequence integration remain outstanding.

Deposit candidates are now available for all three actors at `revisions/{actor}-deposit-helmet-east-v1`, reproduced by `build_deposit_revision.py`. They reuse pickup poses [5,4,3,2,1,0], with independent durations [160,200,200,260,180,160] ms and a release marker at the first empty-handed pose (820 ms). All removal/deposit boundary images match exactly. The review contains 72 verified frames and labels the intended release. Static Veld contact shows a readable extend/release/withdraw sequence, but the held-helmet-to-empty-hand transition must be supported by a persistent locker prop in gameplay. These are derived candidates, not new authored art or completed runtime interactions. Existing pickup shape defects remain inherited.

Current runtime selection: `locker/` manifests compose pickup+donning and removal+deposit, 12 frames each for every actor. The NPC duration reader and renderer now consume the same composed manifests. Equip is 2300 ms; return is 2400 ms. Historical candidate-only statements above describe earlier states. Source packs remain provisional but are now consumed through these compositions. Airlock integration, exact pose timing and medium/cancellation tests pass; see `locker/README.md`. Shelf persistence and continuous visual acceptance are still open.
