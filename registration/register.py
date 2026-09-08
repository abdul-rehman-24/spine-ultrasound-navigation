"""US-to-CT slice localization via Normalized Cross-Correlation search.

Note: this is a 1D slice-position search (single translation axis), not a
full 6-DOF rigid registration. See registration/README.md for discussion.
"""
import numpy as np
from ultrasound.simulate import simulate_ultrasound_slice


def normalized_cross_correlation(img1, img2):
    img1_norm = (img1 - img1.mean()) / (img1.std() + 1e-8)
    img2_norm = (img2 - img2.mean()) / (img2.std() + 1e-8)
    return np.mean(img1_norm * img2_norm)


def find_best_matching_slice(ct_arr, query_us, step=2):
    """Searches y-axis slices of ct_arr for the best NCC match to query_us."""
    search_range = range(0, ct_arr.shape[1], step)
    scores = []
    for y in search_range:
        candidate_us = simulate_ultrasound_slice(ct_arr[:, y, :])
        scores.append(normalized_cross_correlation(query_us, candidate_us))
    scores = np.array(scores)
    best_idx = np.argmax(scores)
    predicted_y = list(search_range)[best_idx]
    return predicted_y, scores, list(search_range)
