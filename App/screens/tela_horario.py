from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class TelaHorario(Screen):
    dias_input = ObjectProperty(None)
    horas_input = ObjectProperty(None)
    resultado_label = ObjectProperty(None)
    
    def calcular_ch(self):
        try:
            dia = int(dias_input.text)
            horas_minimas = int(horas_input.text)
            carga_horaria = dia * horas_minimas
            self.resultado_label.text = f'Carga Horária: {carga_horaria} horas'
        except ValueError:
            self.resultado_label.text = f'Por favor, insira valores válidos.' 