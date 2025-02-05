from kivy.uix.screenmanager import Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from math import ceil
import json
from screens.input_materia import InputMateria

# IMPLEMENTAR O JSON NO CÓDIGO E CARREGA-LO

class Ciclo(Screen):
    materias = []
    carga_horaria = 0 # Salvar a carga horária definida ao ser fechado.

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
                materia["checkboxes"] = max(1,ceil(int(valor_base * 5))) # Adicionar Math.ceil()
            elif dificuldade == 2:
                materia["checkboxes"] = max(1,ceil(int(valor_base * 3)))
            elif dificuldade == 3:
                materia["checkboxes"] = max(1,ceil(int(valor_base * 3)))
            elif dificuldade == 4:
                materia["checkboxes"] = max(1,ceil(int(valor_base * 2)))
            elif dificuldade == 5:
                materia["checkboxes"] = max(1,ceil(int(valor_base * 1)))

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

            # Garantir que "checkbox_states" tem o tamanho correto
            if "checkbox_states" not in materia or len(materia["checkbox_states"]) != quantidade:
                materia["checkbox_states"] = [False] * quantidade

            for i in range(quantidade):
                checkbox = CheckBox(size_hint=(None, None), size=(40, 40))
                checkbox.active = materia["checkbox_states"][i]
                checkbox.bind(active=self.on_checkbox_active(materia, i))
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

    def on_checkbox_active(self, materia, index): ## Manter ativado quando clicar em voltar
        def callback(checkbox, value):
            if "checkbox_states" not in materia:
                materia["checkbox_states"] = [False] * materia["checkboxes"]
            materia["checkbox_states"][index] = value
            if all(materia["checkbox_states"]):
                self.mostrar_concluido(materia["nome"])
        return callback
    
    def verificar_checkbox(self):
        for materia in self.materias:
            if not all(materia["checkbox_states"]):
                return False
        return True
    
    def mostrar_concluido(self,nome_materia):
        pop = Popup(
            title='Concluído',
            content=Label(text=f'{nome_materia} foi concluída com sucesso!'),
            size_hint=(None, None), size=(400, 100),
            padding=(10, 10, 10, 10)
        )
        pop.open()
        
    def mostrar_excluido(self, nome_materia):
        label = Label(
            text=f'A matéria de {nome_materia} foi excluída com sucesso!',
            size_hint_y=None
        )
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))  # Ajusta a altura
        pop = Popup(
            title='Matéria Excluída',
            content=label,
            size_hint=(None, None),  # Permite definir tamanho manualmente
        )
        # Ajusta o tamanho do popup baseado no tamanho do texto
        label.bind(texture_size=lambda instance, value: pop.setter('size')(pop, (value[0] + 40, value[1] + 60)))
        pop.open()

    def adicionar_materia(self, nome, dificuldade):
        self.materias.append({"nome": nome, "dificuldade": dificuldade})
        self.calcular_checkboxes()
        self.populate_materias()

    def excluir_materia(self, index):
        materia_excluida = self.materias[index]["nome"]
        del self.materias[index]
        self.calcular_checkboxes()
        self.populate_materias()
        self.mostrar_excluido(materia_excluida)
