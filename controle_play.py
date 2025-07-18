from ficha import *
from Dados import * #add na camera o resultado o que falta dos dados
import cv2
import keyboard
import numpy as np
import keyboard
import threading #para poder rodar a camera e os inputs
turnos_reviver = 3
ficha_esc = input("selecione a ficha: ").lower()
explosao_cap = cv2.VideoCapture("videos/Deltarune Explosion Green Screen(720P_HD).mp4")
valido = False
cam_on = False
mostrar_explosao = False
rotacao = 0
state = 1
escurecer_ativo = False 
red_blue_off = True
hsv_state_red = False
hsv_state_blue = False
hsv_state_green = False
police = False
police_contador  = 0
walter = False
enter_pressed = False
pixelar_ativo = False
negativo_ativo = False
dado_atual_img = None
dado_atual_num = None
#so para conseguir acessar o metodo de hab_bonus e fazer a consulta da ficha aqui
fichas = {
    "golpnur": golpnur,# obj e como ele fica aqui
    "xx": xx,#add outros players e seu objs(dados da ficha) n arquivo onde fica localizado as fichas e aqui do jeito que esta
}
def instrucoes():
    print("\ninstruções deste controle use somente durante combate \nver ficha | ficha \nsofreu dano | dano e dps num de dano sofrido(ex dano 5) curado | vida e dps num da cura(vida 5) upou de nivel | lv up usou habilidade | hab usada dps o nome dela e por fim qnt de vezs usadas no turno ex chute 1(chute 1 vez)recarregou habilidade | hab reset \n efeitos de camera são digitados aqui: pixel(para pixelizar a camera),vermelho(imagem mais avermelhada),azul(imagem mais azulada) verde(imagem mais verde) inverter(inverte as cores) escurecer normal(retira os filtros) policia(alterna entre vermelho e azul) walter(filtro laranja) noir cor(desativa o noir/ou use o normal)\nse a sessão acabou |fim da sessão\n fim do guia")
def Cam():
        explosao_cap = None
        cam = cv2.VideoCapture(0)
        explosao_cap = cv2.VideoCapture("videos/Deltarune Explosion Green Screen(720P_HD).mp4")
        #misc
        global rotacao, state
        global mana, hp, mana_max
        #p/ações especificas deste jeito p/nn bugar
        global escurecer_ativo
        global red_blue_off
        global hsv_state_red
        global hsv_state_blue
        global hsv_state_green
        global police
        global police_contador
        global walter
        global enter_pressed
        global pixelar_ativo
        global negativo_ativo
        global mostrar_explosao
        #incluso com mecanicas
        def mostrar_dado_no_frame(frame):
            global dado_atual_img, dado_atual_num
            if dado_atual_img is not None and dado_atual_num is not None:
                # Posição onde o dado vai aparecer
                x, y = 10, 10
                frame = sobrepor_imagem_fundo(frame, dado_atual_img, x, y)
                # Escreve o número do dado ao lado da imagem
                img_h, img_w = dado_atual_img.shape[:2]
                center_x = x + img_w // 2
                center_y = y + img_h // 2
                text = str(dado_atual_num)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1.5
                thickness = 3
                text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
                text_x = center_x - text_size[0] // 2
                text_y = center_y + text_size[1] // 2  # alinha pela base do texto
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
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
            # Limite para verde
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            mask = cv2.inRange(hsv, lower_green, upper_green)
            mask_inv = cv2.bitwise_not(mask)
            # Remove o fundo
            frame_video_sem_fundo = cv2.bitwise_and(frame_video, frame_video, mask=mask_inv)
            return frame_video_sem_fundo, mask_inv
        def barras_webcam(img):
            hp = fichas[ficha_esc].hp_val
            hp_max = fichas[ficha_esc].hp
            mana =  fichas[ficha_esc].esp
            mana_max = fichas[ficha_esc].esp_max
            #espessura positivo so borda negativo ocupa tudo
            espessura = -1
            cor_hp_full = (13,217,16)#bgr verde
            cor_hp_incompleto = (0, 0, 255)
            cor_mana_full = (0, 234, 255)
            cor_mana_incompleto = (254, 255, 207)#207, 255, 254
            #p/calculos
            largura = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)) #480 no meu pc
            altura = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)) #640 no meu pc
            barra_hp_max_width = int(largura - (largura / 8) - 50)
            barra_hp_min_x = 50
            barra_hp_height_y1 = int(altura - 100)
            barra_hp_height_y2 = int(altura - 50)
            #dano tbm esta aumentando a barra
            hp_ratio = max(0, min((hp / hp_max), 1.65))#1,65 por escala de dano
            hp_width = int((barra_hp_max_width - barra_hp_min_x) * hp_ratio)# barra incompleta (vermelho)
            cv2.rectangle(img, (barra_hp_min_x, barra_hp_height_y1), (barra_hp_max_width, barra_hp_height_y2), cor_hp_incompleto, -1)
            # barra atual (verde)
            cv2.rectangle(img, (barra_hp_min_x, barra_hp_height_y1), (barra_hp_min_x + hp_width, barra_hp_height_y2), cor_hp_full, -1)
            barra_mana_max_y1 = int(altura - (altura / 10))
            barra_mana_min_y = int(altura / 10)
            barra_mana_x1 = int(largura - 100)
            barra_mana_x2 = int(largura - 50)
            # proporção da mana
            mana_ratio = max(0, min(mana / mana_max, 1))
            mana_height = int((barra_mana_max_y1 - barra_mana_min_y) * mana_ratio)
            # barra incompleta (azul claro)
            cv2.rectangle(img, (barra_mana_x1, barra_mana_min_y), (barra_mana_x2, barra_mana_max_y1), cor_mana_incompleto, -1)
            # barra atual (amarelo)
            cv2.rectangle(img, (barra_mana_x1, barra_mana_max_y1 - mana_height), (barra_mana_x2, barra_mana_max_y1), cor_mana_full, -1)
            return img
        #visual
        def pixelar(img):   
            altura, largura = img.shape[:2]
            pequeno = cv2.resize(img, (32, 24),     interpolation=cv2.INTER_LINEAR)
            return cv2.resize(pequeno,  (largura, altura),   interpolation=cv2.INTER_NEAREST)
        def negativo(img):
            return cv2.bitwise_not(img)
        def escurecer(img):
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            v = (v * 0.42).clip(0, 255).astype  (np.uint8)  # reduz brilho pela   metade
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
            h,s, v = cv2.split(hsv)
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
        while True:
            validacao, frame = cam.read()
            if not validacao:
                #print("Erro ao capturar frame.")
                break
            frame = barras_webcam(frame)
            # Aplica rotação no frame original
            if rotacao == 1:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            elif rotacao == 2:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
            elif rotacao == 3:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame_display = frame.copy()
            if police and not red_blue_off:
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
                    if explosao_cap is None:
                        explosao_cap = cv2.VideoCapture("videos/Deltarune Explosion Green Screen(720P_HD).mp4")
                    ret_exp, frame_exp = explosao_cap.read()
                    if not ret_exp:
                        explosao_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        mostrar_explosao = False
                        explosao_cap.release()
                        explosao_cap = None
                    else:
                        frame_exp = cv2.resize(frame_exp, (480, 480))
                        frame_exp_sem_fundo, mask_inv = remover_fundo_verde(frame_exp)
                        x_offset, y_offset = 100, 100
                        h, w = frame_exp.shape[:2]
                        roi = frame_display[y_offset:y_offset+h, x_offset:x_offset+w]
                        mask_inv_color = cv2.merge([mask_inv, mask_inv, mask_inv])
                        bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask_inv))
                        fg = cv2.bitwise_and(frame_exp, frame_exp, mask=mask_inv)
                        combinada = cv2.add(bg, fg)
                        frame_display[y_offset:y_offset+h, x_offset:x_offset+w] = combinada

                # Aplica modo preto e branco se selecionado
            if state == 2:
                frame_display = cv2.cvtColor(frame_display, cv2.COLOR_BGR2GRAY)
                frame_display = cv2.cvtColor(frame_display, cv2.COLOR_GRAY2BGR)

            frame_display = mostrar_dado_no_frame(frame_display)
            cv2.imshow("Camera", frame_display)
            if keyboard.is_pressed('left'):
                rotacao = 3
            elif keyboard.is_pressed('up'):
                rotacao = 0
            elif keyboard.is_pressed('right'):
                rotacao = 1
            elif keyboard.is_pressed('down'):
                rotacao = 2
            # Controle das setas # estou fazendo deste jeito ´para multimplas teclas o key == nn funciona com certas teclas
            key = cv2.waitKey(1)
            if key == 27:  # esc para fechar
                print("fechando")
                exit()
                break
        cam.release()
        cv2.destroyAllWindows()
def play():
    global cam_on, rotacao, state
    global escurecer_ativo, red_blue_off
    global hsv_state_red, hsv_state_blue, hsv_state_green
    global police, police_contador, walter, enter_pressed
    global pixelar_ativo, negativo_ativo
    global valido, turnos_reviver
    global dado_atual_img, dado_atual_num 
    global mostrar_explosao
    if not cam_on:
        thread = threading.Thread(target=Cam, daemon=True)
        thread.start()
        cam_on = True
    while valido:
        act = input("\n sua ação é: ").lower()
        match act:
            case "ficha":
                fichas[ficha_esc].ficha_info()
                fichas[ficha_esc].hab_bonus()
                #efeitos camera
                #tem que arrumar conforme tamanho da camera
            case "explosao":
                mostrar_explosao = True
                print("Explosão ativada")
            case "pixel":
                pixelar_ativo = not pixelar_ativo
                print(f"Pixelar {'ativado' if pixelar_ativo else 'desativado'}")
            case "vermelho":
                hsv_state_red = True
                hsv_state_blue = hsv_state_green = False
                red_blue_off = False
                print("Filtro vermelho ativado")
            case "azul":
                hsv_state_blue = True
                hsv_state_red = hsv_state_green = False
                red_blue_off = False
                print("Filtro azul ativado")
            case "verde":
                hsv_state_green = True
                hsv_state_red = hsv_state_blue = False  
                red_blue_off = True
                print("Filtro verde ativado")
            case "inverter":
                negativo_ativo = not negativo_ativo
                print(f"Negativo {'ativado' if negativo_ativo else 'desativado'}")
            case "escurecer":
                escurecer_ativo = True
                hsv_state_red = hsv_state_blue = hsv_state_green = False
                red_blue_off = True
                print("Escurecimento ativado")
            case "normal":
                hsv_state_red = False
                hsv_state_blue = False
                hsv_state_green = False
                police = False
                walter = False
                red_blue_off = True
                dado_atual_img = None
                dado_atual_num = None
                mostrar_explosao = False
                pixelar_ativo = False
                negativo_ativo = False
                escurecer_ativo = False
                state = 1
                print("Todos os filtros desativados")
            case "policia":
                police = True
                hsv_state_red = hsv_state_blue = hsv_state_green = False
                red_blue_off = False
                print("Modo polícia ativado")
            case "walter":
                walter = True
                hsv_state_red = hsv_state_blue = hsv_state_green = False
                print("Modo Walter ativado")
            case "noir":
                state = 2
                print("Modo preto e branco ativado")
            case "cor":
                state = 1
                print("Modo colorido ativado")
                #dados
            case "d4":
                dado_atual_img = cv2.imread("imagens/d4-removebg-preview.png", cv2.IMREAD_UNCHANGED)
                dado_atual_num = Dados.d4()
                print(f"caiu: {dado_atual_num}")
            case "d6":
                dado_atual_img = cv2.imread("imagens/d6-removebg-preview.png", cv2.IMREAD_UNCHANGED)
                dado_atual_num = Dados.d6()
                print(f"caiu: {dado_atual_num}")
            case "d10":
                dado_atual_img = cv2.imread("imagens/d10-removebg-preview.png", cv2.IMREAD_UNCHANGED)
                dado_atual_num = Dados.d10()
                print(f"caiu: {dado_atual_num}")
            case "d20":
                dado_atual_img = cv2.imread("imagens/d20-removebg-preview.png", cv2.IMREAD_UNCHANGED)
                dado_atual_num = Dados.d20()
                print(f"caiu: {dado_atual_num}")
                #açoes geral/mecanicas
            case "cura":
                cura = int(input("Valor curado: "))
                fichas[ficha_esc].hp_val = min(fichas[ficha_esc].hp_val + cura, fichas[ficha_esc].hp)
                turnos_reviver = 3
                cura = None
            case "dano":
                if fichas[ficha_esc].hp_val < 1:
                    turnos_reviver -= 1
                    print("menos 1 turno para reviver")
                    print(f"HP atual: {fichas[ficha_esc].hp_val}")
                    if turnos_reviver < 1:
                        print("morreu")
                        fichas[ficha_esc].vivo = False
                else:
                    dano = int(input("Valor de dano sofrido: "))
                    fichas[ficha_esc].hp_val  -= dano
                    dano = None
                    print(f"Novo HP: {fichas[ficha_esc].hp_val}")
            case "hab usada":
                qual_hab = input("Habilidade usada: ").lower()
                hab_ficha = fichas[ficha_esc].bonus.lower()
                if qual_hab == hab_ficha:
                    qnt_usos = int(input("Usos no turno: "))
                    uso_qnt_perso = fichas[ficha_esc].bonus_usos#sem () neste caso para acessar direto o valor
                    uso_qnt_perso -= qnt_usos
                else:
                    print("não existe essa habilidade")
            case "hab reset":
                print("Usos resetados.")
            case "full restore":
                fichas[ficha_esc].restore()
                turnos_reviver = 3
                fichas[ficha_esc].esp = fichas[ficha_esc].esp_max
            case "salario":
                salario = input("digite seu ganho($): ")
                #falta isso
            case "compra":
                salario = input("digite o valor gasto: ")
                #falta isso
            case "magia":
                mana = fichas[ficha_esc].esp
                mana_max = fichas[ficha_esc].esp_max
                print(f"atualmente possui {mana}")
                uso_magia = int(input(f"digite o quanto de espirito você quer usar(máximo de {fichas[ficha_esc].esp_max}): "))
                resultado = (uso_magia-mana)
                if resultado > 0:
                    print("passou do limite")
                else:
                    print(f"foi usado {uso_magia} de espirito")
                    fichas[ficha_esc].esp -= uso_magia
                if mana > mana_max:
                    mana = mana_max
                    print(f"mana maxima({mana_max}) foi ultrapassado do limite recolocando dentro do range: {mana}")
            case "lv up":
                fichas[ficha_esc].lv_up()
            case "fim da sessão":
                print("Espero que tenha tido uma boa sessão!")
                break
    else:
        print("você morreu")
if ficha_esc in fichas:
    fichas[ficha_esc].ficha_info()
    fichas[ficha_esc].hab_bonus()
    valido = True
    instrucoes()
    jogar_valido = fichas[ficha_esc].vivo
    if jogar_valido:
        play()
    else:
        print("jogador morto")
else:
    print(f"Ficha '{ficha_esc}' não encontrada. Verifique a ortografia.")
