# Countermovement jump height with Mediapipe
Jump Height with Mediapipe BlazePose

The countermovement jump height (CMJ) is considered an important tool for monitoring and evaluating neuromuscular characteristics. The rapid development of deep neural networks to identify joints without the use of markers, even when they are covered, and the possibility of using one or more cameras gives coaches and athletes access to important movement-related information, previously only identified in laboratory environments. The MediaPipe BlazePose (MPBP) is a lightweight deep neural network developed by for high-fidelity human pose detection (Bazarevsky et al., 2020), inferring 33 reference points of a body from a single 2D frame, that can be implemented on different operating systems without the need for a GPU and processed on smartphones. Despite being easy to use, such joint recognition models may have virtual markers that are different from anatomical markers. The aim of the present study was to analyse the validity of the jump height evaluated through the MPBP using the maximum height of the virtual trochanter marker. Sixteen triathletes (n = 4 female, 12 male) aged 18±3.1 years participated in the study. After warm-up participants performed 3 maximum SCM jumps with an interval of 30 seconds, being filmed in the sagittal plane by smartphone (iPhone 7s, Apple Inc., EUA), frequency of acquisition 120hz. During the jump, ground reaction force was record with a force plate (AMTI, Advanced Mechanical. Technology, Inc., Waltham Street, Watertown, MA, USA), frequency of acquisition of 1000hz. The jump height was calculated with to methods from impulse momentum, and flight time. For MPBP the jump height was obtained by the maximum height of the virtual trochanter. For calibration the real distance between trochanter and floor was used. Validity was tested using the concordance correlation coefficient (CCC) and measures of agreement between jump height methods are calculate using the package epiR from software R (version 4.2.2, 2022). There was validity between flight time and MPBP (CCC: 0.90 [0.75; 0.96]; bias: -1.86 cm [-3.06; 0.65]), and between impulse momentum and MPBP (CCC: 0.98 [0.88 - 0.99], bias: - 0.86 cm [-1.72; - 0.00]). We can conclude that jump height through the maximum height of the virtual trochanter marker obtained with MPBP is valid, but the value was underestimated for both methods, with the smallest bias in relation to the jump height observed in relation to impulse momentum method.

for trhocanter 

![image](https://github.com/user-attachments/assets/e39c8a79-8dc8-4a0c-b70c-4014f016aaa8)



for center of mass 

![image](https://github.com/user-attachments/assets/61c6410d-b91b-435a-9cf8-47e49948b3c1)



XX Congresso Brasileiro de Biomecância: https://bsb.org.br/wp-content/uploads/2024/02/365-Manuscript-file-Mandatory-3950-4407-10-20230525.pdf
with use the code considering cite: 10.13140/RG.2.2.14372.28801
