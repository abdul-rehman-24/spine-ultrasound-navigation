# Ultrasound Simulation (Week 6)

## Method
Since paired real ultrasound-CT spine data is scarce, this project uses a
simulated ultrasound approach (as planned in the original MVP scope).

For each axial-like CT slice:
1. Ray-cast column by column, simulating probe beam traveling posterior-to-anterior
2. On hitting bone (intensity > threshold): render bright echo, then start acoustic shadow
3. Below bone: heavily attenuated signal (acoustic shadow effect)
4. Add speckle noise (gamma-distributed) to mimic ultrasound texture
5. Slight Gaussian smoothing for realism

## Key finding
Using a sagittal-oriented CT slice gave unrealistic results (bone appears as thin
lines, not the enclosing arc typical of axial ultrasound views). Switching to an
axial CT slice (probe depth axis = anterior-posterior) produced a much more
anatomically realistic result, with clear bone-surface echo and acoustic shadow
columns matching real spine ultrasound characteristics.

## Output
8 sample subjects processed, simulated US + corresponding CT slice pairs saved
as .npy arrays in results/simulated_us/, for use in Week 7 (US-to-3D registration).

## Limitation
This is a simplified 2D ray-casting simulation, not a full acoustic wave simulator
(e.g. k-Wave). Sufficient for MVP registration testing but not for realistic
US image quality assessment.
