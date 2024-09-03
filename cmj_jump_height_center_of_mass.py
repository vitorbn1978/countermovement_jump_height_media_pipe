import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

# Inicializando o Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Função para calcular o COM de um segmento
def calculate_segment_com(landmarks, indices):
    segment_points = np.array([[
        landmarks[idx].x, 
        landmarks[idx].y, 
        landmarks[idx].z
    ] for idx in indices])
    com = np.mean(segment_points, axis=0)
    return com

# Função para calcular o COM do corpo
def calculate_body_com(landmarks, height, weight):
    # Pesos relativos dos segmentos ajustados para o peso do indivíduo
    SEGMENT_WEIGHTS = {
        'head': 0.081 * weight,
        'torso': 0.497 * weight,
        'left_arm': 0.0265 * weight,
        'right_arm': 0.0265 * weight,
        'left_leg': 0.161 * weight,
        'right_leg': 0.161 * weight
    }
    
    # Definindo os índices dos landmarks para cada segmento
    segments = {
        'head': [0, 1, 2, 3, 4],
        'torso': [11, 12, 23, 24],
        'left_arm': [11, 13, 15],
        'right_arm': [12, 14, 16],
        'left_leg': [23, 25, 27],
        'right_leg': [24, 26, 28]
    }
    
    # Calculando o COM ponderado de cada segmento
    weighted_coms = []
    total_weight = 0
    for segment, indices in segments.items():
        segment_com = calculate_segment_com(landmarks, indices)
        weight = SEGMENT_WEIGHTS[segment]
        weighted_coms.append(segment_com * weight)
        total_weight += weight

    # Cálculo do COM do corpo
    overall_com = np.sum(weighted_coms, axis=0) / total_weight
    return overall_com

# Lista para armazenar o caminho do centro de massa
cm_path = []

# Lista para armazenar as alturas do CM para o gráfico
cm_heights = []

# Variáveis para armazenar as alturas do CM
max_cm_height = -np.inf
initial_cm_heights = []  # Lista para armazenar as alturas iniciais do CM

# Processamento de vídeo para curar e calcular o centro de massa
cap = cv2.VideoCapture("v_jump.mp4") #se for usar web cam colocar 0 ou nome do video "video.mp4", "video.mov"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('processed_video.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
frame_count = 0  # Contador de frames

# Variável para armazenar a altura do salto calculada
jump_height_m = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convertendo a imagem para RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        # Defina a altura e o peso do indivíduo (em metros e kg)
        height = 1.70  # Estatura
        weight = 70.0  # Peso
        body_com = calculate_body_com(landmarks, height, weight)

        # Ajustar a posição do CM para a área da imagem
        height_img, width_img, _ = frame.shape
        # Converte as coordenadas do CM para pixels corretamente
        cm_x_pixel = int(body_com[0] * width_img)
        cm_y_pixel = int(body_com[1] * height_img)  # Não inverter Y para manter o desenho correto

        # Atualizar a altura máxima do CM em metros, invertendo a escala de Y
        cm_height_m = (1 - body_com[1]) * height  # Ajusta para refletir corretamente o movimento real
        
        # Coletar as alturas iniciais do CM nos primeiros 10 quadros
        if frame_count < 10:
            initial_cm_heights.append(cm_height_m)

        # Atualiza o valor da altura máxima
        max_cm_height = max(max_cm_height, cm_height_m)

        # Adiciona a altura do CM para os cálculos
        cm_heights.append(cm_height_m)
        
        # Adiciona a posição do centro de massa à lista do caminho
        cm_path.append((cm_x_pixel, cm_y_pixel))

        # Desenhar o caminho do centro de massa no centro do corpo em branco
        for i in range(1, len(cm_path)):
            cv2.line(frame, cm_path[i - 1], cm_path[i], (255, 255, 255), 2)

        # Desenhar o ponto atual do centro de massa no frame com fundo preto
        cv2.rectangle(frame, (cm_x_pixel - 3, cm_y_pixel - 3), (cm_x_pixel + 3, cm_y_pixel + 3), (0, 0, 0), -1)
        cv2.circle(frame, (cm_x_pixel, cm_y_pixel), 5, (255, 255, 255), -1)
        cv2.putText(frame, "CM", (cm_x_pixel, cm_y_pixel), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Adicionar a altura do CM no canto superior esquerdo do vídeo
        cv2.putText(frame, f"Altura do CM: {cm_height_m:.2f} m", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        # Calcular a altura do salto durante o processamento
        if frame_count >= 10:
            initial_cm_height_mean = np.mean(initial_cm_heights)
            jump_height_m = max_cm_height - initial_cm_height_mean

        # Adicionar a altura do salto no canto superior direito do vídeo
        cv2.putText(frame, f"Altura do Salto: {jump_height_m:.2f} m", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    # Escrever o frame no vídeo de saída
    out.write(frame)

    # Mostrar o frame processado (opcional)
    cv2.imshow('Centro de Massa', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Incrementar o contador de frames
    frame_count += 1

cap.release()
out.release()
cv2.destroyAllWindows()

# Calcular a altura inicial média do CM nos primeiros 10 quadros
initial_cm_height_mean = np.mean(initial_cm_heights)

# Mostrar as alturas do CM e a altura do salto
print(f"Altura Inicial do Centro de Massa: {initial_cm_height_mean:.2f} m")
print(f"Altura Máxima do Centro de Massa: {max_cm_height:.2f} m")
print(f"Altura do Salto Calculada: {jump_height_m:.2f} m")

# Gerar o gráfico da altura do CM ao longo do tempo
plt.plot(cm_heights, label='Altura do CM (Ajustada para Cálculo)')
plt.axhline(initial_cm_height_mean, color='r', linestyle='--', label='Altura Inicial Média do CM')
plt.xlabel('Quadros')
plt.ylabel('Altura do CM (m)')
plt.title('Trajetória do Centro de Massa Durante o Salto')
plt.grid(True)
plt.legend()
plt.show()
