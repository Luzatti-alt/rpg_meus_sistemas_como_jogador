from ficha_db import *
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

class rpg_app(App):
    def build(self):
        altura = Window.height
        largura = Window.width

        layout = FloatLayout()

        # Fundo
        with layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  
            self.bg_rect = Rectangle(size=Window.size, pos=layout.pos)

        # Atualizar fundo quando redimensionar
        def update_bg(*args):
            self.bg_rect.pos = layout.pos
            self.bg_rect.size = Window.size
        layout.bind(pos=update_bg, size=update_bg)
        #elementos visuai/ indormativoss do app
        #info/log de ações feitas
        #log=rectangle()#con scrool (x range 300 ~ 500)
        # Botões 
        self.criar_ficha = Button(
            text='Criar ficha',
            size_hint=(None, None),
            size=(300, 100),
            background_normal="",
            background_color=(0.2, 0.6, 0.9, 1),
            pos=(0,altura-100)
        )
        #dados
        self.d4 = Button(
        text='d4',
        size_hint=(None, None),
        size=(150, 100),
        background_normal="",
        background_color=(0.2, 0.6, 0.9, 1),
        pos=(0, altura / 2 +325)
        )
        self.d6 = Button(
        text='d6',
        size_hint=(None, None),
        size=(150, 100),
        background_normal="",
        background_color=(0.2, 0.6, 0.9, 1),
        pos=(0, altura / 2+225)
        )
        self.d10 = Button(
        text='d10',
        size_hint=(None, None),
        size=(150, 100),
        background_normal="",
        background_color=(0.2, 0.6, 0.9, 1),
        pos=(150, altura / 2+225)
        )
        self.d20 = Button(
        text='d20',
        size_hint=(None, None),
        size=(150, 100),
        background_normal="",
        background_color=(0.2, 0.6, 0.9, 1),
        pos=(150, altura / 2+325)
        )
        #camera
        self.efeitos = Spinner(text='Efeito a ser aplicado',
            values=('desativar','normal','vermelho', 'verde', 'azul', 'policia' ,'noir', 'laranja', 'invertido' ,'escurecido', 'explosao'),
            size_hint=(None, None),
            size=(300, 100),
            pos=(0, altura/2+125))
        self.up = Button(
        text='cima',
        size_hint=(None, None),
        size=(150, 100),
        background_normal="",
        background_color=(0.2, 0.6, 0.9, 1),
        pos=(0, 100)
        )
        self.down = Button(
        text='baixo',
        size_hint=(None, None),
        size=(150, 100),
        background_normal="",
        background_color=(0.2, 0.6, 0.9, 1),
        pos=(0, 0)
        )
        self.esquerda = Button(
        text='esquerda',
        size_hint=(None, None),
        size=(150, 100),
        background_normal="",
        background_color=(0.2, 0.6, 0.9, 1),
        pos=(150, 0)
        )
        self.direita = Button(
        text='direita',
        size_hint=(None, None),
        size=(150, 100),
        background_normal="",
        background_color=(0.2, 0.6, 0.9, 1),
        pos=(150, 100)
        )
        self.aplicar_efeito= Button(
        text='Aplicar efeito',
        size_hint=(None, None),
        size=(300, 100),
        background_normal="",
        background_color=(0.2, 0.6, 0.9, 1),
        pos=(0, altura/2+25)
        ) 
        #adicionando
        layout.add_widget(self.criar_ficha)
        layout.add_widget(self.d4)
        layout.add_widget(self.d6)
        layout.add_widget(self.d10)
        layout.add_widget(self.d20)
        layout.add_widget(self.up)
        layout.add_widget(self.down)
        layout.add_widget(self.direita)
        layout.add_widget(self.esquerda)
        layout.add_widget(self.aplicar_efeito)
        layout.add_widget(self.efeitos)
        # Reposicionar elementos quando mudar tamanho
        def reposicionar_elementos(*args):
            altura = Window.height
            self.criar_ficha.pos = (0, altura-100)
            self.efeitos.pos=(0, altura/2+125)
            self.aplicar_efeito.pos=(0, altura/2+25)
            self.d4.pos=(0, altura / 2+325)
            self.d6.pos=(0, altura / 2+225)
            self.d10.pos=(150, altura / 2+225)
            self.d20.pos=(150, altura / 2+325)
        Window.bind(size=reposicionar_elementos)

        # Ação do botão
        self.criar_ficha.bind(on_release=lambda x: print("Botão Criar Ficha clicado!"))
        self.d4.bind(on_release=lambda x: print("Botão d4"))
        self.d6.bind(on_release=lambda x: print("Botão d6"))
        self.d10.bind(on_release=lambda x: print("Botão d10"))
        self.d20.bind(on_release=lambda x: print("Botão d20"))
        self.up.bind(on_release=lambda x: print("cima"))
        self.down.bind(on_release=lambda x: print("baixo"))
        self.direita.bind(on_release=lambda x: print("diriuta"))
        self.esquerda.bind(on_release=lambda x: print("esquerda"))
        return layout

rpg_app().run()