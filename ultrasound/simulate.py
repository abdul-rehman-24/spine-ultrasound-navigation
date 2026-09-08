"""Simplified 2D ray-casting ultrasound simulation from a CT slice.

Not a full acoustic wave simulator (e.g. k-Wave) - sufficient for MVP
registration/detection testing, not for realistic image-quality assessment.
Key finding: use an axial-oriented CT slice (probe depth = anterior-posterior),
not a sagittal slice, or the bone-shadow effect looks unrealistic.
"""
import numpy as np
from scipy.ndimage import gaussian_filter


def simulate_ultrasound_slice(ct_slice, bone_threshold=0.5):
    h, w = ct_slice.shape
    us_image = np.zeros_like(ct_slice)

    for col in range(w):
        column = ct_slice[:, col]
        attenuation = 1.0
        shadow_started = False
        for row in range(h):
            intensity = column[row]
            if intensity > bone_threshold and not shadow_started:
                us_image[row, col] = 1.0
                shadow_started = True
                attenuation = 0.05
            elif shadow_started:
                us_image[row, col] = intensity * attenuation * 0.1
            else:
                us_image[row, col] = intensity * attenuation
                attenuation *= 0.995

    speckle = np.random.gamma(shape=4.0, scale=0.15, size=us_image.shape)
    us_image = us_image * speckle
    us_image = gaussian_filter(us_image, sigma=0.7)
    return np.clip(us_image, 0, 1)
