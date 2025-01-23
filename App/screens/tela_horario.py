from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class TelaHorario(Screen):
    dias_input = ObjectProperty(None)
    horas_input = ObjectProperty(None)
    resultado_label = ObjectProperty(None)
    
    def calcular_ch(self):
        try:
            dia = int(self.dias_input.text)
            horas_minimas = int(self.horas_input.text)
            carga_horaria = dia * horas_minimas
            self.resultado_label.text = f'Carga Horária: {carga_horaria} horas'
            
            # Armazena a carga horária no ScreenManager
            self.manager.carga_horaria = carga_horaria
        except ValueError:
            self.resultado_label.text = 'Por favor, insira valores válidos.'