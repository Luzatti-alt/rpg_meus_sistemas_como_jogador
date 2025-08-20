from ficha_db import *
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import camera
from ficha_db import session, Ficha
from camera import *
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
from kivy.uix.screenmanager import Screen
# Importa a função que aplica o filtro diretamente do arquivo camera.py
from camera import aplicar_filtro

class TelaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

        def rolar_e_logar(tipo_dado):
            resultado = rolar_dado(tipo_dado)
            add_log(resultado)
        # === ÁREA CENTRAL ===
        # ===================== CAIXA VERDE (CAM) =====================
        self.cam_view = Image(allow_stretch=True, keep_ratio=False,size_hint=(None,None))
        Clock.schedule_interval(self.update_cam_frame, 1/30)  # ~30 FPS
        # ===================== CAMPO DE TEXTO =====================
        self.input_text = TextInput(
            hint_text="Digite aqui...",
            size_hint=(None, None),
            size=((largura - 750)/2, 80)
        )
        self.ip_text = TextInput(
        hint_text="IP:",
        size_hint=(None, None),
        size=((largura - 750)/2-6, 132),
        pos=((largura/2)-10, 10)
        )
        self.confirmar = Button(text='Confirmar', size_hint=(None, None), size=((largura - 750)/2, 80),
                                  background_normal="", background_color=(0.2, 0.6, 0.9, 1),
                                  pos=(0, altura - 100))
        # Adiciona os dois no central_box
        layout.add_widget(self.cam_view)
        layout.add_widget(self.ip_text)
        layout.add_widget(self.input_text)
        layout.add_widget(self.confirmar)
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
            pos= (0, altura / 2 + 125)
            )
        nomes_personagens_tuplas = session.query(Ficha.nome_personagem).all()
        nomes_personagens_lista = [nome[0] for nome in nomes_personagens_tuplas]
        self.personagem = Spinner(
            text='personagem',
            values=(nomes_personagens_lista),
            size_hint=(None, None),
            size=(300, 100),
            pos= (0, altura / 2 + 125)
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
                       self.aplicar_efeito, self.efeitos,self.personagem, self.dano, self.cura]:
            layout.add_widget(widget)
        # Ações dos botões com log
        self.criar_ficha.bind(on_release=lambda x: setattr(self.manager, "current", "criar_ficha"))
        self.d4.bind(on_release=lambda x: rolar_e_logar('d4'))
        self.d6.bind(on_release=lambda x: rolar_e_logar('d6'))
        self.d10.bind(on_release=lambda x: rolar_e_logar('d10'))
        self.d20.bind(on_release=lambda x: rolar_e_logar('d20'))
        self.up.bind(on_release=lambda x: (add_log("Movendo para cima"), rotacionar_camera('cima')))
        self.down.bind(on_release=lambda x: (add_log("Movendo para baixo"), rotacionar_camera('baixo'))) 
        self.direita.bind(on_release=lambda x: (add_log("Movendo para direita"), rotacionar_camera('direita')))
        self.esquerda.bind(on_release=lambda x: (add_log("Movendo para esquerda"), rotacionar_camera('esquerda')))

        # Ação do botão "Aplicar efeito" agora chama a função do camera.py
        self.aplicar_efeito.bind(on_release=lambda x: (aplicar_filtro(self.efeitos.text), add_log(f"Efeito aplicado: {self.efeitos.text}")))
        self.cura.bind(on_release=lambda x: add_log("Curando"))
        self.dano.bind(on_release=lambda x: add_log("Causando dano"))
        self.personagem.bind(text=self.atualizar_hp_personagem)
        self.add_widget(layout)
        Window.bind(on_resize=self.reposicionar_elementos)
        self.reposicionar_elementos()
    def atualizar_hp_personagem(self, spinner, text):
            ficha = session.query(Ficha).filter_by(nome_personagem=text).first()
            if ficha:
                camera.mana_personagem = ficha.mana_atual
                camera.hp_personagem = ficha.hp_atual
                camera.nome_personagem_atual = text
    def update_bg(self, *args):
        self.bg_rect.pos = (0, 0)
        self.bg_rect.size = Window.size
    def update_log_bg(self, *args):
        self.log_bg.pos = self.scroll_log.pos
        self.log_bg.size = self.scroll_log.size
    def update_cam_frame(self, dt):
        frame = get_frame()
        if frame is None:
            return
        # OpenCV -> Kivy Texture (BGR -> mantém bgr no blit; flip vertical p/ Kivy)
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.cam_view.texture = texture
    def reposicionar_elementos(self, *args):
        altura = Window.height
        largura = Window.width
        # Atualiza fundo
        self.bg_rect.size = Window.size
        self.bg_rect.pos = (0, 0)
        # Atualiza log
        largura_log = 300
        sub_box_width = (largura - 650) / 2
        self.scroll_log.size = (200, altura - 15)
        self.scroll_log.pos = ((largura/1.25), altura/10-40)
        self.log_bg.size = self.scroll_log.size
        self.log_bg.pos = self.scroll_log.pos
        # Atualiza posição do campo IP
        self.ip_text.size = ((largura - 650) / 2 - 18, 132)
        self.ip_text.pos = ((largura/3)+sub_box_width-25, altura/10-40)
        # Atualiza confirmar/input_text
        self.input_text.size = (sub_box_width, altura/10+3.5)
        self.input_text.pos= (largura/3-45, altura/5.5-20)
        self.confirmar.pos = (largura/3-45, altura/10-40)
        self.confirmar.size = (sub_box_width, altura/10)
        # === Câmera alinhada com input_text e ip_text ===
        self.cam_view.size = (sub_box_width*2,altura/1.5)
        self.cam_view.pos = (largura/3-45, altura/4+25)
        # === Botões ===
        self.criar_ficha.pos = (0, altura / 4 + 400)
        self.d4.pos = (0, altura / 4 + 335)
        self.d6.pos = (0, altura / 4 + 265)
        self.d10.pos = (100, altura / 4 + 265)
        self.d20.pos = (100, altura / 4 + 335)
        self.cura.pos = (largura/6-25, altura / 4+60)
        self.dano.pos = (0, altura / 4+60)
        self.up.pos = (0, altura / 4 - 85)
        self.down.pos = (0, altura / 4 - 145)
        self.esquerda.pos = (largura/6-25, altura / 4 - 145)
        self.direita.pos = (largura/6-25, altura / 4 - 85)
        self.efeitos.pos = (0, altura / 4 + 195)
        self.personagem.pos = (largura/6-25, altura / 4 + 195)
        self.aplicar_efeito.pos=(0, altura / 4 + 130)
        # Tamanhos
        self.criar_ficha.size = (largura/8, altura / 12)
        self.efeitos.size = (largura/8, altura / 12)
        self.personagem.size = (largura/8, altura / 12)
        self.d4.size = (80, altura / 12)
        self.d6.size = (80, altura / 12)
        self.d10.size = (80, altura / 12)
        self.d20.size = (80, altura / 12)
        self.cura.size = (largura/8, altura / 12)
        self.dano.size = (largura/8, altura / 12)
        self.up.size = (largura/8, altura / 14)
        self.down.size = (largura/8, altura / 14)
        self.esquerda.size = (largura/8, altura / 14)
        self.direita.size = (largura/8, altura / 14)
        self.aplicar_efeito.size = (largura/8, altura / 12)
