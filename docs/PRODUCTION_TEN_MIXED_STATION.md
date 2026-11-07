# Fifteen-room mixed station exercise

`tests/playtest_production_ten_station.gd` builds all ten requested room types
around a five-Battery Array connecting row. Every subject faces a valid socket
toward the row. The real economy calculates operation once from controlled
reserves, and the production walker update then runs 20,000 steps of 0.1 seconds
with deterministic seed 77321. No next destination is injected after initial setup.

At 1280x720, 1600x900 and 2560x1440, the walker visits all fifteen rooms and makes
303 transitions, each asserted against production connected-neighbor selection.
All three processes exit zero. `mixed-station-*.err` has no ERROR/SCRIPT ERROR
entries; inherited raw-image export warnings remain. Evidence is in
`output/production-ten/mixed-station-<width>/`, matching logs and station-summary.json.

The 1280 and 2560 start overviews were visually inspected. The entire station fits
at approximately 22% zoom, retains the ten room silhouettes and department finish
differences, and displays the three new draft cards. Fine equipment and indicator
detail is naturally limited at the small overview scale. These are overview
observations, not close doorway or full animation inspection.

The 2,000 seconds are simulated walker time with controlled update calls while
the rest of the game is paused; this is not a real-time performance test or a
2,000-second economy/balance run. One deterministic layout/seed does not prove
all mature station arrangements. Full crossing sequence review, incompatible
pixel boundaries, owner aesthetic review and standalone export remain outstanding.
