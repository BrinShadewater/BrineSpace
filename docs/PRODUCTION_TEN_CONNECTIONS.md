# Ten-room connection geometry evidence

`tests/test_production_ten_connections.gd` loads the current manifest and actual
registered views, then compares their sockets with RoomDatabase layouts for all
four rotations. It checks all 6,400 ordered room/rotation/side pairings:
2,916 compatible boundaries and 294,516 center-to-center route samples pass.
Every incompatible boundary blocks its midpoint; disconnected embedded views
have no open sides. Exit status is zero, with zero reported failures.

Evidence: `output/production-ten/connections.log` and `.err`. Inherited raw-image
export warnings remain. This test uses actual registered footprints and shared
geometry but does not render pixels, drive production walkers, or simulate power.
It strengthens the geometric neighbor evidence for all ten rooms; it does not
certify seam appearance, actor crossing, economy states, packaging or owner review.
