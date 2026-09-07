# Pedicle Identification & Trajectory Planning (Week 5)

## Method
1. Load per-vertebra ground-truth masks from VerSe dataset (labels 16-24 for sample subject)
2. For each vertebra, extract voxel coordinates and compute:
   - Centroid (mean position)
   - Spread along each axis (z = superior-inferior, y/x = medial-lateral / anterior-posterior)
3. Identify the medial-lateral axis as the larger-spread axis among y/x (excluding z)
4. Estimate left/right pedicle centers as offset points along this axis (0.3x the spread from centroid)
5. Validated axis choice by overlaying points on a 2D axial slice — confirmed points land
   within the left/right vertebral fragments as expected

## Sample Result (sub-verse004)
- 9 vertebrae processed (labels 16-24)
- Pedicle estimates saved to results/metrics/week5_pedicle_estimates_sub-verse004.csv

## Limitations (documented, not hidden)
- This is a geometric heuristic (centroid + axis offset), not a trained pedicle detector.
- Uses ground-truth per-vertebra masks (not the model's binary prediction from Week 3/4),
  since automatic per-vertebra separation from a binary mask is out of scope for this MVP.
- Left/right pedicle offset ratio (0.3x spread) is a fixed heuristic, not anatomically
  calibrated — works reasonably for typical vertebra shapes but may be off for atypical
  anatomy (as flagged as a risk in the original project roadmap for Week 5).
- Trajectory planning (actual screw insertion path/angle) is not yet implemented —
  this covers pedicle center identification only.
