from ficha_db import *
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

class TelaCriarFicha(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Campos que o usuário preenche  
        self.nome_personagem = TextInput(hint_text="Nome do personagem", size_hint=(0.4, None), height=40, pos_hint={"x": 0.05, "top": 0.95})
        self.hp_total = TextInput(hint_text="HP total", size_hint=(0.4, None), height=40, pos_hint={"x": 0.05, "top": 0.88})
        self.level = TextInput(hint_text="Level", size_hint=(0.4, None), height=40, pos_hint={"x": 0.05, "top": 0.81})
        self.xp = TextInput(hint_text="XP", size_hint=(0.4, None), height=40, pos_hint={"x": 0.05, "top": 0.74})
        self.armour_hp = TextInput(hint_text="Dhb (vida bônus por armadura)", size_hint=(0.4, None), height=40, pos_hint={"x": 0.05, "top": 0.67})
        self.armadura = TextInput(hint_text="Armadura", size_hint=(0.4, None), height=40, pos_hint={"x": 0.05, "top": 0.60})
        self.mare = TextInput(hint_text="Mare (resistência mágica)", size_hint=(0.4, None), height=40, pos_hint={"x": 0.05, "top": 0.53})
        self.classe_armadura = TextInput(hint_text="Classe de armadura", size_hint=(0.4, None), height=40, pos_hint={"x": 0.05, "top": 0.46})
        self.movimento_padrao = TextInput(hint_text="Movimento padrão", size_hint=(0.4, None), height=40, pos_hint={"x": 0.05, "top": 0.39})

        self.movimento_total = TextInput(hint_text="Movimento total", size_hint=(0.4, None), height=40, pos_hint={"x": 0.55, "top": 0.95})
        self.esquiva_padrao = TextInput(hint_text="Esquiva padrão", size_hint=(0.4, None), height=40, pos_hint={"x": 0.55, "top": 0.88})
        self.esquiva_total = TextInput(hint_text="Esquiva total", size_hint=(0.4, None), height=40, pos_hint={"x": 0.55, "top": 0.81})
        self.dinheiro = TextInput(hint_text="Dinheiro", size_hint=(0.4, None), height=40, pos_hint={"x": 0.55, "top": 0.74})
        self.mana_max = TextInput(hint_text="Mana máxima", size_hint=(0.4, None), height=40, pos_hint={"x": 0.55, "top": 0.67})
        self.hab_principal = TextInput(hint_text="Habilidade principal", size_hint=(0.4, None), height=40, pos_hint={"x": 0.55, "top": 0.60})
        self.hab_principal_qnt_uso = TextInput(hint_text="Usos da habilidade principal", size_hint=(0.4, None), height=40, pos_hint={"x": 0.55, "top": 0.53})
        self.hab_bonus = TextInput(hint_text="Habilidade bônus", size_hint=(0.4, None), height=40, pos_hint={"x": 0.55, "top": 0.46})
        self.hab_bonus_qnt_uso = TextInput(hint_text="Usos da habilidade bônus", size_hint=(0.4, None), height=40, pos_hint={"x": 0.55, "top": 0.39})

        self.passiva = TextInput(hint_text="Passiva", size_hint=(0.4, None), height=40, pos_hint={"x": 0.3, "top": 0.32})

        # Adiciona os campos ao layout  
        campos = [  
            self.nome_personagem, self.hp_total, self.level, self.xp, self.armour_hp,  
            self.armadura, self.mare, self.classe_armadura, self.movimento_padrao,  
            self.movimento_total, self.esquiva_padrao, self.esquiva_total, self.dinheiro,  
            self.mana_max, self.hab_principal, self.hab_principal_qnt_uso, self.hab_bonus,  
            self.hab_bonus_qnt_uso, self.passiva  
        ]  
        for campo in campos:  
            layout.add_widget(campo)  
         
        # Botão de criar ficha  
        btn_criar = Button(text="Criar ficha", size_hint=(None, None), size=(120, 50), pos_hint={"right": 0.98, "y": 0.02})  
        btn_criar.bind(on_release=lambda x: self.salvar_ficha(campos))  
        layout.add_widget(btn_criar)
        btn_retornar = Button(text="voltar", size_hint=(None, None), size=(120, 50), pos_hint={"left": 0.98, "y": 0.02})  
        btn_retornar.bind(on_release=lambda x: setattr(self.manager, "current", "principal"))  
        layout.add_widget(btn_retornar)  

        self.add_widget(layout)  

    def salvar_ficha(self, campos):  
        # Verifica se todos os campos obrigatórios estão preenchidos  
        for campo in campos:  
            if not campo.text.strip():  
                print("Preencha todos os campos!")  
                return  

        try:
            ficha = Ficha(  
                nome_personagem=self.nome_personagem.text,  
                hp_total=int(self.hp_total.text),  
                hp_atual=int(self.hp_total.text),  # começa cheio  
                vivo=True,  
                level=int(self.level.text),  
                xp=int(self.xp.text),  
                armour_hp=int(self.armour_hp.text),  
                armadura=int(self.armadura.text),  
                mare=int(self.mare.text),  
                classe_armadura=int(self.classe_armadura.text),  
                movimento_padrao=int(self.movimento_padrao.text),  
                movimento_total=int(self.movimento_total.text),  
                esquiva_padrao=int(self.esquiva_padrao.text),  
                esquiva_total=int(self.esquiva_total.text),  
                dinheiro=int(self.dinheiro.text),  
                mana_atual=int(self.mana_max.text),  # começa cheia  
                mana_max=int(self.mana_max.text),  
                hab_principal=self.hab_principal.text,  
                hab_principal_qnt_uso=int(self.hab_principal_qnt_uso.text),  
                hab_principal_qnt_usada=0,  
                hab_bonus=self.hab_bonus.text,  
                hab_bonus_qnt_uso=int(self.hab_bonus_qnt_uso.text),  
                hab_bonus_qnt_usada=0,  
                passiva=self.passiva.text  
            )  
        except ValueError:
            print("Erro: preencha os campos numéricos corretamente!")
            return

        session.add(ficha)  
        session.commit()  
        print("Ficha criada com sucesso!")