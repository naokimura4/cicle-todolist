from kivy.uix.screenmanager import Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from screens.tela_horario import TelaHorario

class Ciclo(Screen):
    materias = []  # Lista para armazenar matérias e suas dificuldades
    carga_horaria =  30 # Exemplo de carga horária (pode ser calculada) Usar a função calcular_ch da tela horário

    def on_kv_post(self, base_widget):
        """
        Método chamado após o KV ser carregado.
        Popula as matérias e checkboxes no layout.
        """
        self.calcular_checkboxes()
        self.populate_materias()

    def calcular_checkboxes(self):
        """
        Calcula o número de checkboxes para cada matéria com base na dificuldade.
        """
        # Soma dos níveis de dificuldade
        contador_de_diff = sum(materia["dificuldade"] for materia in self.materias)
        if contador_de_diff == 0:
            print("Erro: Nenhuma matéria com dificuldade definida.")
            return

        # Calcula o valor base
        valor_base = self.carga_horaria / contador_de_diff

        # Calcula o número de checkboxes para cada matéria
        for materia in self.materias:
            dificuldade = materia["dificuldade"]
            if dificuldade == 1:  # Péssimo
                materia["checkboxes"] = int(valor_base * 5)
            elif dificuldade == 2:  # Ruim
                materia["checkboxes"] = int(valor_base * 3)
            elif dificuldade == 3:  # Mediano
                materia["checkboxes"] = int(valor_base * 3)
            elif dificuldade == 4:  # Bom
                materia["checkboxes"] = int(valor_base * 2)
            elif dificuldade == 5:  # Excelente
                materia["checkboxes"] = int(valor_base * 1)

    def populate_materias(self):
        """
        Popula o layout com as matérias e seus checkboxes.
        """
        grid_layout = self.ids.grid_layout
        grid_layout.clear_widgets()  # Limpa os widgets existentes

        for materia in self.materias:
            nome = materia["nome"]
            quantidade = materia.get("checkboxes", 0)

            # Criar uma linha com GridLayout para alinhar horizontalmente
            linha_layout = GridLayout(cols=2, size_hint_y=None, height=50, spacing=10)

            # Nome da matéria
            linha_layout.add_widget(Label(
                text=nome,
                font_size=18,
                size_hint_x=None,
                width=200
            ))

            # Checkboxes
            checkboxes_layout = BoxLayout(orientation='horizontal', spacing=10)
            for _ in range(quantidade):
                checkbox = CheckBox(size_hint=(None, None), size=(40, 40))
                checkboxes_layout.add_widget(checkbox)

            linha_layout.add_widget(checkboxes_layout)
            grid_layout.add_widget(linha_layout)

    def adicionar_materia(self, nome, dificuldade):
        """
        Adiciona uma matéria e recalcula os checkboxes.
        """
        self.materias.append({"nome": nome, "dificuldade": dificuldade})
        self.calcular_checkboxes()
        self.populate_materias()


