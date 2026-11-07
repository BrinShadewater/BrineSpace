# Bill pickup — endpoint comparison candidate

Five generated pickup poses plus the exact existing donning start frame are
packaged by `build_pickup_revision.py`. The generated sixth pose was edge-cropped
and is deliberately excluded. Source, measured feet, scale and endpoint hashes
are recorded. Canvas/pivot match donning: 92 x 104, (46,98).

Contact review exposes a visible style/proportion jump into the existing endpoint:
the generated body is slimmer and its held helmet smaller. Matching standing
height alone does not solve this. These frames are not runtime-ready; revise the
pickup source against a larger endpoint reference before integrating. Do not
claim a seamless join merely because the final frame bytes match donning.
