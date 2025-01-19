from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class TelaHorario(Screen):
    dias_input = ObjectProperty(None)
    horas_input = ObjectProperty(None)
    resultado_label = ObjectProperty(None)
    
    def calcular_ch(self):
        try:
            dia = int(self.dias_input.text)  # Corrigido para usar self
            horas_minimas = int(self.horas_input.text)  # Corrigido para usar self
            carga_horaria = dia * horas_minimas
            self.resultado_label.text = f'Carga Horária: {carga_horaria} horas'
        except ValueError:
            self.resultado_label.text = f'Por favor, insira valores válidos.' 