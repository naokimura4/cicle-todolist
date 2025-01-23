from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class InputMateria(Screen):
    nome_materia = ObjectProperty(None)
    spinner_diff = ObjectProperty(None)

    def salvar_materia(self):
        enviar_materia = self.nome_materia.text
        nivel_diff = self.spinner_diff.text

        if enviar_materia and nivel_diff != "Selecione":
            try:
                dificuldade = int(nivel_diff.split(" - ")[0])
                self.manager.get_screen('ciclo').adicionar_materia(enviar_materia, dificuldade)
                self.manager.current = 'ciclo'
            except ValueError:
                print("Erro: Dificuldade inválida.")
        else:
            print("Por favor, preencha todos os campos.")
