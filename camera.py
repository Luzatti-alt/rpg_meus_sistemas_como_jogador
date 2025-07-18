import cv2
import keyboard
import numpy as np
import threading
class Camera:
    def connect():
        cam = cv2.VideoCapture(0)
        rotacao = 0
        state = 1
        #p/ações especificas
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
        solarizar_ativo = False
        negativo_ativo = False
        #filtros
        def pixelar(img):   
            altura, largura = img.shape[:2]
            pequeno = cv2.resize(img, (32, 24),     interpolation=cv2.INTER_LINEAR)
            return cv2.resize(pequeno,  (largura, altura),   interpolation=cv2.INTER_NEAREST)
        def solarizar(img):
         return cv2.max(img, 255 - img)
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
        def walter(img):
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            h[:] = 10
            s = cv2.add(s, 50)
            s = np.clip(s, 60, 255).astype(np.uint8)
            hsv_mod = cv2.merge([h, s, v])
            return cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)
    #detectar camera
        if not cam.isOpened():
            print("Erro ao abrir a câmera.")
            exit()
        elif cam.isOpened():
            print("Conectada")
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
            # Cria uma cópia para exibir e aplicar efeitos
            frame_display = frame.copy()
            # Aplica filtros em cadeia
            if police and not red_blue_off:
                police_contador += 1
                if police_contador % 30 < 15:
                    frame_display = vermelho(frame_display)
                else:
                    frame_display = azul(frame_display)
            else:
                # Aplica filtro vermelho
                if hsv_state_red and not red_blue_off:
                    frame_display = vermelho(frame_display)
                # Aplica filtro azul
                if hsv_state_blue and not red_blue_off:
                    frame_display = azul(frame_display)
                # Aplica filtro verde
                if hsv_state_green:
                    frame_display = verde(frame_display)
                # Aplica filtro walter
                if walter:
                    frame_display = walter(frame_display)
                if pixelar_ativo:
                    frame_display = pixelar(frame_display)
                if solarizar_ativo:
                    frame_display = solarizar(frame_display)
                if negativo_ativo:
                    frame_display = negativo(frame_display)
                if escurecer_ativo:
                    frame_display = escurecer(frame_display)
                # Aplica modo preto e branco se selecionado
            if state == 2:
                frame_display = cv2.cvtColor(frame_display, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Camera", frame_display)
            # Controle das setas # estou fazendo deste jeito ´para multimplas teclas o key == nn funciona com certas teclas
            if keyboard.is_pressed('left'):
                print("esquerda")
                rotacao = 3
            elif keyboard.is_pressed('up'):
                print("cima")
                rotacao = 0
            elif keyboard.is_pressed('right'):
                print("direita")
                rotacao = 1
            elif keyboard.is_pressed('down'):
                print("baixo")
                rotacao = 2
            key = cv2.waitKey(1) & 0xFF  # captura tecla
            if key not in [ord('r'), ord('b'), ord('p'), 255]:  # 255 = nenhuma tecla
                police = False
                hsv_state_blue = False
                hsv_state_red = False
                red_blue_off = True
                escurecer_ativo = False
                pixelar_ativo = False
                solarizar_ativo = False
                negativo_ativo = False
            # Debounce Enter(evitar lag e mudar somente quando apertar e nn precionar)
            if key == 13:  # enter
                if not enter_pressed:
                    if state == 2:
                        state = 1
                    else:
                        state = 2
                    print(f"Modo: {'Preto e Branco' if state == 2 else 'Colorido'}")
                    enter_pressed = True
                    hsv_state_red = False
                    hsv_state_blue = False
                    hsv_state_green = False
                    police = False
                    walter = False
                    escurecer_ativo = False
                    pixelar_ativo = False
                    solarizar_ativo = False
                    negativo_ativo = False
            else:
                enter_pressed = False
            #modo vermelho
            if keyboard.is_pressed('r'):
                hsv_state_red = True
                hsv_state_blue = False
                hsv_state_green = False
                red_blue_off = False
                escurecer_ativo = False
                police = False
                walter = False
                pixelar_ativo = False
                solarizar_ativo = False
                negativo_ativo = False
            if keyboard.is_pressed('b'):
                hsv_state_blue = True
                hsv_state_red = False
                red_blue_off = False
                police = False
                hsv_state_green = False
                escurecer_ativo = False
                walter = False
                pixelar_ativo = False
                solarizar_ativo = False
                negativo_ativo = False
            if keyboard.is_pressed('g'):
                hsv_state_blue = False
                hsv_state_red = False
                red_blue_off = True
                police = False
                hsv_state_green = True
                escurecer_ativo = False
                walter = False
                pixelar_ativo = False
                solarizar_ativo = False
                negativo_ativo = False
            if keyboard.is_pressed('n'):
                hsv_state_blue = False
                hsv_state_red = False
                hsv_state_green = False
                police = False
                walter = False
                escurecer_ativo = False
                state = 0
                pixelar_ativo = False
                solarizar_ativo = False
                negativo_ativo = False
            if keyboard.is_pressed('w'):
                hsv_state_blue = False
                hsv_state_red = False
                hsv_state_green = False
                police = False
                walter = True
                escurecer_ativo = False
                pixelar_ativo = False
                solarizar_ativo = False
                negativo_ativo = False
            if keyboard.is_pressed('p'):
                hsv_state_blue = False
                hsv_state_red = False
                hsv_state_green = False
                walter = False
                police = True
                police_contador = 0  # Resetar o contador aqui
                red_blue_off = False  # Ativar modo de cor para o police funcionar
                pixelar_ativo = False
                solarizar_ativo = False
                negativo_ativo = False
                escurecer_ativo = False
            if keyboard.is_pressed('e'):
                hsv_state_blue = False
                hsv_state_red = False
                hsv_state_green = False
                walter = False
                police = False
                red_blue_off = True
                escurecer_ativo = True
                pixelar_ativo = False
                solarizar_ativo = False
                negativo_ativo = False
            if keyboard.is_pressed('a'):
                hsv_state_blue = False
                hsv_state_red = False
                hsv_state_green = False
                walter = False
                police = False
                red_blue_off = True
                escurecer_ativo = False
                pixelar_ativo = True    
                solarizar_ativo = False
                negativo_ativo = False
            if keyboard.is_pressed('i'):
                hsv_state_blue = False
                hsv_state_red = False
                hsv_state_green = False
                walter = False
                police = False
                red_blue_off = True
                escurecer_ativo = False
                pixelar_ativo = False
                solarizar_ativo = False
                negativo_ativo = True
            if key == 27:  # esc para fechar
                print("fechando")
                exit()
                break
        cam.release()
        cv2.destroyAllWindows()
if __name__ == "__main__":#nn iniciar a camera em outro qnd rodar na hora
    thread = threading.Thread(target=Camera.connect)
    thread.start()
