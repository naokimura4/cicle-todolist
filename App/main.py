from screens.menu import Menu
from screens.input_materia import InputMateria
from screens.tela_horario import TelaHorario 
from screens.ciclo import Ciclo
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Definindo a tela do menu
class Gerenciador(ScreenManager):
    pass

# Definindo o aplicativo principal
class MyApp(App):
    def build(self):
        # Carregando o arquivo KV
        Builder.load_file('Gerenciador.kv')
        # Criando o ScreenManager e adicionando a tela do menu
        sm = Gerenciador()
        sm.current = 'menu'
        # Retornando o ScreenManager
        return sm

# Executando o aplicativo
if __name__ == '__main__':
    MyApp().run()