"""CT preprocessing: resampling to isotropic spacing + HU normalization."""
import SimpleITK as sitk
import numpy as np


def resample_volume(image, new_spacing=(1.0, 1.0, 1.0), is_mask=False):
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()
    new_size = [
        int(round(original_size[i] * (original_spacing[i] / new_spacing[i])))
        for i in range(3)
    ]
    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(new_spacing)
    resample.SetSize(new_size)
    resample.SetOutputDirection(image.GetDirection())
    resample.SetOutputOrigin(image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(0)
    resample.SetInterpolator(sitk.sitkNearestNeighbor if is_mask else sitk.sitkLinear)
    return resample.Execute(image)


def normalize_ct(arr, hu_min=-200, hu_max=1500):
    clipped = np.clip(arr, hu_min, hu_max)
    return ((clipped - hu_min) / (hu_max - hu_min)).astype(np.float32)


def preprocess_ct_mask_pair(ct_path, mask_path, new_spacing=(1.0, 1.0, 1.0)):
    """Load, resample, normalize a CT+mask pair. Returns (sitk_image, sitk_mask)."""
    img = sitk.ReadImage(ct_path)
    mask = sitk.ReadImage(mask_path)

    img_r = resample_volume(img, new_spacing, is_mask=False)
    mask_r = resample_volume(mask, new_spacing, is_mask=True)

    arr = sitk.GetArrayFromImage(img_r)
    arr_norm = normalize_ct(arr)
    img_norm = sitk.GetImageFromArray(arr_norm)
    img_norm.CopyInformation(img_r)

    return img_norm, mask_r
