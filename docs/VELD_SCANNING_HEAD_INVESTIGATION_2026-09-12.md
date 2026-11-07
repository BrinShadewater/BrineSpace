# Veld scanning head investigation

Updated: September 12, 2026 · BrineSpace · Owner F8 report investigation

## Objective and acceptance
Investigate “Velds head disappeared while scanning” in manual report `brinespace-report-20260912-230218-47804-1122037346.zip`. Diagnosis only; no fix or reproduction claimed.

## Accepted decisions and constraints
Preserve current character art, room layouts and player saves. Use the report evidence and current source. Do not redesign rooms or replace intact art on suspicion.

## Current state
Evidence copied into `output/veld-scanning-bug/`. Report screenshot already shows Veld walking south with her head visible. Saved state confirms bareheaded, dry, walk-south, looking for food, at (8252.466, 8264.628), visual time 189.587445. The snapshot occurs after the reported scanning glitch.

Selected bare scanning and sample-examination frames were inspected in all four directions (48 frames); heads are present. Source hashes are preserved in `source-hashes.json` and the source review in `scan-frames.png`.

## Verification
Continued the copied station with explicitly advanced NPC simulation and collected eight later scanner stops across Life Support, Current Turbine, Solar and BRINE. Native room rendering at those exact positions, with current local overrides, sampled scanner frames 0/2/4. All eight show Veld's head. Final component captures: `point-00-2.png` through `point-07-2.png`, with `points-final.log`. These samples cover room-local depth drawing, not the complete original station/neighbor-wall composite or the unknown prior moment.

Initial diagnostic attempts are retained as superseded evidence: full-station captures did not follow the intended camera target; a diagnostic call requested an absent interact action-clearance key and was invalid. Neither is a production regression. The final room-component pass has no script errors.

The original report log also contains 492 assertions for two missing Solar floor-dressing hosts, `thermal_pumps` and `thermal_service_table`, through the construction-art renderer. No connection to Veld's missing head has been established; retain as a separate concrete diagnostic finding.

No production files changed. Missing source pixels were not found, and prop/wall occlusion remains an unconfirmed possibility rather than a diagnosis.

## Next action
If it recurs, pause while the head is absent and press F8 so the screenshot and live state retain the offending pose/location. Use that state to test full-station depth/caching against direct rendering. Current report alone does not establish a safe corrective change.
