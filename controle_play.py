from ficha import *
from Dados import * #add na camera o resultado o que falta dos dados
import cv2
import keyboard
import numpy as np
import threading #para poder rodar a camera e os inputs
ficha_esc = input("selecione a ficha: ").lower()
valido = False
cam_on = False
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
#so para conseguir acessar o metodo de hab_bonus e fazer a consulta da ficha aqui
fichas = {
    "golpnur": golpnur,# obj e como ele fica aqui
    "xx": xx,
    #add outros players e seu objs(dados da ficha) n arquivo onde fica localizado as fichas e aqui do jeito que esta
}
def instrucoes():
    print("\ninstruções deste controle use somente durante combate \nver ficha | ficha \nsofreu dano | dano e dps num de dano sofrido(ex dano 5) \ncurado | vida e dps num da cura(vida 5) \nupou de nivel | lv up \nusou habilidade | hab usada dps o nome dela e por fim qnt de vezs usadas no turno ex chute 1(chute 1 vez)\nrecarregou habilidade | hab reset \nse a sessão acabou |fim da sessão\n fim do guia")
def Cam():
        cam = cv2.VideoCapture(0)
        global rotacao
        global state
        #p/ações especificas
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
        #filtros
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
    #detectar camera
        if not cam.isOpened():
            print("Erro ao abrir a câmera.\n")
            exit()
        elif cam.isOpened():
            print("Conectada\n")
        #funções da webcam
        while True:
            validacao, frame = cam.read()
            if not validacao:
                #print("Erro ao capturar frame.")
                break
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
                # Aplica modo preto e branco se selecionado
            if state == 2:
                frame_display = cv2.cvtColor(frame_display, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Camera", frame_display)
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
    global valido
    if not cam_on:
        thread = threading.Thread(target=Cam, daemon=True)
        thread.start()
        cam_on = True
    while valido:
        act = input("\n sua ação é: ")
        if act == "ficha":
            fichas[ficha_esc].ficha_info()
            fichas[ficha_esc].hab_bonus()
            #efeitos camera
        elif act == "pixel":
            pixelar_ativo = not pixelar_ativo
            print(f"Pixelar {'ativado' if pixelar_ativo else 'desativado'}")
        elif act == "vermelho":
            hsv_state_red = True
            hsv_state_blue = hsv_state_green = False
            red_blue_off = False
            print("Filtro vermelho ativado")
        elif act == "azul":
            hsv_state_blue = True
            hsv_state_red = hsv_state_green = False
            red_blue_off = False
            print("Filtro azul ativado")
        elif act == "verde":
            hsv_state_green = True
            hsv_state_red = hsv_state_blue = False
            red_blue_off = True
            print("Filtro verde ativado")
        elif act == "inverter":
            negativo_ativo = not negativo_ativo
            print(f"Negativo {'ativado' if negativo_ativo else 'desativado'}")
        elif act == "escurecer":
            escurecer_ativo = True
            hsv_state_red = hsv_state_blue = hsv_state_green = False
            red_blue_off = True
            print("Escurecimento ativado")
        elif act == "normal":
            escurecer_ativo = pixelar_ativo = negativo_ativo = False
            hsv_state_red = hsv_state_blue = hsv_state_green = police = walter = False
            red_blue_off = True
            state = 1
            print("Todos os filtros desativados")
        elif act == "police":
            police = True
            hsv_state_red = hsv_state_blue = hsv_state_green = False
            red_blue_off = False
            print("Modo polícia ativado")
        elif act == "walter":
            walter = True
            hsv_state_red = hsv_state_blue = hsv_state_green = False
            print("Modo Walter ativado")
        elif act == "bw":
            state = 2
            print("Modo preto e branco ativado")
        elif act == "cor":
            state = 1
            print("Modo colorido ativado")
            #dados
        elif act == "d4":
            print(f"caiu: {Dados.d4()}")
        elif act == "d10":
            print(f"caiu: {Dados.d10()}")
        elif act == "d20":
            print(f"caiu: {Dados.d20()}")
            #açoes geral
        elif act == "cura":
            cura = int(input("Valor curado: "))
            # Adicione lógica de aumento de vida
        elif act == "dano":
            dano = int(input("Valor de dano sofrido: "))
            # Adicione lógica de redução de vida
        elif act == "lv up":
            print("Level upado.")
            #logica aumentar o lv
        elif act == "hab usada":
            qual_hab = input("Habilidade usada: ")
            qnt_usos = input("Usos no turno: ")
            # Adicione lógica de uso
        elif act == "hab reset":
            print("Usos resetados.")
            # Adicione lógica de reset
        elif act == "fim da sessão":
            print("Espero que tenha tido uma boa sessão!")
            break
#especifica por jogador
#eu
if ficha_esc =="golpnur":
    golpnur.ficha_info()
    golpnur.hab_bonus()
    valido = True
    instrucoes()
    play()
#outros personagem
elif ficha_esc == "xx":
    xx.ficha_info()
    xx.hab_bonus()
    valido = True
    instrucoes()
    play()
#geral das fichas
