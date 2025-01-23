from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class InputMateria(Screen):
    nome_materia = ObjectProperty(None)
    spinner_diff = ObjectProperty(None)

    def mostrar_popup(self, titulo, mensagem):
        pop = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(None, None), size=(400, 100),
            padding=(10, 10, 10, 10)
        )
        pop.open()

    def salvar_materia(self):
        enviar_materia = self.nome_materia.text
        nivel_diff = self.spinner_diff.text

        if enviar_materia and nivel_diff != "Selecione":
            try:
                dificuldade = int(nivel_diff.split(" - ")[0])
                self.manager.get_screen('ciclo').adicionar_materia(enviar_materia, dificuldade)
                self.manager.current = 'ciclo'
            except ValueError:
                self.mostrar_popup("Erro", "Por favor, selecione um nível de dificuldade.")
        else:
            self.mostrar_popup("Erro", "Insira um valor válido.")
            
        self.enviar_materia = self.nome_materia.text = ''
        self.nivel_diff = self.spinner_diff.text = 'Selecione'