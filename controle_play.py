from ficha import *
from Dados import * #add na camera o resultado o que falta dos dados
import cv2
import keyboard
import numpy as np
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
def play():
    
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
