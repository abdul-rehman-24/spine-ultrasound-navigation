"""Geometric pedicle-center estimation for a per-vertebra mask.

This is a heuristic (centroid + medial-lateral axis offset), not a trained
detector. Validated by overlaying results on 2D axial slices.
"""
import numpy as np


def get_vertebra_mask(mask_arr, label_id):
    return (mask_arr == label_id).astype(np.uint8)


def find_pedicle_centers(vert_mask, spacing, offset_ratio=0.3):
    """
    Estimates centroid + left/right pedicle centers for one vertebra mask.
    Coordinates are returned in (z, y, x) voxel-index space, consistent with
    the array order used by marching_cubes.
    """
    coords = np.argwhere(vert_mask > 0)
    if len(coords) < 50:
        return None

    spacing_zyx = np.array(spacing[::-1])
    coords_physical = coords * spacing_zyx
    centroid_physical = coords_physical.mean(axis=0)
    spreads = coords_physical.max(axis=0) - coords_physical.min(axis=0)

    # axis 0 (z) = superior-inferior, excluded. Medial-lateral = larger of y/x.
    candidate_axes = [1, 2]
    lr_axis_idx = candidate_axes[np.argmax([spreads[1], spreads[2]])]

    lr_direction = np.zeros(3)
    lr_direction[lr_axis_idx] = 1.0
    offset_distance = spreads[lr_axis_idx] * offset_ratio

    left_physical = centroid_physical + lr_direction * offset_distance
    right_physical = centroid_physical - lr_direction * offset_distance

    return {
        "centroid": centroid_physical / spacing_zyx,
        "left_pedicle_approx": left_physical / spacing_zyx,
        "right_pedicle_approx": right_physical / spacing_zyx,
        "spreads": spreads,
    }


def estimate_all_vertebrae(mask_arr, spacing):
    """Runs pedicle estimation for every non-background label in the mask."""
    unique_labels = np.unique(mask_arr)
    unique_labels = unique_labels[unique_labels > 0]
    results = {}
    for label in unique_labels:
        label = int(label)
        vmask = get_vertebra_mask(mask_arr, label)
        if vmask.sum() < 50:
            continue
        res = find_pedicle_centers(vmask, spacing)
        if res is not None:
            results[label] = res
    return results
