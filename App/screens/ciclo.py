from kivy.uix.screenmanager import Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import math

class Ciclo(Screen):
    materias = []  # Lista para armazenar matérias e dificuldades
    carga_horaria_total = 0  # Carga Horária Total (dias * horas por dia)

    def calcular_carga_horaria(self, dias, horas_por_dia):
        """Calcula a Carga Horária Total."""
        self.carga_horaria_total = dias * horas_por_dia

    def calcular_distribuicao(self):
        """Calcula a distribuição da carga horária com base nas dificuldades."""
        if not self.materias or self.carga_horaria_total == 0:
            print("Erro: Não há matérias ou a carga horária total é zero.")
            return

        # Soma dos pesos (dificuldades)
        peso_total = sum(materia['dificuldade'] for materia in self.materias)
        if peso_total == 0:
            print("Erro: O peso total é zero.")
            return

        # Cálculo do valor base
        valor_base = self.carga_horaria_total / peso_total

        # Cálculo da carga horária de cada matéria
        for materia in self.materias:
            materia['carga_horaria'] = math.ceil(valor_base * materia['dificuldade'])

    def populate_materias(self):
        """Popula o layout com as matérias, checkboxes e botão de excluir."""
        grid_layout = self.ids.grid_layout
        grid_layout.clear_widgets()

        for index, materia in enumerate(self.materias):
            nome = materia["nome"]
            quantidade = materia.get("carga_horaria", 0)

            # Layout para alinhar os elementos horizontalmente
            linha_layout = GridLayout(cols=3, size_hint_y=None, height=50, spacing=10)

            # Nome da matéria
            linha_layout.add_widget(Label(
                text=nome,
                font_size=18,
                size_hint_x=None,
                width=200
            ))

            # Checkboxes representando as horas de estudo
            checkboxes_layout = BoxLayout(orientation='horizontal', spacing=5)
            for _ in range(quantidade):
                checkbox = CheckBox(size_hint=(None, None), size=(40, 40))
                checkboxes_layout.add_widget(checkbox)

            linha_layout.add_widget(checkboxes_layout)

            # Botão para excluir a matéria
            excluir_button = Button(
                text="Excluir",
                size_hint_x=None,
                width=100
            )
            excluir_button.bind(on_release=lambda btn, idx=index: self.excluir_materia(idx))
            linha_layout.add_widget(excluir_button)

            grid_layout.add_widget(linha_layout)

    def adicionar_materia(self, nome, dificuldade):
        """Adiciona uma matéria e recalcula a distribuição."""
        self.materias.append({"nome": nome, "dificuldade": dificuldade})
        self.calcular_distribuicao()
        self.populate_materias()

    def excluir_materia(self, index):
        """Remove uma matéria da lista e recalcula a distribuição."""
        del self.materias[index]
        self.calcular_distribuicao()
        self.populate_materias()
