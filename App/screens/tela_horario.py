from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from screens.ciclo import *
from assets.storage import salvar_dados, carregar_dados  # Importamos as funções de salvamento

class TelaHorario(Screen):
    dias_input = ObjectProperty(None)
    horas_input = ObjectProperty(None)
    resultado_label = ObjectProperty(None)
    
    def on_enter(self):
        carga_horaria, _, _, _ = carregar_dados()  

        if carga_horaria > 0:
            self.resultado_label.text = f'Carga Horária Atual: {carga_horaria} horas'

        else:
            carga_horaria = 0  # Valor padrão

        if carga_horaria > 0:
            self.resultado_label.text = f'Carga Horária Atual: {carga_horaria} horas'


    def aviso_popup(self, titulo, mensagem):
        pop = Popup(
            title=titulo,
            content=Label(text=mensagem,
                halign="center",
                valign="middle",
                font_size=18,
            ),
            size_hint=(None, None),
            size=(700, 150),
        )
        pop.open()
        Clock.schedule_once(lambda dt: pop.dismiss(), 2)
        
    def calcular_ch(self):
        try:
            dias = int(self.dias_input.text) 
            horas_minimas = int(self.horas_input.text)
            if dias > 7 or horas_minimas >= 12:
                self.aviso_popup("Aviso!", "Escolha pelo menos 7 dias na semana para poder estudar.")
            else:
                carga_horaria = dias * horas_minimas

                self.resultado_label.text = f'Carga Horária: {carga_horaria} horas'
                self.aviso_popup("Atualizado", "Carga Horária Atualizada!")

                ciclo_screen = self.manager.get_screen('ciclo')
                ciclo_screen.carga_horaria = carga_horaria
                ciclo_screen.dias_para_reset = dias  # 🔥 Atualizando dias

                salvar_dados(carga_horaria, ciclo_screen.materias, ciclo_screen.ultima_data, dias)

        except ValueError:
            self.aviso_popup('Erro', 'Preencha todos os campos corretamente!')