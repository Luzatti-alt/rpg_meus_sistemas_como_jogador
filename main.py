from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from App_rpg import TelaPrincipal
from ficha_criar import TelaCriarFicha

class Gerenciador(ScreenManager):
    pass

class MeuApp(App):
    def build(self):
        sm = Gerenciador()
        sm.add_widget(TelaPrincipal(name="principal"))
        sm.add_widget(TelaCriarFicha(name="criar_ficha"))
        return sm

if __name__ == "__main__":
    MeuApp().run()