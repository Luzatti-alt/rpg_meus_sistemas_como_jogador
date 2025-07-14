class Ficha:
    def __init__ (self,nome_char:str,lv:int,hp:int,hp_val:int,hpb:int,armour:int,mare:int,ca:int,mv_p:int,mv_t:int,esquiva_p:int,esquiva_t:int,dinheiro:int,esp:int,esp_max:int,vivo:bool, bonus: str, bonus_usos: int)->None:
        #__init__ atribuir valores(self(obj),nome:str(nome que é do tipo string),lv:int,etc) ->(retorna) none(nn precisa add: return ______)
        #uso de self para multiplos que usam a mesma classe nome(self/this/instance) : classe = ...
        #esta parte é mais para dados
        self.nome_char = nome_char #nome personagem
        self.lv = lv #level atual
        self.hp = hp #hp atual
        self.hp_val = hp_val #valor do hp
        if hp_val==0:
            vivo = False
        else:
            vivo = True
        self.hpb = hpb #hpb(ver com o miguel esta sigla)
        self.armour = armour #armadura
        self.mare = mare #mare(ver com o miguel esta sigla)
        self.ca = ca # ca(ver com o miguel esta sigla)
        self.mv_p = mv_p #movimento padrão(ver a diferença)
        self.mv_t = mv_t #movimento total(ver a diferença)
        self.esquiva_p = esquiva_p#esquiva padrão(ver a diferença)
        self.esquiva_t = esquiva_t#esquiva total(ver a diferença)
        self.dinheiro = dinheiro#dinheiro
        self.esp = esp #mana
        self.esp_max = esp_max #mana max
        self.vivo :bool = True
        self.bonus = bonus #nome da habilidade bonus
        self.bonus_usos = bonus_usos # qnts usos restantes 
    #exemplo do uso da classe
    def ficha_info (self) -> None:
        print(f"nome: {self.nome_char}")
        print(f"level: {self.lv}")
        print(f"hp: {self.hp}")
        print(f"hpb: {self.hpb}")
        print(f"armour: {self.armour}")
        print(f"mare: {self.mare}")
        print(f"ca: {self.ca}")
        print(f"movimento padrão: {self.mv_p}")
        print(f"movimento total: {self.mv_t}")
        print(f"esquiva padrão: {self.esquiva_p}")
        print(f"esquiva total: {self.esquiva_t}")
        print(f"dinheiro $: {self.dinheiro}")
        print(f"vivo: {self.vivo}")
    def hab_bonus (self) -> None:
        print(f"sua habilidade bonus: {self.bonus}")
        print(f"sua quantidade de habilidade bonus restantes: {self.bonus_usos}")
    def lv_up(self) -> None:
        self.lv += 1
        print(f"level de {self.nome_char} upado: {self.lv}")
    def restore(self)->None:
        self.hp = self.hp_val
        print("teste: ",self.hp_val)
        print("dano aplicado a ficha: ",self.hp_val)
#aqui se atribui valoras aos personagens
#exemplo hp 11 hp_atual 7 
golpnur : Ficha = Ficha("Golpnur",1,7,11,0,0,0,7,65,65,0,1,5,42,42,True,"gusparada de tinta", 3)#fazer em minusculo para ajudar em criar o controle
xx : Ficha = Ficha("xx",1,7,0,0,0,7,7,765,65,0,1,5,42,42,True,"mvp", 3)
#obj.metodo executar um def(parametro(tipo de dados)) interno da classe com esse nome ex:
#pedir ficha
