# Data

This project uses the VerSe19 dataset (official release).

## Source
- Training split: https://s3.bonescreen.de/public/VerSe-complete/dataset-verse19training.zip
- Validation split: https://s3.bonescreen.de/public/VerSe-complete/dataset-verse19validation.zip
- Test split: https://s3.bonescreen.de/public/VerSe-complete/dataset-verse19test.zip
- Official repo: https://github.com/anjany/verse

This project uses only the training split, with a custom 70/15/15
train/val/test split (30 subjects total: 21 train / 4 val / 5 test).
License: CC BY-SA 4.0 (see official repo for citation requirements).

## Week 3 Results (Binary Spine Segmentation)
- Model: 3D U-Net (MONAI), DiceCELoss (Dice + Cross-Entropy combo)
- Training: 100 epochs total (60 initial + 40 extended, resumed from checkpoint)
- Best Validation Dice: 0.7285
- Mean Test Dice: 0.8297 (5 held-out test subjects)

Note: An earlier attempt using pure DiceLoss got stuck near Dice 0.10-0.15
due to the vanishing-gradient issue with near-zero initial overlap.
Switching to DiceCELoss resolved this.
