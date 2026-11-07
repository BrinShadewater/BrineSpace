# Fresh runs, fires and Water — October 19, 2026

Owner requested more fresh runs and fire/sprinkler demand. Three new fresh-profile
seeds (**9021, 1729, 7013**) reached cycle70 under normal paid offered-card play.
One continued to cycle80 to observe actual heat-driven ignition. Five separately
labelled severe-fire fixtures then used copies of an early paid checkpoint.
No gameplay tuning, supplies, blueprint pools or artwork changed.

## Fresh openings

| Seed | Desalination completed | Galley completed | Water at cycle70 | Lowest Water | Blackouts |
| --- | --- | --- | ---: | ---: | ---: |
| 9021 | 169.7s /cycle8 | 1085.0s /cycle54 | 30 | 4 | 0 |
| 1729 | 170.4s /cycle8 | 466.6s /cycle23 | 30 | 4 | 0 |
| 7013 | 171.4s /cycle8 | Not built by cycle70 | 30 | 4 | 0 |

Times are simulated, with the ordinary 20-second cycle. All three survived, kept
normal costs/failures and had no Galley Water outages. The blueprint entered the
hand at 64.3s /cycle3 in all three; paid construction and harvesting determined
when it finished. The basic Hydroponics Bay and crew do not directly spend Water,
so the third run exercised supply accumulation without a Water-consuming Galley.
Different draft/placement progression delayed the Galleys; do not treat all three
as equal consumer workloads or infer broad difficulty from full storage alone.

In seed1729, the Galley produced a heat warning at cycle61. The diagnostic left it
unrepaired to observe natural ignition at **cycle73**, intensity0.12. Sprinklers
were enabled two simulated seconds later. The fire was out **3.9s after ignition**,
consumed **1 Water**, and never ran dry. Water dipped30→29 and returned to30 by
cycle80; crew and the run survived. No heat/fire was injected in this continuation.
Normal preventive suspension/repair could have avoided that ignition.

## Controlled severe fires

All cases copied seed9021's **cycle9, first paid Water-production checkpoint**:
**6 Water /12 Power /2 Metal**, with the paid Desalination Unit already working.
No supplies, rooms or cards were added. The only hazard injection set listed
compartments to fire intensity1.0. These are stress cases, not measured natural
fire frequency: Mining, Hydroponics, Solar and Desalination do not self-heat in the
current ignition model. Normal suppression, operation shutdown, flooding, crew
escape, repair costs and failure conditions continued throughout.

| Scenario | Sprinkler response | Water spent on suppression | All fires out | Sprinkler interruption | Water after80s |
| --- | ---: | ---: | --- | --- | ---: |
| One severe fire | 2s | 3 | 14.9s | None | 11 |
| Two simultaneous | 2s | 6 | 14.9s | None; reserve reached0 with paid spray remaining | 8 |
| Three simultaneous | 2s | 10 | 47.2s | Water ran out between replenishments | 4 |
| Same three, Desalination suspended | 2s | 6 | Still3 fires at80s | No fresh supply after the reserve emptied | 0 |
| Desalination itself burning | 22s | 3 | 34.9s | No dry spray; one production cycle lost | 9 |

Single/two-fire suppression finished from the initial reserve. In the three-fire
case the reserve reached0 at7.1s; continued 2-Water cycle deliveries eventually
finished suppression. Dry time summed across affected compartments was44.0
room-seconds, versus204.0 with Desalination suspended. These sums are not the
elapsed outage of one room. All extinguished cases logged **suppressed by
sprinklers**; maximum target flooding stayed below the25% flood-extinction threshold.

The burning-plant case deliberately delayed the response past a cycle boundary:
operation correctly read FIRE at20s, with zero Water production, then resumed on
the next funded cycle after extinction. All five runs/crew survived the80-second
observation with zero blackouts. Fire left hull cracks in the affected rooms;
survival and100 Integrity do not mean the compartments need no repair. The suspended
control ended with three severe fires and leaks still active.

## Judgment and scope

The tested unit provides a useful early reserve and can replenish suppression
after a burst. It is not a continuous fire-water guarantee: sprinklers consume
**1 Water per5s per burning room**, while one unit produces **2 per20s cycle**.
Prompt response, stored Water, preventive maintenance and protecting the water
plant still matter. Retain the current 5-Metal /2-Power→2-Water tuning for now;
this evidence does not justify a buff by itself. Higher consumer loads, other
strategies, longer fire sequences and human response times remain unaccepted.

## Evidence

`output/desalination-fire-water-20261019` contains full logs, timelines, copied
checkpoint/meta hashes, process/isolation receipts and independent Water tallies.
All three completed processes exit0 with zero script/engine errors; the fresh
cohort and five-case stress harness report zero harness errors. The initial stress
script had an indentation parse error before any game started; its log is retained,
and only the fixture was repaired. No production source changed.

[Handoff](../output/desalination-fire-water-20261019/HANDOFF.md) and `FINAL.json`
record preservation. All runs used separate scratch APPDATA folders. Existing
owner trials were left alone. No export, signing, upload, cleanup, Git integration
or new platform/performance acceptance.
