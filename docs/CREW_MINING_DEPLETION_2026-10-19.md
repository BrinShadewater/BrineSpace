# Larger crew and mining-depletion tests

October 19, 2026. **Testing complete with findings; no runtime, art or balance values changed.** Local working source remains on main1fb93e50 with existing uncommitted work. The three- and four-person stations sustain their resource budgets after nearby deposits empty. Crew traffic, Marsh's return-to-charge margin and stabilization timing need attention before broad balance acceptance.

## Crew and scenario provenance

Started with the prior paid seed1729 two-person checkpoint: Bill and Veld, established Hydroponics/Galley/Desalination/Life Support,39 Metal,28 Food,28 Oxygen and30 Water. Added a paid Crew Hab and Solar Array, constructed access routes, paid8 Metal per ward and had crew physically repair the existing sites. Branforth joined at407.1 simulated seconds from that checkpoint. A later three-person checkpoint is the common starting point for the fourth-person expansion trials.

The narrow route stalled before Marsh. A separate route using paid Tee Corridors completed the remaining ward and recovered Marsh at492.1s from the three-person checkpoint. All four current named characters are present. Marsh eats but does not breathe, so four crew have three Oxygen consumers. Crew Hab adds berths, not supplied population.

**Construction cards were explicitly supplied.** Resources, room costs, construction travel/work, ward welding, discovery, upkeep, hazards, power and failure rules remain normal. This tests infrastructure and resource budgets, not blueprint availability or blind human exploration. The source profile already has stabilized **Breathable Quarters**, which improves its Oxygen budget; do not transfer these margins to a profile without it.

## Natural depletion of surveyed deposits

Held each station without further expansion, with sprinklers armed and normal paid post-fire repairs. No deposit stock edited in these runs. Observe both bays exhausting their surveyed stocks, then another360 simulated seconds.

| Cohort | Mining/salvage loads extracted during this observation | Both surveyed stocks empty after | Further observation | Minimum Food / Oxygen / Water / Power | Final Metal |
|---|---:|---:|---:|---:|---:|
| Three named crew | 23 /16 | 766.2s | 360s | 27 /27 /29 /10 | 40 |
| Four named crew | 5 /0 | 154.1s | 360s | 26 /27 /30 /9 | 40 |

Both runs remain active with all recovered characters alive,100 Integrity and **zero blackout cycles**. Final Food/Oxygen/Water:27/27/30 for three crew;26/27/30 for four. The four-person checkpoint begins later with only five surveyed mining loads left and no surveyed salvage stock; these are sequential observations, **not matched timing comparisons or evidence that crew size changes extraction speed**.

Both end with **120 mining loads and150 salvage loads still outside the surveyed area**. Mining/salvage bays correctly report depleted surveyed stocks; expansion can still uncover more. Food, Oxygen and Water production do not require continuing mining. These holds retain Metal reserves; the separate spending test below examines the zero-Metal condition.

## Whole-map-empty controlled cases

Four forks of the actual four-person checkpoint explicitly set remaining deposit units/progress to zero in scratch data. This removes125 mining and150 salvage loads; it is **not a claim of naturally extracting the entire map**. Existing cargo may return normally. No resources or crew are granted. Every final checkpoint independently validates with all site stocks zero and four living named crew.

| Controlled case | Observed result |
|---|---|
| Keep the reserve | After420s, still40 Metal,26 Food,27 Oxygen,30 Water; no emergency Metal or passive Metal income. |
| Spend down through conversion | Pay for a Salvage Workshop, convert earned Metal to Rare Minerals, suspend at shortage and spend the last2 Metal on a Corridor. Reserve reaches0. BRINE awards two1-Metal reclamations, reaching2 Metal67.4s later. A subsequent paid Corridor completes; the next reclamation leaves1 Metal. |
| Add an Ore Refinery | Pay8 Metal +1 Power to build. Over20 measured cycles, produces **1 Metal/cycle with every deposit empty**, ending at52 Metal. Its added storage permits that reserve. The source profile did not own this blueprint; it was supplied for this isolated functional test, so availability/purchase is separate. |
| Discover Logistics Spine | Pay2 Metal for a new straight Corridor and6 for connected Storage. One functioning recipe link generates **1 Metal/cycle, then2 after stabilization in this same run**. Reserve ends70 Metal; the setup also receives its normal1-Metal discovery pulse. |

All four have zero blackout cycles and keep their Food/Oxygen/Water budgets. BRINE's fallback is small:1 Metal every three cycles only below2 Metal without an open harvest route. It funds a cheap passage in this case, not unrestricted rebuilding or an assurance that the necessary card is in a real hand. The conversion case deliberately overcommits its reserve; it is a controlled stress choice, not a recommended strategy.

**Mining is finite; Metal is not currently finite.** Refineries and recipe output can keep supplying it after deposits are empty. Do not diagnose all-map depletion as an unavoidable economic end solely from exhausted bay targets.

## Findings requiring follow-up

### Narrow-route construction traffic

Repeated headless expansion attempts leave Bill assigned to the paid Corridor at **(26,17)** while three crew cluster near the narrow Corner Corridor at **(24,20)**. The order has no construction progress despite healthy resources. A saved-state **native rendered replay remains stalled for another180.1s** with all three crew alive. The assigned builder keeps retrying the approach; no automatic reassignment resolves this observed case.

The alternative paid Tee Corridor route reaches Marsh successfully. This is a useful layout workaround, **not a fix for the reproduced traffic stall**. Preserve both cases when working on passage clearance and build-order recovery. The source files were inspected but not modified.

### Marsh's return reserve on long routes

The four-person natural-depletion tail ends with Marsh alive at0% battery, still making an emergency return. Other controlled tails also show low-battery/route warnings despite healthy station Power. A separate native continuation from the actual post-depletion checkpoint reaches the charging pod and recharges from0% to **90% by180.1s**, spending normal stored Power. He is docked and charging at the end, so this is not a permanently disconnected charger or a proven charging failure.

Long travel/traffic can consume his35% return reserve; at zero he returns at quarter speed. Route-aware return margins and passage handling are more useful next investigations than increasing station Power output. Four living crew is not the same as four continuously productive crew; no full-duty/endurance acceptance is claimed.

### Stabilization timing differs from written direction

The new Logistics Spine is discovered at cycle149, stabilizes at151, and the same run's Metal rate rises from1 to2 at152. Source profile had only Breathable Quarters stabilized; there is exactly one active Metal recipe link, so this is not two stacked links. AGENTS describes doubling in later loops. Record the current behavior and reconcile it with that direction before changing progression. **No rule was changed in this testing pass.**

## Verification and preservation

- Natural three-/four-crew holds, successful wide-route recovery, corrected Logistics Spine case and native traffic/Marsh observations finish with clean process exits and no script/engine errors. The native traffic observation intentionally records an unresolved stalled order.
- The initial combined depletion batch completed its first three independent cases, then failed to set up Logistics Spine because every existing straight passage had both ends occupied. Added a normally paid Corridor and reran **only that fourth case**. Seven source/final checkpoints were independently read and validated against recorded resources, crew and stocks. Original batch/error logs remain; it is not reported as a clean overall batch.
- Early failed traffic runs and one shutdown-only harness audio error remain separately archived. Cleanup ordering was corrected in output-only helpers. No production audio or routing fix is claimed.
- Fresh focused tests **test_finite_harvest** and **test_metal_trickle** both pass. Full logs and independently recomputed results are retained.
- Scratch APPDATA for every invocation; **all2,971 real profile files,27 protected source/art hashes, original checkpoint/meta inputs and signed Windows ZIP size/mtime unchanged**. Existing private previews retained. No export, signing, upload, commit, merge or cleanup.

Evidence: [review summary](../output/crew-depletion-20261019/review-summary.json), [final receipt](../output/crew-depletion-20261019/FINAL.json), [handoff](../output/crew-depletion-20261019/HANDOFF.md). Source profiles, directed routes and supplied cards limit generality. Deterministic0.1s steps and bounded native follow-ups do not establish human pacing, packaged performance, leak/headroom or other-platform acceptance.
