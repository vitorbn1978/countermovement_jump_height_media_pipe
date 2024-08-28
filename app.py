from flask import Flask, render_template, request, redirect, url_for
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Inicializando MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Função para processar os dados
def process_frame(landmarks, df_body_part, body_part_name, columns):
    new_row = {
        'x': landmarks[mp_pose.PoseLandmark[body_part_name].value].x,
        'y': landmarks[mp_pose.PoseLandmark[body_part_name].value].y,
        'z': landmarks[mp_pose.PoseLandmark[body_part_name].value].z,
        'visibility': landmarks[mp_pose.PoseLandmark[body_part_name].value].visibility
    }
    df_body_part = pd.concat([df_body_part, pd.DataFrame([new_row])], ignore_index=True)
    return df_body_part

@app.route('/')
def index():
    return render_template('index.html', result=None, video_url=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    if 'video' not in request.files or 'throchanter' not in request.form:
        return redirect(request.url)
    
    video_file = request.files['video']
    throchanter_height = float(request.form['throchanter'])

    if video_file.filename == '':
        return redirect(request.url)

    # Criando o diretório static caso não exista
    if not os.path.exists('static'):
        os.makedirs('static')

    # Salvando o vídeo em um arquivo temporário
    video_path = os.path.join("static", "uploaded_video.mp4")
    video_file.save(video_path)

    # Caminho para o vídeo processado
    processed_video_path = os.path.join("static", "processed_video.mp4")

    # Inicializando os DataFrames
    df_lhip = pd.DataFrame(columns=['x', 'y', 'z', 'visibility'])

    # Processando o vídeo e salvando com os landmarks desenhados
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec compatível
    out = cv2.VideoWriter(processed_video_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    if not cap.isOpened():
        print("Erro ao abrir o vídeo")
        return "Erro ao processar o vídeo"

    # Configurações do texto
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    color = (0, 0, 255)
    thickness = 3

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            try:
                landmarks = results.pose_landmarks.landmark
                df_lhip = process_frame(landmarks, df_lhip, 'LEFT_HIP', df_lhip.columns)
                
                # Desenhar os landmarks no frame
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
            except Exception as e:
                print(f"Erro ao processar landmarks: {e}")
            
            # Calculando a altura do salto
            qy = df_lhip['y']
            jumpheight = (throchanter_height * np.min(qy)) / np.mean(qy[0:30]) - throchanter_height
            jump_height_cm = round(jumpheight * -1, 2) * 100
            
            # Adicionar texto ao frame
            text = f"Jump Height: {jump_height_cm:.2f} cm"
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            org = (frame.shape[1] - text_size[0] - 10, 50)
            cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)
            
            # Escrever o frame processado no vídeo de saída
            out.write(frame)

    cap.release()
    out.release()

    # Verificar se o vídeo foi salvo corretamente
    if not os.path.exists(processed_video_path):
        print("Erro ao salvar o vídeo processado")
        return "Erro ao salvar o vídeo processado"

    # Passando o resultado e o caminho do vídeo processado para o template
    return render_template('index.html', result=f"Jump Height: {jump_height_cm:.2f} cm", video_url=url_for('static', filename='processed_video.mp4'))

if __name__ == '__main__':
    app.run(debug=True)

