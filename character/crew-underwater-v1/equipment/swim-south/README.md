# Overhead south helmet — provisional fitting

Generated specifically for the revised prone south camera. Rebuild the 23 x 28
overlay and 18 actor fittings using `fit_south_revision.py`. Source alpha is
preserved through cropping/downsampling and thresholded to binary export alpha;
source and composition hashes are recorded.

Candidate 03 uses magenta keying for both exterior and visor opening. Candidate
01 had an opaque visor; candidate 02 returned a painted RGB checkerboard instead
of alpha and is retained as a rejected source. The builder asserts transparency
at the exported visor center. Contact inspection of all 18 fittings shows face
pixels through the opening and intact reaching hands. Continuous playback and
southbound movement validation remain pending. The fittings are provisionally
integrated and native phase selection passes for every crew member.
