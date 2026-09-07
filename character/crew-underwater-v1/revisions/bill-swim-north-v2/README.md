# Bill north compact catch — candidate

Six frames packaged from the preserved candidate-02 source. Rebuild with
`python character/crew-underwater-v1/build_south_revision.py --actor bill --direction north`.
The shared vertical-swim exporter now accepts north explicitly and rejects actors
whose north measurements are not yet supplied.

Canvas 104 x 112, shoulder pivot (52,36), source scale 0.2 and manually measured
shoulder centers. Contact inspection shows distinct compact catch/pull phases,
intact hands and feet, and stable torso placement. This scale matches the south
source calibration but still needs cross-direction anatomical comparison; do not
treat the canvas or a routing pass as proof of consistent character size.

Six rear-helmet fittings are now packaged with `fit_north_revision.py`, including
recorded foreground hand regions during reach/catch. The north/south contact
comparison shows broadly comparable body lengths with remaining head-projection
differences; native turning review is still required.

No runtime integration yet. Northbound fixture currently fails
on the old Bill and Branforth clips. Preserve that regression until the replacement
is fitted, integrated and verified at the intended body scale.

Current status: provisionally integrated with helmet fitting. All three crew
pass the 19-node northbound furnished route after this update. Native frame
selection, moving capture and continuous loop review remain outstanding.
