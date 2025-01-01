from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from screens.menu import Menu
from screens.input_materia import InputScreen
from screens.tela_horario import TelaHorario 

class Gerenciador(ScreenManager):
    pass

class MyAplicationApp(App):
    def build(self):
        return Gerenciador()

if __name__=="__main__":
    MyAplicationApp().run()