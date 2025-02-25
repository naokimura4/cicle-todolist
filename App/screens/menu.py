from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from assets.storage import salvar_dados
from screens.tela_horario import *

class Menu(Screen):
    def resetar_dados(self):
        carga_horaria_atual = self.manager.get_screen('ciclo').carga_horaria

        # Reseta apenas as matérias
        self.manager.get_screen('ciclo').materias = []

        # Salva os dados mantendo a carga horária
        salvar_dados(carga_horaria_atual, [])

        # Atualiza a tela do ciclo para refletir a mudança
        self.manager.get_screen('ciclo').populate_materias()

        # Mostra um popup de confirmação
        pop = Popup(
            title="Resetado!",
            content=Label(text="Todas as matérias foram apagadas."),
            size_hint=(None, None), size=(350, 150)
        )
        pop.open()
