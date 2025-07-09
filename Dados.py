import random
class Dados:
    tipo = input("Digite o dados que será jogado(como d+num): ")
    def d10():
        return random.randint(1,10)
    def d20():
        return random.randint(1,20)
    def d4():
        return random.randint(1,4)
    if tipo == "d10":
        print("caiu: ", d10())
    elif tipo == "d20":
        print("caiu: ", d20())
    elif tipo == "d4":
        print("caiu: ", d4())