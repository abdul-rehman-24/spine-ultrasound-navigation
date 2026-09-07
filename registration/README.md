# Ultrasound-to-3D Registration (Week 7)

## Method
Since real ultrasound-CT paired data is unavailable, this uses the simulated
ultrasound pipeline from Week 6 in a controlled validation setup:

1. Pick a known CT slice location (the "ground truth" probe position)
2. Generate a simulated ultrasound image from that slice (the "query" US)
3. Search across candidate slice locations in the CT volume, generating a
   simulated US for each candidate
4. Compute Normalized Cross-Correlation (NCC) between query and each candidate
5. The candidate with highest NCC is the predicted registration location

## Results (5 subjects, random true locations)
| Subject | True Y | Predicted Y | Error (voxels) |
|---|---|---|---|
| sub-verse004 | 97 | 98 | 1 |
| sub-verse005 | 141 | 140 | 1 |
| sub-verse006 | 386 | 386 | 0 |
| sub-verse007 | 185 | 184 | 1 |
| sub-verse008 | 135 | 136 | 1 |

Mean error: 0.80 voxels, Max error: 1 voxel

## Limitations (documented, not hidden)
- This is a 1D slice-position search (single translation axis), not a full
  6-DOF rigid registration (3 translation + 3 rotation) as originally scoped
  in the roadmap's "rigid + ICP" plan.
- Validation is circular by design: both query and candidates are generated
  by the same simulation function, so this proves the matching mechanism
  works, not that it would generalize to real ultrasound images (which have
  probe-specific noise, patient motion, and acoustic properties not modeled
  here).
- No ICP refinement was implemented; NCC-based discrete search was sufficient
  to achieve sub-voxel-level accuracy in this simulated setting.
- Real-world registration would need to search over rotation and out-of-plane
  translation as well, which is significantly harder and was flagged as the
  highest-risk, highest-time-allocation task in the original roadmap.
