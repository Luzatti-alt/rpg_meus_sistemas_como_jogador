import random
class Dados:
    def d4():
        return random.randint(1,4)
    def d6():
        return random.randint(1,6)
    def d10():
        return random.randint(1,10)
    def d20():
        return random.randint(1,20)
    if __name__ == "__main__":#so roda esta parte se ele for neste aquivo este é o uso de __name == "__main__"
        tipo = input("Digite o dados que será jogado(como d+num): ")
        if tipo == "d10":
            print("caiu: ", d10())
        elif tipo == "d20":
            print("caiu: ", d20())
        elif tipo == "d4":
            print("caiu: ", d4())
