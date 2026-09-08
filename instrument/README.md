# Surgical Instrument Detection/Tracking (Week 8)

## Method
Since real surgical instrument video/ultrasound is unavailable, this validates
the detection algorithm using synthetic needle injection into simulated
ultrasound frames (from Week 6):

1. Inject a synthetic bright straight line (needle) at a known position,
   angle, and length into a simulated US frame
2. Apply Canny edge detection to find image edges
3. Apply Probabilistic Hough Line Transform to find straight line segments
4. Select the longest detected line as the predicted instrument position

## Results (5 random test cases, varying angle/position/length)
| Test | True Angle | Detected Angle | Error |
|---|---|---|---|
| 1 | 26° | 25.4° | 0.6° |
| 2 | 55° | 56.0° | 1.0° |
| 3 | 128° | 129.5° | 1.5° |
| 4 | 75° | 75.7° | 0.7° |
| 5 | 26° | 25.7° | 0.3° |

Mean angle error: 0.82 degrees

## Limitations (documented, not hidden)
- Validated only on synthetic, injected needles — real instruments in real
  ultrasound have different reflectivity, artifacts (reverberation, comet-tail),
  and are affected by tissue motion, none of which are modeled here.
- No temporal tracking across frames (this detects a needle in a single static
  frame only, not continuous tracking across a video sequence).
- Longest-line heuristic assumes the needle is the most prominent straight
  edge in the frame, which may fail if bone edges or other structures produce
  longer/stronger line segments.
