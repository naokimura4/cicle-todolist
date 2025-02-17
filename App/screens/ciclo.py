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

    # Ao entrar, irão executar as funções de carregar_dados() para os dados salvos, além das demais. 
    def on_enter(self):
        if not self.materias:  # Só carrega se a lista estiver vazia
            self.carga_horaria, self.materias = carregar_dados()
        self.calcular_checkboxes()
        self.populate_materias()

    # Calcula a quantidade de checkbox por matéria com base em suas dificuldades
    def calcular_checkboxes(self): # Ajeitar
        contador_de_diff = sum(materia["dificuldade"] for materia in self.materias)
        if contador_de_diff == 0:
            return

        valor_base = self.carga_horaria / contador_de_diff

        for materia in self.materias:
            dificuldade = materia["dificuldade"] # Ajeitar
            multiplicador = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}.get(dificuldade, 1)
            materia["checkboxes"] = max(1, ceil(valor_base * multiplicador)) # Para, no mínimo, existir 1 checkbox
            # Se ainda não existir a lista de checkboxes, criar
            if "checkbox_states" not in materia or len(materia["checkbox_states"]) != materia["checkboxes"]:
                materia["checkbox_states"] = [False] * materia["checkboxes"]
                
    def populate_materias(self):
        # Será populado em formato de Grid
        grid_layout = self.ids.grid_layout
        grid_layout.clear_widgets()

        
        for index, materia in enumerate(self.materias):
            nome = materia["nome"]
            quantidade = materia.get("checkboxes", 0)
            
            linha_layout = GridLayout(cols=3, size_hint_y=None, height=50, spacing=10)
            linha_layout.add_widget(Label(text=nome, font_size=18, size_hint_x=None, width=200))
            # Adicionar Scroll da parte horizontal nas checkbox
            checkboxes_layout = BoxLayout(orientation='horizontal', spacing=10)
            
            for i in range(quantidade):
                checkbox = CheckBox(size_hint=(None, None), size=(40, 40))
                checkbox.active = materia["checkbox_states"][i]  # Manter estado salvo
                checkbox.bind(active=self.on_checkbox_active(materia, i))
                checkboxes_layout.add_widget(checkbox)

            linha_layout.add_widget(checkboxes_layout)

            excluir_button = Button(text="Excluir", size_hint_x=None, width=100)
            excluir_button.bind(on_release=lambda btn, idx=index: self.excluir_materia_popup(idx))
            linha_layout.add_widget(excluir_button)
            grid_layout.add_widget(linha_layout)

    def on_checkbox_active(self, materia, index):
        # Atualiza o estado das checkboxes e salva os dados.
        def callback(checkbox, value):
            materia["checkbox_states"][index] = value
            salvar_dados(self.carga_horaria, self.materias)  # Salvar progresso
            
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
            salvar_dados(self.carga_horaria, self.materias)  # Salvar dados ao adicionar
            debug_json()
        except Exception as e:
            print(f"Erro ao adicionar matéria: {e}") 
            
    def excluir_materia_popup(self, index):
        nome_materia = self.materias[index]["nome"]
        
        # Calcula a largura do popup com base no tamanho do nome da matéria
        largura_popup = max(350, min(150 + len(nome_materia) * 15, 800))  

        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        label = Label(text=f"Tem certeza que deseja excluir '{nome_materia}'?", 
                    font_size=18, 
                    halign='center', 
                    valign='middle', 
                    size_hint_y=None,
                    height=50)

        # Criar um layout para os botões e garantir que eles fiquem no centro
        botoes_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5})

        btn_confirmar = Button(text="Sim", size_hint=(None, None), size=(90, 50))
        btn_cancelar = Button(text="Não", size_hint=(None, None), size=(90, 50))

        # Configurar eventos dos botões
        btn_confirmar.bind(on_release=lambda btn: self.excluir_materia(index, popup))
        btn_cancelar.bind(on_release=lambda btn: popup.dismiss())

        botoes_layout.add_widget(btn_confirmar)
        botoes_layout.add_widget(btn_cancelar)

        layout.add_widget(label)
        layout.add_widget(botoes_layout)

        popup = Popup(title="Confirmação",
                    content=layout,
                    size_hint=(None, None), 
                    size=(largura_popup, 200))  

        popup.open()


    def confirmar_exclusao(self, index, popup):
        """ Exclui a matéria e fecha o popup """
        popup.dismiss()  # Fecha o popup
        self.excluir_materia(index)  # Chama a função para excluir
        
    def materia_concluida_popup(self, nome_materia): # Corrigir isso
        popup = Popup(title="Matéria Concluida",
                    content=Label(text=f"Parabéns! Você concluiu {nome_materia}!"),
                    size_hint=(None, None), size=(400, 100))
        popup.open()
            
    def excluir_materia(self, index,popup=None, *_):
        del self.materias[index]
        self.calcular_checkboxes()
        self.populate_materias()
        salvar_dados(self.carga_horaria, self.materias)  # Salvar dados ao excluir
        
        if popup:
            popup.dismiss()
        
    def verificar_conclusao(self):
        for materia in self.materias:
            if all(materia.checkbox_states):
                self.materia_concluida_popup(materia.nome)
                
    # Adicionar Reset das checkbox de acordo com os dias diff: DATA (Atual) - De maneira Assicrona saber quanto tempo falta para a semana diff dia aberto - dia determinado usar a função timer
    # Ver se muda a semana com relação aos "close" do aplicativo
    # 
        