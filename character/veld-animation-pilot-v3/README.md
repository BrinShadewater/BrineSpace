# Veld pilot v3

Continues v2 with a targeted source edit lowering the two passing knees, and a
deterministic colour pass using the selected v4 skin, blue and graphite ramps.
The walk stays six frames / 900ms. Stationary source-size corrections are retained.

Rebuild with `python character/veld-animation-pilot-v3/build_pilot.py`, then
`python character/veld-animation-pilot-v3/build_review.py` from the project root.
Run `verify_materials.py` for alpha, geometry, luminance and anchor checks.

`materials.py` uses bounded colour/position masks and connected components to
separate warm face pixels from the hair crown. It interpolates along the exact
authored ramp anchors at each pixel's existing luminance. Intermediate shades
remain continuous; this is not flat 24-colour quantization. Dark neutral material
selection can include glove or steel shadow pixels, so it is not a complete hand
segmentation of all materials. Review the saved masks along with the artwork.

The comparison uses v2 on the left and v3 on the right. Sources, source hashes,
prompt and mask diagnostics are saved. Colour validation passes 18 cropped-frame
transforms; sprite validation passes all 18 exports. These checks do not establish
native foot contact, exact whole-character palette compliance or owner acceptance.

Pending: native travel/heel contact and full material audit (especially hair,
ivory and steel), followed by direction/helmet coverage. No runtime art changed.
