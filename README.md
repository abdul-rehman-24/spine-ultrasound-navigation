# Computer Vision Methods for Surgical Navigation in Spine Surgery

A research and educational MVP prototype of an ultrasound-based spine
surgical navigation system for pedicle screw placement — covering the full
pipeline from raw CT input to an interactive 3D navigation application.

> **⚠️ Research/educational prototype only. NOT validated for clinical use.**

---

## Overview

This project implements and connects nine stages of a spine navigation
pipeline, using the public [VerSe19](https://github.com/anjany/verse) CT
dataset as its data source:
CT Volume (VerSe19)
|
v
Preprocessing -> resample to isotropic 1mm spacing, HU normalization
|
v
3D U-Net Segmentation -> binary spine mask (Test Dice: 0.8297)
|
v
3D Mesh Reconstruction -> marching cubes + noise cleanup
|
v
Pedicle Center Estimation -> geometric centroid + medial-lateral offset
|
v
Simulated Ultrasound -> 2D ray-casting B-mode simulation from CT
|
v
US-to-CT Registration -> NCC-based slice localization (mean error: 0.80 voxels)
|
v
Instrument Detection -> Hough Transform needle detection (mean angle error: 0.82 deg)
|
v
Navigation App -> PyQt6 + PyVista interactive 3D viewer


## Results at a glance

| Stage | Metric | Result |
|---|---|---|
| Segmentation (3D U-Net) | Test Dice score | **0.8297** |
| Segmentation | Validation Dice (100 epochs) | 0.7285 |
| US-to-CT registration | Mean localization error | **0.80 voxels** |
| Instrument detection | Mean angle error | **0.82 deg** |

## Project structure
spine-ultrasound-navigation/
├── preprocessing/ CT resampling + HU normalization
├── segmentation/ 3D U-Net dataset, training, and evaluation
├── reconstruction/ Marching-cubes mesh generation from masks
├── planning/ Geometric pedicle-center estimation
├── ultrasound/ Simulated B-mode ultrasound generation
├── registration/ US-to-CT slice localization (NCC search)
├── instrument/ Synthetic needle detection (classical CV)
├── navigation/ PyQt6 + PyVista desktop navigation app
├── data/ Dataset source, license, and setup notes
├── results/
│ ├── figures/ Visualizations from every stage
│ ├── metrics/ CSV outputs (Dice scores, pedicle coords, etc.)
│ ├── meshes/ Exported .stl spine meshes
│ └── predictions/ Saved model prediction volumes
└── requirements.txt


Each module folder has its own `README.md` documenting the method used and,
importantly, its **honest limitations** — this project prioritizes
transparent documentation of what was and wasn't validated over-claiming.

## Getting started

```bash
git clone https://github.com/abdul-rehman-24/spine-ultrasound-navigation.git
cd spine-ultrasound-navigation
pip install -r requirements.txt
```

### Dataset

This project uses the [VerSe19](https://github.com/anjany/verse) spine CT
dataset (CC BY-SA 4.0). See `data/README.md` for download links and citation
requirements. The scripts in this repo expect data in the VerSe BIDS-style
layout (`rawdata/sub-XXX/sub-XXX_ct.nii.gz` +
`derivatives/sub-XXX/sub-XXX_seg-vert_msk.nii.gz`).

### Running the navigation app

```bash
python navigation/navigation_app.py
```

1. Click **"Load Spine Mesh (.stl)"** then select a file from `results/meshes/`
2. Click **"Load Pedicle Points (.csv)"** then select a file from `results/metrics/`
3. Click any vertebra in the list to focus the camera on it

### Using individual modules

Each stage is a standalone, importable module. Example - running a
segmentation training loop:

```python
from segmentation.dataset import make_dataloader
from segmentation.train import build_model, train, evaluate
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = build_model(device)

train_loader = make_dataloader(train_files, train=True)
val_loader = make_dataloader(val_files, train=False)

train(model, train_loader, val_loader, device, max_epochs=100)
```

See each module's source for its exact function signatures.

## Key design decisions and lessons learned

- **DiceLoss alone gets stuck.** Early segmentation training plateaued at
  Dice around 0.10-0.15 for many epochs due to vanishing gradients when initial
  prediction/ground-truth overlap is near zero. Switching to `DiceCELoss`
  (Dice + Cross-Entropy) resolved this and reached Dice 0.83 on the test set.
- **Simulated ultrasound needs the right slice orientation.** Simulating
  ultrasound from a sagittal CT slice produces an unrealistic thin-line bone
  appearance. Using an axial-oriented slice (probe depth axis =
  anterior-posterior) produces the expected bone-surface echo + acoustic
  shadow pattern seen in real spine ultrasound.
- **Pedicle axis detection needs anatomical assumptions.** A naive
  "largest-spread axis" heuristic sometimes picked the superior-inferior
  axis instead of medial-lateral. Fixing the superior-inferior axis
  explicitly (based on known VerSe volume orientation) and choosing between
  the remaining two axes resolved this - validated by overlaying estimated
  points on 2D axial slices.

## Known limitations (documented honestly)

- Segmentation is **binary** (spine vs. background), not per-vertebra -
  per-vertebra pedicle planning uses VerSe's ground-truth labels, not the
  model's own prediction.
- Ultrasound is a **simplified 2D ray-casting simulation**, not real acquired
  data or a full acoustic wave simulator (e.g. k-Wave).
- Registration is a **1D slice-position search** along one axis, not a full
  6-DOF rigid + ICP registration as originally scoped.
- Instrument detection is validated **only on synthetic injected needles** in
  simulated ultrasound - not on real instruments or real US video.
- All results are from a **30-subject subset** of VerSe19, split 21/4/5 for
  train/val/test - not the full 374-scan dataset.

## Dataset citation

If reusing this pipeline, please cite the VerSe dataset papers listed in
`data/README.md`, per the CC BY-SA 4.0 license terms.

## License

Code in this repository is available for research and educational use.
The VerSe19 dataset is licensed separately under CC BY-SA 4.0 - see
`data/README.md`.
