# Balance pass: paid recovery and crew growth

October 19, 2026. Local working source on main `1fb93e508f782e5109385e5fa9de12ea743e4cd9`, including the existing uncommitted Desalination, opening-draft and look work. **No gameplay values, runtime code or art changed in this pass.** The tested economy provides both pressure and recovery; these cases do not justify a general buff or difficulty increase.

## Paid recovery after early fires

Four cases copy seed9021's actual paid seven-room checkpoint at cycle9: 2 Metal, 6 Water, 12 stored Power. Each deliberately inserts a maximum-intensity compartment fire, enables normal sprinklers after2s (22s for the plant case), then requests ordinary full hull repairs two seconds after all fires are out. No supplied resources, rooms, crew, free building or disabled failures. Mining deliveries and actual crew travel/welding remain active. Observe240 simulated seconds per case.

| Controlled case | Fire out | All target hulls sealed | Repair Metal | Lowest Metal | Final Metal / Water |
|---|---:|---:|---:|---:|---:|
| Mining bay | 14.9s | 41.5s | 2 | 2 | 20 /27 |
| Mining +Hydroponics | 14.9s | 59.4s | 4 | 0 | 18 /24 |
| Mining +Hydroponics +Solar | 47.2s | 102.2s | 6 | 0 | 14 /20 |
| Desalination, delayed sprinkler response | 34.9s | 73.6s | 2 | 2 | 20 /25 |

All four survive with Bill alive, all target cracks repaired, target flood levels zero, no remaining fires, no blackout cycles and valid final checkpoints. The three-fire case still has44 dry sprinkler-room seconds between Water deliveries. A zero reserve is recoverable here because the existing finite mining route resumes income; this does not prove recovery after deposit exhaustion or blocked routes. Simultaneous repair orders reserve their costs, then one crew member completes the work sequentially.

Retain **2 Metal for a hairline full weld** and **Desalination5 Metal /2 Power →2 Water per cycle**. Repairing three compartments still consumes the available Metal; Water production does not remove the need for a reserve. These controlled fires are not a measurement of natural fire frequency, and some target rooms do not naturally self-heat.

## Actual named-crew recovery and Oxygen response

Two further cases copy seed1729's paid cycle70 checkpoint, already containing Hydroponics, Galley, Desalination and established power/harvesting. Starting reserve: 40 Metal, 30 Water, 29 Food, 8 Oxygen and12 Power. Each builds a2-Metal Corner Corridor and2-Metal Corridor to the existing ward, pays **8 Metal** for its repair, has crew physically weld it, and lets Dr. Veld thaw normally. Core berths accommodate Bill and Veld; Crew Hab does not manufacture population.

**Construction blueprints are explicitly supplied in these two controlled scenarios.** Costs, construction travel, crew welding, power, room operation, finite resources, natural hazards and failure rules remain normal. This isolates recovery cost and response time; it does not test when those blueprints appear in an actual hand.

| Case | Life Support order | Veld awake | Minimum Oxygen | Final Oxygen | Minimum Food / Water |
|---|---:|---:|---:|---:|---:|
| Build support before recovery | 0s | 147.1s | 8 | 28 | 28 /30 |
| Respond when Oxygen reaches4 | 180s | 107.1s | 3 | 17 | 28 /30 |

Both continue240 simulated seconds after Veld wakes, finish with two living named crew, zero blackout cycles and valid checkpoints. The prepared case adds Life Support before the access route; the reactive case awakens Veld sooner, then pays for Life Support after the Oxygen reserve starts falling. Retain the current Life Support build cost5 Metal +1 Power and1 Power/cycle operating cost: preparation matters, and the tested late response still has room to complete construction. A blocked route, unavailable card, smaller reserve or longer travel could change that result.

Both copies inherit the Galley's natural cycle73 ignition and deliberately leave it unattended. Floodwater extinguishes it at cycle80 and a wading warning is logged. They are **not sprinkler recovery cases** and their full Water reserve does not exercise sustained Water demand. Food resilience here depends on already-built Hydroponics, Galley and stored provisions; it is not a claim about a fresh two-crew opening.

## Opening draft and water-room roles

Reviewed the existing three-seed cycle70 opening receipts without rerunning them. The restricted policy discards non-priority cards, caps most foundation rooms at one copy, and uses19 rerolls in each run. Galley construction at cycles54/23/not built is therefore not sufficient evidence for changing its rarity or staging. Hydroponics already supports one crew without Water input. Keep the existing early foundation sequence and reroll recovery for now; broader expansion with actual offered cards remains useful follow-up.

Tidal Condenser retains an indoor operating niche with no ocean-intake requirement, plus its existing Nutrient Mist, Chilled Cells and Condensate Loop recipes. Desalination trades those placement/discovery benefits for a cheaper common foundation with an exposed intake. Neither room's output or cost changed. Existing hidden recipes and progression rules remain intact.

## Verification and limits

- Final recovery and growth processes both exit0 with zero script/engine errors and zero harness errors: **six completed scenarios**. Independent review reconciles repair costs, Water arithmetic, actual crew count, checkpoint writes and outcomes.
- Every Godot invocation used scratch APPDATA. All **2,971 real profile files**, **19 protected source/art hashes**, **four checkpoint/meta inputs**, and signed Windows ZIP size/mtime match. Existing playable previews remain open; no export, signing, upload, Git integration or release change.
- Two fixture API mistakes during inventory/growth preparation were corrected in output-only helpers. Failed logs remain separate; final clean runs govern the reported results.
- Headless deterministic0.1s manual game steps, normal20s cycles. One early station and one established station reused across controlled cases; two crew only. No human-pacing, visual, large-station, three-plus-crew, release-performance or platform acceptance.

Evidence: [handoff](../output/balance-recovery-20261019/HANDOFF.md), [independent review](../output/balance-recovery-20261019/review-summary.json), [final receipt](../output/balance-recovery-20261019/FINAL.json). Next useful scope: varied fresh-run expansion with actual offered cards, further named-crew recovery, finite-deposit depletion and maintenance at larger station sizes.
