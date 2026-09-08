"""3D mesh reconstruction from a binary segmentation mask via marching cubes."""
import numpy as np
from skimage import measure
from scipy import ndimage


def keep_largest_component(binary_mask):
    """Removes small disconnected noise regions, keeping only the largest component."""
    labeled, num_features = ndimage.label(binary_mask)
    if num_features == 0:
        return binary_mask
    sizes = ndimage.sum(binary_mask, labeled, range(1, num_features + 1))
    largest_label = np.argmax(sizes) + 1
    return (labeled == largest_label).astype(np.float32)


def mask_to_mesh(binary_mask, clean=True, level=0.5):
    """Returns (verts, faces) from a binary mask using marching cubes."""
    mask = keep_largest_component(binary_mask) if clean else binary_mask
    verts, faces, normals, values = measure.marching_cubes(mask, level=level)
    return verts, faces
