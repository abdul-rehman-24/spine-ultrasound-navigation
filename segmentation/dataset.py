"""Dataset/dataloader setup for 3D U-Net spine segmentation."""
import numpy as np
from monai.transforms import (
    Compose, LoadImaged, EnsureChannelFirstd, SpatialPadd,
    RandCropByPosNegLabeld, RandFlipd, RandRotate90d, EnsureTyped, MapTransform
)
from monai.data import Dataset, DataLoader

PATCH_SIZE = (96, 96, 96)


class BinarizeLabeld(MapTransform):
    """Converts a multi-label vertebra mask into a binary spine/background mask."""
    def __call__(self, data):
        d = dict(data)
        for key in self.keys:
            d[key] = (d[key] > 0).astype(np.float32)
        return d


def get_transforms(train=True, patch_size=PATCH_SIZE):
    base = [
        LoadImaged(keys=["image", "label"]),
        EnsureChannelFirstd(keys=["image", "label"]),
        BinarizeLabeld(keys=["label"]),
        SpatialPadd(keys=["image", "label"], spatial_size=patch_size, mode="constant"),
    ]
    if train:
        base += [
            RandCropByPosNegLabeld(
                keys=["image", "label"], label_key="label",
                spatial_size=patch_size, pos=1, neg=1, num_samples=4
            ),
            RandFlipd(keys=["image", "label"], prob=0.5, spatial_axis=0),
            RandRotate90d(keys=["image", "label"], prob=0.5, max_k=3),
        ]
    base.append(EnsureTyped(keys=["image", "label"]))
    return Compose(base)


def make_dataloader(data_dicts, train=True, batch_size=2, num_workers=0):
    transforms = get_transforms(train=train)
    ds = Dataset(data=data_dicts, transform=transforms)
    return DataLoader(ds, batch_size=batch_size, shuffle=train, num_workers=num_workers)
