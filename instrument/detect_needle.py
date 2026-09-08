"""Synthetic needle injection + classical CV detection (Canny + Hough).

Validated only on synthetic injected needles - see instrument/README.md
for limitations regarding real ultrasound instrument appearance.
"""
import numpy as np
import cv2


def inject_synthetic_needle(us_image, start_point, angle_deg, length):
    img_with_needle = us_image.copy()
    angle_rad = np.deg2rad(angle_deg)
    end_x = int(start_point[0] + length * np.cos(angle_rad))
    end_y = int(start_point[1] + length * np.sin(angle_rad))

    img_uint8 = (img_with_needle * 255).astype(np.uint8)
    img_uint8 = cv2.cvtColor(img_uint8, cv2.COLOR_GRAY2BGR)
    cv2.line(img_uint8, start_point, (end_x, end_y), (255, 255, 255), thickness=2)
    img_with_needle = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

    return img_with_needle, (start_point, (end_x, end_y))


def detect_needle_hough(us_image):
    img_uint8 = (us_image * 255).astype(np.uint8)
    img_blurred = cv2.GaussianBlur(img_uint8, (3, 3), 0)
    edges = cv2.Canny(img_blurred, threshold1=100, threshold2=200)
    lines = cv2.HoughLinesP(
        edges, rho=1, theta=np.pi / 180, threshold=30,
        minLineLength=40, maxLineGap=5
    )
    return lines, edges


def get_longest_line(lines):
    if lines is None or len(lines) == 0:
        return None, 0
    max_len = 0
    best_line = None
    for l in lines:
        x1, y1, x2, y2 = l[0]
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if length > max_len:
            max_len = length
            best_line = (x1, y1, x2, y2)
    return best_line, max_len
