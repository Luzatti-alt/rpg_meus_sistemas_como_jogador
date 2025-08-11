from ficha_db import *
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
class rpg_app(App):
    def build(self):
        altura = Window.height
        largura = Window.width
        layout = FloatLayout()
        # Fundo geral
        with layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.bg_rect = Rectangle(size=Window.size, pos=layout.pos)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        # Área de log
        self.log_layout = GridLayout(cols=1, size_hint_y=None, spacing=5, padding=5)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        largura_log = 300
        self.scroll_log = ScrollView(
            size_hint=(None, None),
            size=(largura_log, altura - 15),
            pos=(largura - largura_log - 10, 10),
            bar_width=10
        )
        with self.scroll_log.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.log_bg = Rectangle(size=self.scroll_log.size, pos=self.scroll_log.pos)
        self.scroll_log.bind(pos=self.update_log_bg, size=self.update_log_bg)
        self.scroll_log.add_widget(self.log_layout)
        layout.add_widget(self.scroll_log)
        # Função para adicionar mensagens no log
        def add_log(msg):
            log_label = Label(
                text=msg,
                size_hint_y=None,
                height=60,
                color=(1, 1, 1, 1),
                halign="left",
                valign="middle"
            )
            log_label.bind(size=lambda *x: log_label.setter('text_size')(log_label, (log_label.width, None)))
            self.log_layout.add_widget(log_label)
            self.scroll_log.scroll_y = 0
        # === ÁREA CENTRAL ===
        central_box = BoxLayout(
        orientation='vertical',
        size_hint=(None, None),
        size=(largura - largura_log - 650, altura - 20),
        pos=(460, 10),
        spacing=10
        )
        # ===================== CAIXA VERDE (CAM) =====================
        cam_widget = FloatLayout(size_hint_y=0.8)
        with cam_widget.canvas:
            Color(0, 1, 0, 1)
            self.cam_rect = Rectangle(size=cam_widget.size, pos=cam_widget.pos)
        cam_widget.bind(size=self.update_cam_rect, pos=self.update_cam_rect)
        # ===================== CAMPO DE TEXTO =====================
        input_text = TextInput(
        hint_text="Digite aqui...",
        size_hint_y=0.2
        )
        # Adiciona os dois no central_box
        central_box.add_widget(cam_widget)
        central_box.add_widget(input_text)
        layout.add_widget(central_box)
        # Botões e spinner
        self.criar_ficha = Button(text='Criar ficha', size_hint=(None, None), size=(300, 100),
                                  background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                                  pos=(0, altura - 100))
        self.d4 = Button(text='d4', size_hint=(None, None), size=(150, 100),
                         background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                         pos=(0, altura / 2 + 325))
        self.d6 = Button(text='d6', size_hint=(None, None), size=(150, 100),
                         background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                         pos=(0, altura / 2 + 225))
        self.d10 = Button(text='d10', size_hint=(None, None), size=(150, 100),
                          background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                          pos=(150, altura / 2 + 225))
        self.d20 = Button(text='d20', size_hint=(None, None), size=(150, 100),
                          background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                          pos=(150, altura / 2 + 325))
        self.cura = Button(text='cura', size_hint=(None, None), size=(150, 100),
                           background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                           pos=(150, altura / 2 - 75))
        self.dano = Button(text='Dano', size_hint=(None, None), size=(150, 100),
                           background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                           pos=(0, altura / 2 - 75))
        self.efeitos = Spinner(
            text='Efeito a ser aplicado',
            values=('desativar', 'normal', 'vermelho', 'verde', 'azul', 'policia',
                    'noir', 'laranja', 'invertido', 'escurecido', 'explosao', 'pixelar'),
            size_hint=(None, None),
            size=(300, 100),
            pos=(0, altura / 2 + 125)
        )
        self.up = Button(text='cima', size_hint=(None, None), size=(150, 100),
                         background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                         pos=(0, 100))
        self.down = Button(text='baixo', size_hint=(None, None), size=(150, 100),
                           background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                           pos=(0, 0))
        self.esquerda = Button(text='esquerda', size_hint=(None, None), size=(150, 100),
                               background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                               pos=(150, 0))
        self.direita = Button(text='direita', size_hint=(None, None), size=(150, 100),
                              background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                              pos=(150, 100))
        self.aplicar_efeito = Button(text='Aplicar efeito', size_hint=(None, None), size=(300, 100),
                                     background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                                     pos=(0, altura / 2 + 25))
        for widget in [self.criar_ficha, self.d4, self.d6, self.d10, self.d20,
                       self.up, self.down, self.direita, self.esquerda,
                       self.aplicar_efeito, self.efeitos, self.dano, self.cura]:
            layout.add_widget(widget)
        # Ações dos botões com log
        self.criar_ficha.bind(on_release=lambda x: add_log("Criar Ficha clicado"))
        self.d4.bind(on_release=lambda x: add_log("Rolou um d4"))
        self.d6.bind(on_release=lambda x: add_log("Rolou um d6"))
        self.d10.bind(on_release=lambda x: add_log("Rolou um d10"))
        self.d20.bind(on_release=lambda x: add_log("Rolou um d20"))
        self.up.bind(on_release=lambda x: add_log("Movendo para cima"))
        self.down.bind(on_release=lambda x: add_log("Movendo para baixo"))
        self.direita.bind(on_release=lambda x: add_log("Movendo para direita"))
        self.esquerda.bind(on_release=lambda x: add_log("Movendo para esquerda"))
        self.aplicar_efeito.bind(on_release=lambda x: add_log(f"Efeito aplicado: {self.efeitos.text}"))
        self.cura.bind(on_release=lambda x: add_log("Curando"))
        self.dano.bind(on_release=lambda x: add_log("Causando dano"))
        return layout
    def update_bg(self, *args):
        self.bg_rect.pos = (0, 0)
        self.bg_rect.size = Window.size
    def update_log_bg(self, *args):
        self.log_bg.pos = self.scroll_log.pos
        self.log_bg.size = self.scroll_log.size
    def update_cam_rect(self, instance, value):
        self.cam_rect.pos = instance.pos
        self.cam_rect.size = instance.size
rpg_app().run()