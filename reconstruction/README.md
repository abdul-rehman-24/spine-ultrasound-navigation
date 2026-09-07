# 3D Reconstruction (Week 4)

## Method
1. Load trained 3D U-Net checkpoint (Week 3, Test Dice 0.8297)
2. Run sliding-window inference on full CT volume to get binary spine mask
3. Apply largest-connected-component filtering to remove noise/disconnected regions
4. Run marching cubes (skimage) to extract 3D surface mesh from the cleaned mask
5. Export mesh as STL for downstream use (pedicle planning, navigation viz)

## Sample Result (sub-verse004)
- Raw mesh: 170,330 vertices, 341,222 faces
- Cleaned mesh (largest component only): 168,216 vertices, 337,268 faces

## Notes
- Rendering uses matplotlib (Poly3DCollection) instead of PyVista's interactive
  renderer, since PyVista/VTK off-screen rendering crashed the Kaggle kernel
  (no working OpenGL context in this container).
- Mesh is currently a binary spine mesh (not per-vertebra separated) — 
  per-vertebra separation will be needed for Week 5 pedicle planning.
