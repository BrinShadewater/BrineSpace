# Medical diagnostic and records walls

The Med Center and Med Office front installations and paired inward side variants now use assets/material-polish-medical-v2. Six registrations reference four new PNGs. Exact prompts, previous and current source hashes, and aperture seeds are retained in that directory; previous registration geometry is in output/art-material-medical-v2. Source images are unchanged by the vector registration step.

The medical warm cream/teal identity follows the updated treatment wall. Reflective rims and screen glare are reduced; functional bays remain legible. Some sparse teal wear remains. This is a material improvement, not a claim that all medical art is finished.

Validation: two rooms, 16 rotation/state renders, two sealed offline card bakes, and all 20 side variant checks passed without ERROR output. Native q0/q1 captures of both rooms were visually inspected: paired side silhouettes and full front banks read cleanly against the floor. Other generated rotations remain available for subsequent visual inspection. Both card consumers now select the new cards.

The room-scale review exposes the next mismatch: Med Center's imaging shell and Med Office's pale cabinet tops remain brighter than the repainted walls. Their equipment source atlases remain rooms/underwater/batch-two/med_center-source-v1.png and med_office-source-v1.png. Repaint these next, preserving their UV geometry and the office's warmer upholstery. Med Office captures its medical_hull from the inherited Med Center texture, so review both rooms after the center donor changes. Riser walls and broad lighting/animation acceptance remain separate unfinished work. No executable rebuild.
