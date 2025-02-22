from screens.tela_horario import *
from kivy.uix.screenmanager import Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from math import ceil
import datetime
from assets.storage import salvar_dados, carregar_dados

class Ciclo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.carga_horaria, self.materias, self.ultima_data, self.dias_para_reset = carregar_dados()
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.carga_horaria, self.materias, self.ultima_data, self.dias_para_reset = 0, [], None, 7

    def on_enter(self):
        self.atualizar_data()
        if not self.materias:
            self.carga_horaria, self.materias, self.ultima_data = carregar_dados()
        self.verificar_reset_diario()
        self.calcular_checkboxes()
        self.populate_materias()

    def atualizar_data(self):
        """Atualiza a data atual e os dias restantes para resetar as checkboxes."""
        hoje = datetime.date.today()

        # Atualiza o texto com a data atual
        if 'data_atual' in self.ids:
            self.ids.data_atual.text = f"Dia: {hoje.strftime('%d/%m/%Y')}"

        # Garante que ultima_data nunca seja None
        if not self.ultima_data:
            self.ultima_data = hoje.isoformat()

        ultima_data = datetime.date.fromisoformat(self.ultima_data)
        dias_passados = (hoje - ultima_data).days
        dias_restantes = self.dias_para_reset - dias_passados

        # Evita valores negativos e atualiza o texto
        if 'dias_para_reset' in self.ids:
            self.ids.dias_para_reset.text = f"Dias para Reset: {max(dias_restantes, 0)}"

    def verificar_reset_diario(self):
        hoje = datetime.date.today()

        if not self.ultima_data:
            self.ultima_data = hoje.isoformat()
            salvar_dados(self.carga_horaria, self.materias, self.ultima_data)
            return

        ultima_data = datetime.date.fromisoformat(self.ultima_data)

        if hoje == ultima_data:
            return

        for materia in self.materias:
            materia["checkbox_states"] = [False] * len(materia["checkbox_states"])

        self.ultima_data = hoje.isoformat()
        salvar_dados(self.carga_horaria, self.materias, self.ultima_data)

        self.populate_materias()


    def populate_materias(self):
        grid_layout = self.ids.grid_layout
        grid_layout.clear_widgets()

        for index, materia in enumerate(self.materias):
            nome = materia["nome"]
            quantidade = materia.get("checkboxes", 0)

            linha_layout = GridLayout(cols=3, size_hint_y=None, height=50, spacing=10)

            # Nome da matéria
            linha_layout.add_widget(Label(text=nome, font_size=18, size_hint_x=None, width=200))

            # Criando um ScrollView horizontal para os checkboxes
            scroll_view = ScrollView(
                do_scroll_x=True, do_scroll_y=False,
                size_hint=(1, None), height=50  # Ajusta altura e mantém largura flexível
            )

            checkboxes_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_x=None)
            checkboxes_layout.width = max(quantidade * 50, 200)  # Garante largura mínima

            for i in range(quantidade):
                checkbox = CheckBox(size_hint=(None, None), size=(40, 40))
                checkbox.active = materia["checkbox_states"][i]
                checkbox.bind(active=self.on_checkbox_active(materia, i))
                checkboxes_layout.add_widget(checkbox)

            scroll_view.add_widget(checkboxes_layout)
            linha_layout.add_widget(scroll_view)

            # Botão de exclusão
            excluir_button = Button(text="Excluir", size_hint_x=None, width=100)
            excluir_button.bind(on_release=self.criar_excluir_callback(index))
            linha_layout.add_widget(excluir_button)

            grid_layout.add_widget(linha_layout)


    def criar_excluir_callback(self, index):
        return lambda btn: self.excluir_materia_popup(index)

    def calcular_checkboxes(self):
        contador_de_diff = sum(materia.get("dificuldade", 1) for materia in self.materias)
        if contador_de_diff == 0:
            return

        valor_base = self.carga_horaria / contador_de_diff

        for materia in self.materias:
            dificuldade = materia.get("dificuldade", 1)
            multiplicador = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}.get(dificuldade, 1)
            materia["checkboxes"] = max(1, ceil(valor_base * multiplicador))

            if "checkbox_states" not in materia or len(materia["checkbox_states"]) != materia["checkboxes"]:
                materia["checkbox_states"] = [False] * materia["checkboxes"]
                
    def on_checkbox_active(self, materia, index):
        def callback(checkbox, value):
            materia["checkbox_states"][index] = value
            salvar_dados(self.carga_horaria, self.materias, self.ultima_data)

            if all(materia["checkbox_states"]):
                self.materia_concluida_popup(materia["nome"])
        return callback

    def adicionar_materia(self, nome, dificuldade):
        try:
            nova_materia = {
                "nome": nome,
                "dificuldade": dificuldade,
                "checkboxes": 1,
                "checkbox_states": [False]
            }
            self.materias.append(nova_materia)
            self.calcular_checkboxes()
            self.populate_materias()
            salvar_dados(self.carga_horaria, self.materias, self.ultima_data)
        except Exception as e:
            print(f"Erro ao adicionar matéria: {e}")
    
    def excluir_materia(self, index):
        if 0 <= index < len(self.materias):
            del self.materias[index]
            salvar_dados(self.carga_horaria, self.materias, self.ultima_data)
            self.populate_materias()
            
    def excluir_materia_popup(self, index):
        nome_materia = self.materias[index]["nome"]
        largura_popup = max(350, min(150 + len(nome_materia) * 15, 800))

        layout = BoxLayout(orientation='vertical', spacing=20, padding=(20, 0))

        label = Label(
            text=f"Tem certeza que deseja excluir:\n'{nome_materia}'\n",
            font_size=18,
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=50
        )

        botoes_layout = BoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5}
        )

        btn_confirmar = Button(text="Sim", size_hint=(None, None), size=(90, 50))
        btn_cancelar = Button(text="Não", size_hint=(None, None), size=(90, 50))

        popup = Popup(title="Confirmação", content=layout, size_hint=(None, None), size=(largura_popup, 200))

        btn_confirmar.bind(on_release=lambda btn: self.confirmar_exclusao(index, popup))
        btn_cancelar.bind(on_release=lambda btn: popup.dismiss())

        botoes_layout.add_widget(btn_confirmar)
        botoes_layout.add_widget(btn_cancelar)

        layout.add_widget(label)
        layout.add_widget(botoes_layout)

        popup.open()

    def materia_concluida_popup(self, nome_materia):
        popup = Popup(
            title="Matéria Concluída",
            content=Label(
                text=f"Parabéns! Você concluiu {nome_materia}!",
                halign="center",
                valign="middle",
                font_size=18,
            ),
            size_hint=(None, None),
            size=(400, 150),
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def confirmar_exclusao(self, index, popup):
        popup.dismiss()
        self.excluir_materia(index)