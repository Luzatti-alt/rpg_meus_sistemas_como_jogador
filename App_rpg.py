from ficha_db import *
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

class rpg_app(App):
    def build(self):
        altura = Window.height
        largura = Window.width
        layout = FloatLayout()

        # Fundo colorido
        with layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # cinza escuro
            self.bg_rect = Rectangle(size=Window.size, pos=layout.pos)

        # Atualizar fundo ao redimensionar
        def update_bg(*args):
            self.bg_rect.pos = layout.pos
            self.bg_rect.size = Window.size
        layout.bind(pos=update_bg, size=update_bg)

        # Botão criar ficha
        self.criar_ficha = Button(
            text='Criar ficha',
            size_hint=(None, None),
            size=(300, 100),
            background_normal="",
            background_color=(0.2, 0.6, 0.9, 1),
            pos=(0, altura / 2 + 200)
        )
        #interagir com câmera(adicionar dps)
        layout.add_widget(self.criar_ficha)

        # Função ao clicar (jeito atual e temporario])
        self.criar_ficha.bind(on_release=lambda x: print("Criar ficha clicado!"))

        # Reposicionar elementos ao redimensionar
        def reposicionar_elementos(*args):
            altura = Window.height
            self.criar_ficha.pos = (0, altura / 2 + 200)
        Window.bind(size=reposicionar_elementos)

        return layout

rpg_app().run()