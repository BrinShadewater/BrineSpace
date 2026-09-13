# Isolation Vault owner asset repair

Updated September 12, 2026. The unclear “Full Insolation Wall” was identified as
the north-only baked `isolation-u-flush-clean-v1.png` perimeter, separate from the
registered `emergency-isolation-wall`. The baked perimeter is no longer loaded.
The live emergency wall now uses the accepted south overhead bank in every
direction through exact quarter turns. The sealed chamber, release catches and
supply access face the room interior from each wall.

The vault also inherited its room implementation from Battery Array. That brought
in two battery banks, a breaker, distribution cabinet, test bench and cable reel;
they were reuse artifacts rather than isolation equipment. The vault now clears
that inherited furnishing layer and retains only the Emergency Isolation bank.
The floor-profile machinery record was updated so removed flush pieces are no
longer reported as live hosts.

The Battery Array test-bench source received a separate matte pass at
`rooms/production-ten/decor/battery-test-bench-matte-v1.png`. It compresses bright
steel and burnt-orange highlights while preserving the original alpha and geometry.
The current full-wall Battery Array layouts can displace this supplemental bench,
but its maintained composition binding and provenance now point to the matte source.

Native Isolation Vault q0-q3 evidence is in
`output/isolation-owner-repair-2026-09-12/candidate-native`; the Battery Array
placement review is in the sibling `battery-matte-native` directory. Directional
hashes and the exact removal list are in `assets/isolation-directional-v2`. The
reviewed q0 vault capture is the live catalog card. No power behavior or character
animation changed.
