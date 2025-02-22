from kivy.core.window import Window
from screens.menu import Menu
from screens.input_materia import InputMateria
from screens.tela_horario import TelaHorario 
from screens.transition_horario import TransitionHorario
from screens.welcome import Welcome
from screens.ciclo import Ciclo
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.config import Config

Config.set('graphics', 'height', '1920')
Config.set('graphics', 'width', '1080')

# ScreenManager
class Gerenciador(ScreenManager):
    ...

# App Principal
class MyCicleStudyApp(App):
    def build(self):
        Window.set_icon("App/img/logo.png")
        Builder.load_file('assets/Gerenciador.kv')
        # Criando o ScreenManager e adicionando a tela do menu
        sm = Gerenciador()
        sm.current = 'welcome'
        # Retornando o ScreenManager
        return sm

# Executando o aplicativo
if __name__ == '__main__':
    MyCicleStudyApp().run()