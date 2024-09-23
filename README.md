# Countermovement jump height with Mediapipe
## Jump Height with Mediapipe BlazePose

### Overview

The **Countermovement Jump (CMJ)** is a key tool used to monitor and evaluate neuromuscular performance. With the rapid advancement of deep neural networks, it's now possible to identify joint positions without the need for markers—even in occluded situations—using just a single camera. This enables coaches and athletes to access important data about movements that were previously confined to laboratory settings.

**MediaPipe BlazePose (MPBP)** is a lightweight deep neural network developed for high-fidelity human pose detection (Bazarevsky et al., 2020). It tracks 33 body landmarks from a single 2D frame and can be implemented on various systems, including smartphones, without the need for a GPU.

### Objective

This project aims to validate the jump height obtained via the MPBP by analyzing the maximum height of the virtual trochanter marker. We conducted an experiment with 16 triathletes (4 female, 12 male) to compare the MPBP-based measurements against traditional methods.

### Experiment Details

- **Participants**: 16 triathletes (4 female, 12 male), aged 18 ± 3.1 years.
- **Jump protocol**: Participants performed 3 maximal CMJ jumps after a warm-up, with 30-second intervals between each jump.
- **Recording**: The jumps were filmed in the sagittal plane using an iPhone 7s at 120Hz.
- **Force Plate Data**: Ground reaction forces were recorded using a force plate (AMTI, USA) at 1000Hz.

### Jump Height Measurement Methods

1. **Flight Time Method**: Calculated from the time the athlete was airborne.
2. **Impulse Momentum Method**: Calculated from the force plate data.
3. **MediaPipe BlazePose (MPBP)**: Jump height obtained by measuring the maximum height of the virtual trochanter marker. The real-world distance between the trochanter and the floor was used for calibration.

### Results

- **Flight Time vs. MPBP**: Concordance Correlation Coefficient (CCC) = 0.90 [0.75; 0.96], Bias = -1.86 cm [-3.06; 0.65].
- **Impulse Momentum vs. MPBP**: CCC = 0.98 [0.88; 0.99], Bias = -0.86 cm [-1.72; 0.00].

The jump height calculated with MPBP was found to be valid when compared to both traditional methods, though it tended to slightly underestimate the actual height.

### Conclusion

Jump height determined by the maximum height of the virtual trochanter marker obtained using MPBP is a valid method, although it underestimates jump height by a small margin when compared to the impulse momentum and flight time methods. The smallest bias was observed when comparing MPBP to the impulse momentum method.


for trhocanter 

![image](https://github.com/user-attachments/assets/e39c8a79-8dc8-4a0c-b70c-4014f016aaa8)



for center of mass 

![image](https://github.com/user-attachments/assets/61c6410d-b91b-435a-9cf8-47e49948b3c1)



XX Congresso Brasileiro de Biomecância: https://bsb.org.br/wp-content/uploads/2024/02/365-Manuscript-file-Mandatory-3950-4407-10-20230525.pdf
with use the code considering cite: 10.13140/RG.2.2.14372.28801
