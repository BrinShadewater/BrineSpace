# Floor decoration placement review

Reviewed native furnished captures for all 44 non-corridor rooms and checked automatic details across four rotations. Initial checks found 320 host-adjacent placements with no missing hosts or hidden pieces. Visual review found redundant automatic standing mats beside workstations that already have authored pads.

The resolver now omits the redundant automatic mat when its host already has an authored pad. Explicit saved placement overrides are retained. The final default layout resolves 306 details, all passing host/bounds/protected-route/spacing and native visibility checks. The corrected Current Turbine capture was inspected at native size. This is a check of default automatic placements; it does not certify arbitrary player-moved decorations or baked decoration pixels. Corridors are outside this host-based decoration system.

The audit fixture now handles newer rooms with empty detail lists and asserts no duplicate automatic workstation pad. Evidence: output/floor-decoration-pass, including initial review sheets and final individual captures. The current Godot checkout contains the correction; the Windows package predates it.
