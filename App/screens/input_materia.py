from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class InputScreen(Screen):
    nome_materia = ObjectProperty(None)
    spinner_diff = ObjectProperty(None)

    def salvar_materia(self):
        # Captura os dados inseridos
        enviar_materia = self.nome_materia.text
        nivel_diff = self.spinner_diff.text
        # Fazer retorno como Objeto de CheckBox
        # Verificação simples
        if enviar_materia and nivel_diff != "Selecione":
            print(f"Matéria: {enviar_materia}, Dificuldade: {nivel_diff}")
        else:
            print("Por favor, preencha todos os campos.")
