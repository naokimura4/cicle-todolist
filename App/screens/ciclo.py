from screens.tela_horario import *
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from math import ceil
from assets.storage import * # Importamos as funções

class Ciclo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carga_horaria, self.materias = carregar_dados()

    def on_enter(self):
        if not self.materias:  # Só carrega se a lista estiver vazia
            self.carga_horaria, self.materias = carregar_dados()
        self.calcular_checkboxes()
        self.populate_materias()


    def calcular_checkboxes(self):
        contador_de_diff = sum(materia["dificuldade"] for materia in self.materias)
        if contador_de_diff == 0:
            return

        valor_base = self.carga_horaria / contador_de_diff

        for materia in self.materias:
            dificuldade = materia["dificuldade"]
            multiplicador = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}.get(dificuldade, 1)
            materia["checkboxes"] = max(1, ceil(valor_base * multiplicador))

            # Se ainda não existir a lista de checkboxes, criar
            if "checkbox_states" not in materia or len(materia["checkbox_states"]) != materia["checkboxes"]:
                materia["checkbox_states"] = [False] * materia["checkboxes"]
    def aviso_popup(self, titulo, mensagem):
        """Exibe uma mensagem popup de aviso."""
        pop = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(None, None), size=(400, 100),
            padding=(10, 10, 10, 10)
        )
        pop.open()
    
    def populate_materias(self):
        grid_layout = self.ids.grid_layout
        grid_layout.clear_widgets()

        for index, materia in enumerate(self.materias):
            nome = materia["nome"]
            quantidade = materia.get("checkboxes", 0)
            linha_layout = GridLayout(cols=3, size_hint_y=None, height=50, spacing=10)
            linha_layout.add_widget(Label(text=nome, font_size=18, size_hint_x=None, width=200))

            checkboxes_layout = BoxLayout(orientation='horizontal', spacing=10)
            for i in range(quantidade):
                checkbox = CheckBox(size_hint=(None, None), size=(40, 40))
                checkbox.active = materia["checkbox_states"][i]  # Manter estado salvo
                checkbox.bind(active=self.on_checkbox_active(materia, i))
                checkboxes_layout.add_widget(checkbox)

            linha_layout.add_widget(checkboxes_layout)

            excluir_button = Button(text="Excluir", size_hint_x=None, width=100)
            excluir_button.bind(on_release=lambda btn, idx=index: self.excluir_materia(idx))
            linha_layout.add_widget(excluir_button)

            grid_layout.add_widget(linha_layout)

    def on_checkbox_active(self, materia, index):
        """Atualiza o estado das checkboxes e salva os dados."""
        def callback(checkbox, value):
            materia["checkbox_states"][index] = value
            salvar_dados(self.carga_horaria, self.materias)  # Salvar progresso
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
            salvar_dados(self.carga_horaria, self.materias)  # Salvar dados ao adicionar
            debug_json()
        except Exception as e:
            print(f"Erro ao adicionar matéria: {e}") 
            
    def excluir_materia(self, index):
        del self.materias[index]
        self.calcular_checkboxes()
        self.populate_materias()
        salvar_dados(self.carga_horaria, self.materias)  # Salvar dados ao excluir

    def mostrar_popup(self, nome_materia): # Corrigir isso
        popup = Popup(title="Parabéns!",
                    content=Label(text=f"Você concluiu {nome_materia}!"),
                    size_hint=(None, None), size=(300, 200))
        popup.open()
        
    def verificar_conclusao(self):
        for materia in self.materias:
            if all(materia.checkbox_states):
                self.mostrar_popup(materia.nome)
    # Adicionar Popup de "CONCLUIDO"
    # Adicionar Reset de acordo com os dias
        