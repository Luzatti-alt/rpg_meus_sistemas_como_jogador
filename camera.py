import cv2
import numpy as np

# ===== Configuração de captura =====
cam = cv2.VideoCapture(0)
explosao_cap = cv2.VideoCapture("videos/Deltarune Explosion Green Screen(720P_HD).mp4")

# ===== Variáveis globais =====
rotacao = 0
state = 0
mana = hp = mana_max = 100
fichas = []
ficha_esc = 0
escurecer_ativo = False
red_blue_off = False
hsv_state_red = False
hsv_state_blue = False
hsv_state_green = False
police = False
police_contador = 0
walter = False
pixelar_ativo = False
negativo_ativo = False
mostrar_explosao = False
dado_atual_img = None
dado_atual_num = None

# ===== Funções =====
def mostrar_dado_no_frame(frame):
    global dado_atual_img, dado_atual_num
    if dado_atual_img is not None and dado_atual_num is not None:
        x, y = 10, 10
        frame = sobrepor_imagem_fundo(frame, dado_atual_img, x, y)
        img_h, img_w = dado_atual_img.shape[:2]
        center_x = x + img_w // 2
        center_y = y + img_h // 2
        text = str(dado_atual_num)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_x = center_x - text_size[0] // 2
        text_y = center_y + text_size[1] // 2
        cv2.putText(frame, text, (text_x, text_y), font, font_scale,
                    (255, 255, 255), thickness, cv2.LINE_AA)
    return frame

def sobrepor_imagem_fundo(frame, imagem, x, y):
    h, w = imagem.shape[:2]
    if y + h > frame.shape[0] or x + w > frame.shape[1]:
        return frame
    roi = frame[y:y+h, x:x+w]
    if imagem.shape[2] == 4:
        overlay = imagem[:, :, :3]
        mask = imagem[:, :, 3:] / 255.0
        roi[:] = (1.0 - mask) * roi + mask * overlay
    else:
        frame[y:y+h, x:x+w] = imagem
    return frame

def remover_fundo_verde(frame_video):
    hsv = cv2.cvtColor(frame_video, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask_inv = cv2.bitwise_not(mask)
    frame_video_sem_fundo = cv2.bitwise_and(frame_video, frame_video, mask=mask_inv)
    return frame_video_sem_fundo, mask_inv

def barras_webcam(img):
    try:
        hp_val = fichas[ficha_esc].hp_val
        hp_max = fichas[ficha_esc].hp
        mana_val = fichas[ficha_esc].esp
        mana_max_val = fichas[ficha_esc].esp_max
    except:
        hp_val, hp_max, mana_val, mana_max_val = 80, 100, 50, 100

    cor_hp_full = (13, 217, 16)
    cor_hp_incompleto = (0, 0, 255)
    cor_mana_full = (0, 234, 255)
    cor_mana_incompleto = (254, 255, 207)
    largura = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    barra_hp_max_width = int(largura - (largura / 8) - 50)
    barra_hp_min_x = 50
    barra_hp_height_y1 = int(altura - 100)
    barra_hp_height_y2 = int(altura - 50)
    hp_ratio = max(0, min((hp_val / hp_max), 1.65))
    hp_width = int((barra_hp_max_width - barra_hp_min_x) * hp_ratio)
    cv2.rectangle(img, (barra_hp_min_x, barra_hp_height_y1),
                  (barra_hp_max_width, barra_hp_height_y2), cor_hp_incompleto, -1)
    cv2.rectangle(img, (barra_hp_min_x, barra_hp_height_y1),
                  (barra_hp_min_x + hp_width, barra_hp_height_y2), cor_hp_full, -1)
    barra_mana_max_y1 = int(altura - (altura / 10))
    barra_mana_min_y = int(altura / 10)
    barra_mana_x1 = int(largura - 100)
    barra_mana_x2 = int(largura - 50)
    mana_ratio = max(0, min(mana_val / mana_max_val, 1))
    mana_height = int((barra_mana_max_y1 - barra_mana_min_y) * mana_ratio)
    cv2.rectangle(img, (barra_mana_x1, barra_mana_min_y),
                  (barra_mana_x2, barra_mana_max_y1), cor_mana_incompleto, -1)
    cv2.rectangle(img, (barra_mana_x1, barra_mana_max_y1 - mana_height),
                  (barra_mana_x2, barra_mana_max_y1), cor_mana_full, -1)
    return img

# ==== Filtros ====
def pixelar(img):
    altura, largura = img.shape[:2]
    pequeno = cv2.resize(img, (32, 24), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(pequeno, (largura, altura), interpolation=cv2.INTER_NEAREST)

def negativo(img):
    return cv2.bitwise_not(img)

def escurecer(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = (v * 0.42).clip(0, 255).astype(np.uint8)
    hsv_mod = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)

def vermelho(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h[:] = 179
    s = cv2.add(s, 120)
    s = np.clip(s, 0, 255).astype(np.uint8)
    hsv_mod = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)

def azul(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h[:] = 120
    s = cv2.add(s, 50)
    s = np.clip(s, 0, 255).astype(np.uint8)
    hsv_mod = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)

def verde(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h[:] = 60
    s = cv2.add(s, 50)
    s = np.clip(s, 0, 255).astype(np.uint8)
    hsv_mod = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)

def filtro_walter(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h[:] = 10
    s = cv2.add(s, 50)
    s = np.clip(s, 60, 255).astype(np.uint8)
    hsv_mod = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)

# ===== Função chamada pelo Kivy =====
def get_frame():
    """Retorna um frame processado para exibir no Kivy."""
    global explosao_cap, mostrar_explosao

    ret_cam, frame = cam.read()
    if not ret_cam:
        return None

    frame = barras_webcam(frame)

    # Rotação
    if rotacao == 1:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif rotacao == 2:
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    elif rotacao == 3:
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    frame_display = frame.copy()

    # Filtros
    if police and not red_blue_off:
        global police_contador
        police_contador += 1
        if police_contador % 30 < 15:
            frame_display = vermelho(frame_display)
        else:
            frame_display = azul(frame_display)
    else:
        if hsv_state_red and not red_blue_off:
            frame_display = vermelho(frame_display)
        if hsv_state_blue and not red_blue_off:
            frame_display = azul(frame_display)
        if hsv_state_green:
            frame_display = verde(frame_display)
        if walter:
            frame_display = filtro_walter(frame_display)
        if pixelar_ativo:
            frame_display = pixelar(frame_display)
        if negativo_ativo:
            frame_display = negativo(frame_display)
        if escurecer_ativo:
            frame_display = escurecer(frame_display)
        if mostrar_explosao:
            ret_exp, frame_exp = explosao_cap.read()
            if not ret_exp:
                explosao_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                mostrar_explosao = False
            else:
                frame_exp = cv2.resize(frame_exp, (480, 480))
                _, mask_inv = remover_fundo_verde(frame_exp)
                x_offset, y_offset = 100, 100
                h, w = frame_exp.shape[:2]
                roi = frame_display[y_offset:y_offset+h, x_offset:x_offset+w]
                bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask_inv))
                fg = cv2.bitwise_and(frame_exp, frame_exp, mask=mask_inv)
                combinada = cv2.add(bg, fg)
                frame_display[y_offset:y_offset+h, x_offset:x_offset+w] = combinada

    if state == 2:
        frame_display = cv2.cvtColor(frame_display, cv2.COLOR_BGR2GRAY)
        frame_display = cv2.cvtColor(frame_display, cv2.COLOR_GRAY2BGR)

    frame_display = mostrar_dado_no_frame(frame_display)
    return frame_display
