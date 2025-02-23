from screens.tela_horario import *
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from assets.storage import salvar_dados, carregar_dados  # Importamos funções para salvar e carregar dados
from kivy.clock import Clock

class InputMateria(Screen):
    nome_materia = ObjectProperty(None)
    spinner_diff = ObjectProperty(None)

    def on_enter(self):
        """Carrega as matérias salvas ao entrar na tela."""
        _, materias, _, dias_para_reset = carregar_dados()
        self.manager.get_screen('ciclo').materias = materias  # Atualiza a lista de matérias

    def mostrar_popup(self, titulo, mensagem):
        """Exibe uma mensagem popup."""
        popup = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(None, None), size=(400, 100),
            padding=(10, 10, 10, 10)
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2) 

    def salvar_materia(self):
        enviar_materia = self.nome_materia.text
        nivel_diff = self.spinner_diff.text
        if enviar_materia and nivel_diff != "Selecione":
            try:
                dificuldade = int(nivel_diff.split(" - ")[0])
                ciclo_screen = self.manager.get_screen('ciclo')

                ciclo_screen.adicionar_materia(enviar_materia, dificuldade)

                self.mostrar_popup("Sucesso!", "Matéria adicionada com sucesso.")
                self.nome_materia.text = ''
                self.spinner_diff.text = 'Selecione'

            except ValueError:
                self.mostrar_popup("Erro!", "Por favor, selecione um nível de dificuldade.")
        else:
            self.mostrar_popup("Erro!", "Insira um valor válido.")
