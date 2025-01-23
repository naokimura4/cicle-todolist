from kivy.uix.screenmanager import Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class Ciclo(Screen):
    materias = []
    carga_horaria = 0

    def on_enter(self):
        # Obtém a carga horária do ScreenManager
        self.carga_horaria = self.manager.carga_horaria
        self.calcular_checkboxes()
        self.populate_materias()

    def calcular_checkboxes(self):
        contador_de_diff = sum(materia["dificuldade"] for materia in self.materias)
        if contador_de_diff == 0:
            print("Erro: Nenhuma matéria com dificuldade definida.")
            return

        valor_base = self.carga_horaria / contador_de_diff

        for materia in self.materias:
            dificuldade = materia["dificuldade"]
            if dificuldade == 1:
                materia["checkboxes"] = int(valor_base * 5)
            elif dificuldade == 2:
                materia["checkboxes"] = int(valor_base * 3)
            elif dificuldade == 3:
                materia["checkboxes"] = int(valor_base * 3)
            elif dificuldade == 4:
                materia["checkboxes"] = int(valor_base * 2)
            elif dificuldade == 5:
                materia["checkboxes"] = int(valor_base * 1)

    def populate_materias(self):
        grid_layout = self.ids.grid_layout
        grid_layout.clear_widgets()

        for index, materia in enumerate(self.materias):
            nome = materia["nome"]
            quantidade = materia.get("checkboxes", 0)

            linha_layout = GridLayout(cols=3, size_hint_y=None, height=50, spacing=10)

            linha_layout.add_widget(Label(
                text=nome,
                font_size=18,
                size_hint_x=None,
                width=200
            ))

            checkboxes_layout = BoxLayout(orientation='horizontal', spacing=10)
            for _ in range(quantidade):
                checkbox = CheckBox(size_hint=(None, None), size=(40, 40))
                checkboxes_layout.add_widget(checkbox)

            linha_layout.add_widget(checkboxes_layout)

            excluir_button = Button(
                text="Excluir",
                size_hint_x=None,
                width=100
            )
            excluir_button.bind(on_release=lambda btn, idx=index: self.excluir_materia(idx))
            linha_layout.add_widget(excluir_button)

            grid_layout.add_widget(linha_layout)

    def adicionar_materia(self, nome, dificuldade):
        self.materias.append({"nome": nome, "dificuldade": dificuldade})
        self.calcular_checkboxes()
        self.populate_materias()

    def excluir_materia(self, index):
        del self.materias[index]
        self.calcular_checkboxes()
        self.populate_materias()
