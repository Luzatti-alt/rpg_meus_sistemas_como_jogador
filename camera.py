import cv2
import numpy as np
# ===== Configuração de captura =====
cam = cv2.VideoCapture(0)
explosao_cap = cv2.VideoCapture("videos/Deltarune Explosion Green Screen(720P_HD).mp4")
# ===== Variáveis globais =====
rotacao = 0
state = 0
fichas = []
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
imagens_dados = {}
hp_personagem = None
mana_personagem = None
nome_personagem_atual = None
def carregar_imagens_dados():
    try:
        # Tente carregar as imagens. Substitua os caminhos de arquivo se necessário.
        imagens_dados['d4'] = cv2.imread('imagens/d4-removebg-preview.png', cv2.IMREAD_UNCHANGED)
        imagens_dados['d6'] = cv2.imread('imagens/d6-removebg-preview.png', cv2.IMREAD_UNCHANGED)
        imagens_dados['d10'] = cv2.imread('imagens/d20-removebg-preview.png', cv2.IMREAD_UNCHANGED)
        imagens_dados['d20'] = cv2.imread('imagens/d20-removebg-preview.png', cv2.IMREAD_UNCHANGED)
    except Exception as e:
        print(f"Erro ao carregar imagens dos dados: {e}")

# Chame esta função na inicialização para pré-carregar as imagens.
carregar_imagens_dados()

# ===== Funções =====
def hp_val(frame):
    global hp_personagem, nome_personagem_atual
    hp_img = cv2.imread("imagens/escudo-removebg-preview.png", cv2.IMREAD_UNCHANGED)
    if hp_personagem is not None and nome_personagem_atual is not None and hp_img is not None:
        esc_h, esc_w = hp_img.shape[:2]
        # Redimensiona se for maior que o frame
        if esc_h > frame.shape[0] or esc_w > frame.shape[1]:
            escala = min(frame.shape[0] / esc_h, frame.shape[1] / esc_w, 0.2)
            esc_w = int(esc_w * escala)
            esc_h = int(esc_h * escala)
            hp_img = cv2.resize(hp_img, (esc_w, esc_h), interpolation=cv2.INTER_AREA)
        # Centro desejado do escudo
        center_x = frame.shape[1] - esc_w // 2 - 20
        center_y = 20 + esc_h // 2
        x_escudo = center_x - esc_w // 2
        y_escudo = center_y - esc_h // 2
        frame = sobrepor_imagem_fundo(frame, hp_img, x_escudo, y_escudo)
        # Número centralizado no escudo
        texto = str(hp_personagem)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        text_size, baseline = cv2.getTextSize(texto, font, font_scale, thickness)
        text_x = center_x - text_size[0] // 2
        text_y = center_y + text_size[1] // 2
        cv2.putText(frame, texto, (text_x, text_y), font, font_scale,
                    (255, 255, 255), thickness, cv2.LINE_AA)
    return frame
def mana_val(frame):
    global mana_personagem, nome_personagem_atual
    mana_img = cv2.imread("imagens/mana-removebg-preview.png", cv2.IMREAD_UNCHANGED)
    if mana_personagem is not None and nome_personagem_atual is not None and mana_img is not None:
        esc_h, esc_w = mana_img.shape[:2]
        # Redimensiona se for maior que o frame
        if esc_h > frame.shape[0] or esc_w > frame.shape[1]:
            escala = min(frame.shape[0] / esc_h, frame.shape[1] / esc_w, 0.2)
            esc_w = int(esc_w * escala)
            esc_h = int(esc_h * escala)
            mana_img = cv2.resize(mana_img, (esc_w, esc_h), interpolation=cv2.INTER_AREA)
        # Posição igual ao escudo, mas Y deslocado para baixo
        center_x = frame.shape[1] - esc_w // 2 - 20
        # Pega a posição do escudo (usada em hp_val)
        escudo_img = cv2.imread("imagens/escudo-removebg-preview.png", cv2.IMREAD_UNCHANGED)
        escudo_h = escudo_img.shape[0] if escudo_img is not None else 0
        center_y = 20 + escudo_h + esc_h // 2 + 10  # 10 pixels abaixo do escudo
        x_escudo = center_x - esc_w // 2
        y_escudo = center_y - esc_h // 2
        frame = sobrepor_imagem_fundo(frame, mana_img, x_escudo, y_escudo)
        # Número centralizado no escudo de mana
        texto = str(mana_personagem)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        text_size, baseline = cv2.getTextSize(texto, font, font_scale, thickness)
        text_x = center_x - text_size[0] // 2
        text_y = center_y + text_size[1] // 2
        cv2.putText(frame, texto, (text_x, text_y), font, font_scale,
                    (255, 255, 255), thickness, cv2.LINE_AA)
    return frame
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

def rotacionar_camera(direcao):
        global rotacao
        if direcao == 'direita':
            rotacao = 90
        elif direcao == 'esquerda':
            rotacao = 270
        elif direcao == "baixo":  # Alteração necessária
            rotacao = 180
        elif direcao == "cima":   # Alteração necessária
            rotacao = 0
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

# ===== Funções para a rotação e rolagem de dados =====

def rolar_dado(tipo_dado):
    global dado_atual_img, dado_atual_num  
    import random
    class Dados:
        def d4(): return random.randint(1,4)
        def d6(): return random.randint(1,6)
        def d10(): return random.randint(1,10)
        def d20(): return random.randint(1,20)    
    if tipo_dado == 'd4':
        dado_atual_num = Dados.d4()
        dado_atual_img = imagens_dados['d4']
    elif tipo_dado == 'd6':
        dado_atual_num = Dados.d6()
        dado_atual_img = imagens_dados['d6']
    elif tipo_dado == 'd10':
        dado_atual_num = Dados.d10()
        dado_atual_img = imagens_dados['d10']
    elif tipo_dado == 'd20':
        dado_atual_num = Dados.d20()
        dado_atual_img = imagens_dados['d20']
    # Retorna o resultado da rolagem.
    return f'Você rolou um {tipo_dado} e o resultado foi {dado_atual_num}!'

# ===== Adicionando a função para aplicar o filtro =====
def aplicar_filtro(nome_filtro):
    global hsv_state_red, hsv_state_blue, hsv_state_green, pixelar_ativo, negativo_ativo, escurecer_ativo, police, walter, mostrar_explosao
    # Desativa todos os efeitos primeiro
    hsv_state_red = False
    hsv_state_blue = False
    hsv_state_green = False
    pixelar_ativo = False
    negativo_ativo = False
    escurecer_ativo = False
    police = False
    walter = False
    mostrar_explosao = False
    # Ativa o efeito selecionado
    if nome_filtro == 'vermelho':
        hsv_state_red = True
    elif nome_filtro == 'azul':
        hsv_state_blue = True
    elif nome_filtro == 'verde':
        hsv_state_green = True
    elif nome_filtro == 'pixelar':
        pixelar_ativo = True
    elif nome_filtro == 'invertido':
        negativo_ativo = True
    elif nome_filtro == 'escurecido':
        escurecer_ativo = True
    elif nome_filtro == 'policia':
        police = True
    elif nome_filtro == 'laranja':
        walter = True
    elif nome_filtro == 'explosao':
        mostrar_explosao = True
def get_frame():
    global explosao_cap, mostrar_explosao, rotacao
    ret_cam, frame = cam.read()
    if not ret_cam:
        return None
    if rotacao != 0:
        (h, w) = frame.shape[:2]
        (cx, cy) = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D((cx, cy), rotacao, 1.0)
        frame = cv2.warpAffine(frame, M, (w, h))
    # Rotação
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
                frame_h, frame_w = frame_display.shape[:2]
                frame_exp = cv2.resize(frame_exp, (639, 479))  # Redimensiona a explosão
                frame_exp_sem_fundo, mask_inv = remover_fundo_verde(frame_exp)
                h, w = frame_exp.shape[:2]
                x_offset = (frame_w - w) // 2
                y_offset = (frame_h - h) // 2
                # Garante que não vamos acessar fora dos limites do frame
                if y_offset + h > frame_display.shape[0] or x_offset + w > frame_display.shape[1]:
                    print("Erro: explosão fora dos limites da tela")
                    return frame_display
                roi = frame_display[y_offset:y_offset+h, x_offset:x_offset+w]
                # Garante que a máscara tem o mesmo tamanho do ROI
                if mask_inv.shape[:2] != roi.shape[:2]:
                    mask_inv = cv2.resize(mask_inv, (roi.shape[1], roi.shape[0]))   
                bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask_inv))
                fg = cv2.bitwise_and(frame_exp, frame_exp, mask=mask_inv)
                combinada = cv2.add(bg, fg)
                frame_display[y_offset:y_offset+h, x_offset:x_offset+w] = combinada
    if state == 2:
        frame_display = cv2.cvtColor(frame_display, cv2.COLOR_BGR2GRAY)
        frame_display = cv2.cvtColor(frame_display, cv2.COLOR_GRAY2BGR)

    frame_display = mostrar_dado_no_frame(frame_display)
    frame_display = hp_val(frame_display)
    #frame_display = mana_val(frame_display)
    #comentado enquanto nn estiver feito
    return frame_display
if __name__ == '__main__':
    resultado = rolar_dado('d20')

    rotacionar_camera('direita')
    

