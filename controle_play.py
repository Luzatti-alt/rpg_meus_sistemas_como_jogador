from ficha import *
from Dados import * #add na camera o resultado o que falta dos dados
from camera import *#tem que fazer uma tread para o sistema e outro para a camera estudar isso
import threading #para poder rodar a camera e os inputs
ficha_esc = input("selecione a ficha: ").lower()
valido = False
#so para conseguir acessar o metodo de hab_bonus e fazer a consulta da ficha aqui
fichas = {
    "golpnur": golpnur,# obj e como ele fica aqui
    "xx": xx,
    #add outros players e seu objs(dados da ficha) n arquivo onde fica localizado as fichas e aqui do jeito que esta
}
def instrucoes():
    print("\ninstruções deste controle use somente durante combate \nver ficha | ficha \nsofreu dano | dano e dps num de dano sofrido(ex dano 5) \ncurado | vida e dps num da cura(vida 5) \nupou de nivel | lv up \nusou habilidade | hab usada dps o nome dela e por fim qnt de vezs usadas no turno ex chute 1(chute 1 vez)\nrecarregou habilidade | hab reset \nse a sessão acabou |fim da sessão\n fim do guia")
def play():
     while valido:
        Camera.connect()
        thread = threading.Thread(target=Camera.connect, daemon=True)
        thread.start()
        act = input("\n sua açõa é: ")
        #ficha aparecer elementos
        if act == "ficha":
            fichas[ficha_esc].ficha_info()
            fichas[ficha_esc].hab_bonus()
            play()
        elif act == "d4":
            print(f"caiu: {Dados.d4()}")
            play()
        elif act == "d10":
            print(f"caiu: {Dados.d10()}")
            play()
        elif act == "d20":
            print(f"caiu: {Dados.d20()}")
            play()
             #cura
        elif act == "cura":
            print("numero curado")
            cura = int(input("digite valor curado (ex: 5 de hp de cura): "))
            #add pegar valor da vida e fazer somar ou diminuir aqui para controle
            play()
        #dano
        elif act == "dano":
            print("dano sofrido")
            dano = int(input("digite valor de dano sofrido (ex: 5 de hp de dano): "))
            #add pegar valor da vida e fazer somar ou diminuir aqui para controle
            play()
        #lv up
        elif act == "lv up":
            print("level upado em sua ficha \n")
            #updatar o lv na ficha escolhida
            play()
        #usadas
        elif act == "hab usada":
            print("qual habilidade usada: ")
            qual_hab = input("qual habilidade será usada: ")
            print("quantos usos: ")
            qnt_usos = input("quantas vezes foi usada no turno: ")
            play()
        #reset
        elif act == "hab reset":
            print("num de usos das habilidades resetados")
            #add func de resetar o num das habilidades
            play()
        #invalidos
        elif act == "ficha"or"cura"or"dano"or"lv up"or"hab usada"or"hab reset"or"fim da sessão"or"d4"or"d10"or"d20":
            print("digitou algo inválido digite algo entre(por enquanto so fecha o programa)")
            instrucoes()
            play()
        #fim sessão
        elif act == "fim da sessão":
            print("espero que tenha tido uma boa sessão")
            break
        exit()
#especifica por jogador
#eu
if ficha_esc =="golpnur":
    golpnur.ficha_info()
    golpnur.hab_bonus()
    valido = True
    instrucoes()
    play()
#
elif ficha_esc == "xx":
    xx.ficha_info()
    xx.hab_bonus()
    valido = True
    instrucoes()
    play()
#geral das fichas
if ficha_esc != "golpnur" or "xx" or "a" or "b" or "c":
    print("sem ficha ainda ou ficha inválida")
    exit()
