from ficha import *
from Dados import * #so chamar o metodo ali e ja faz a rolagem e ver como add na camera
ficha_esc = input("selecione a ficha: ").lower()
valido = False
#so para conseguir acessar o metodo de hab_bonus e fazer a consulta da ficha aqui
fichas = {
    "golpnur": golpnur,
    "xx": xx,
    #add outros players e seu objs ficha deito aqui e do outro jeito que ta no outro
}
def instrucoes():
    print("\ninstruções deste controle use somente durante combate \nver ficha | ficha \nsofreu dano | dano e dps num de dano sofrido(ex dano 5) \ncurado | vida e dps num da cura(vida 5) \nupou de nivel | lv up \nusou habilidade | hab usada dps o nome dela e por fim qnt de vezs usadas no turno ex chute 1(chute 1 vez)\nrecarregou habilidade | hab reset \nse a sessão acabou |fim da sessão\n fim do guia")
def play():
     while valido:
        act = input("\n sua açõa é: ")
        #ficha
        if act == "ficha":
            fichas[ficha_esc].ficha_info()
            fichas[ficha_esc].hab_bonus()
            play()
            #dados
        elif act == "d4":
            print(f"caiu: {Dados.d4()}")
        elif act == "d10":
            print(f"caiu: {Dados.d10()}")
        elif act == "d20":
            print(f"caiu: {Dados.d20()}")
             #cura
        elif act == "cura":
            print("numero curado")
            cura = int(input("digite valor curado (ex: 5 de hp de cura): "))
            #add pegar valor da vida e fazer somar ou diminuir aqui para melhora
            play()
        #dano
        elif act == "dano":
            print("dano sofrido")
            dano = int(input("digite valor de dano sofrido (ex: 5 de hp de dano): "))
            #add pegar valor da vida e fazer somar ou diminuir aqui para melhora
            play()
        #lv up
        elif act == "lv up":
            print("level upado em sua ficha \n")
            play()
        #usadas
        elif act == "hab usada":
            print("qual habilidade usada: ")
            qual_hab = input("")
            print("quantos usos: ")
            qnt_usos = input("")
            play()
        #reset
        elif act == "hab reset":
            print("num de usos das habilidades resetados")
            #add func de resetar o num das habilidades
            play()
        #invalidos
        elif act == "ficha"or"cura"or"dano"or"lv up"or"hab usada"or"hab reset"or"fim da sessão"or"d10":
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
if ficha_esc != "golpnur" or "xx" or "a" or "b" or "c":
    print("sem ficha ainda ou ficha inválida")
    exit()
